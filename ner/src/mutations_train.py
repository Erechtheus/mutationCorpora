import os
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader
from datasets import GenerateMode, set_caching_enabled
from pytorch_ie import Document, Pipeline
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.loggers import WandbLogger

from pytorch_ie.models import TransformerTokenClassificationModel

from pytorch_ie.taskmodules import (
    TransformerSpanClassificationTaskModule,
    TransformerTokenClassificationTaskModule,
)
import json
from datetime import datetime
import wandb
import torch
from tqdm import tqdm
import pandas as pd
from dataloaders.mutations import load_mutations

from nervaluate import Evaluator


wandb.init(project="mutation_ner")
wandb_logger = WandbLogger(project="mutation_ner")


SPAN_CLASSIFICATION = False


def prepare_data(config):
    """..."""
    dataset_loaded = load_mutations(
        url=config["data_url"],
        data_mapping={"train": config["train"]},
        download_mode=GenerateMode.FORCE_REDOWNLOAD,
        train_test_split=None,
    )

    train_docs = dataset_loaded["train"]
    val_docs = dataset_loaded["validation"]

    wandb.log({"num_train": len(train_docs)})
    wandb.log({"num_val": len(val_docs)})

    return train_docs, val_docs


def get_task_module(model_name, config):
    """..."""
    if SPAN_CLASSIFICATION:
        task_module = TransformerSpanClassificationTaskModule(
            tokenizer_name_or_path=model_name,
            max_length=config["max_window"],
            padding="max_length",
            single_sentence=True,
            sentence_annotation="sentences",
        )
    else:
        task_module = TransformerTokenClassificationTaskModule(
            tokenizer_name_or_path=model_name,
            entity_annotation="entities",
            partition_annotation="sentences",
            truncation=True,
            max_window=config["max_window"],
            show_statistics=True,
        )

    return task_module


def finetune_model(
    model_name,
    model_output_path,
    config,
    task_module,
    train_dataloader,
    val_dataloader,
    model_out_name,
    num_epochs=3,
    debug=False,
):
    """..."""
    if SPAN_CLASSIFICATION:

        model = TransformerSpanClassificationModel(
            model_name_or_path=model_name,
            t_total=len(train_dataloader) * num_epochs,
            learning_rate=config["learning_rate"],
        )
    else:
        model = TransformerTokenClassificationModel(
            model_name_or_path=model_name,
            num_classes=len(task_module.label_to_id),
            learning_rate=config["learning_rate"],
        )

    checkpoint_callback = ModelCheckpoint(
        monitor="val/f1",
        dirpath=model_output_path,
        # filename="ner-{epoch:02d}-val_f1-{val/f1:.2f}",
        filename=model_out_name,
        save_top_k=1,
        mode="max",
        auto_insert_metric_name=False,
        save_weights_only=False,
    )

    # add early stopping
    early_stop_callback = EarlyStopping(
        monitor="val/f1",
        min_delta=0.002,
        patience=4,
        verbose=True,
        mode="max",
        strict=True,
    )

    trainer = pl.Trainer(
        fast_dev_run=debug,
        max_epochs=config.get("num_epochs", num_epochs),
        gpus=1,
        enable_checkpointing=True,
        callbacks=[early_stop_callback, checkpoint_callback],
        precision=32,
        log_every_n_steps=10,
        logger=wandb_logger,
    )
    trainer.fit(model, train_dataloader, val_dataloader)

    task_module.save_pretrained(model_output_path)


def calculate_results(golds, preds, labels):
    """..."""
    evaluator = Evaluator(true=golds, pred=preds, tags=labels)
    # Returns overall metrics and metrics for each tag
    results, results_per_label = evaluator.evaluate()
    print(f"results per label: {results_per_label}")
    print(f"\n\nresults overall: {results}")

    # calculate f1 score for exact match manually
    ov_prec = results["exact"]["precision"]
    ov_rec = results["exact"]["recall"]
    try:
        overall_f1 = 2 * (ov_prec * ov_rec) / (ov_prec + ov_rec)
    except ZeroDivisionError:
        overall_f1 = 0.0
    results["exact"]["f1"] = overall_f1

    overall_df = pd.DataFrame(results).reindex(["correct", "incorrect", "partial", "missed", "spurious", "actual", "precision", "recall", "f1"]).reset_index()
    wandb.log({"overall_precision_exact": ov_prec})
    wandb.log({"overall_recall_exact": ov_rec})
    wandb.log({"overall_f1_exact": results["exact"]["f1"]})

    wandb.log({"overall": wandb.Table(dataframe=overall_df)})

    for label, res in results_per_label.items():
        print(label)
        wandb.log({f"{label}_precision_exact": res["exact"]["precision"]})
        wandb.log({f"{label}_recall_exact": res["exact"]["recall"]})
        wandb.log({f"{label}_f1_exact": res["exact"]["f1"]})

        df = pd.DataFrame(res)
        df = df.reindex(["correct", "incorrect", "partial", "missed", "spurious", "actual", "precision", "recall", "f1"]).reset_index()

        wandb.log({label: wandb.Table(dataframe=df)})



def eval_on_dev_set(data, task_module, model_output_dir, run_name):
    """Evaluate the best model on the development set."""
    model_path = os.path.join(model_output_dir, run_name, "ner-finetuned.ckpt")

    if SPAN_CLASSIFICATION:

        ner_model = TransformerSpanClassificationModel.from_pretrained(model_path)
    else:
        # this is only to avoid confusion with the transformers warning
        print(f"Loading model ...")
        ner_model = TransformerTokenClassificationModel.load_from_checkpoint(model_path)

    if torch.cuda.is_available():
        device_id = 0
    else:
        device_id = -1

    ner_pipeline = Pipeline(model=ner_model, taskmodule=task_module, device=device_id)

    print("\nPredicting ...")
    golds = []
    preds = []
    out_docs = {"documents": []}

    for i, doc in tqdm(enumerate(data)):
        pred = []
        gold = []

        if i == 0:
            out_docs["referenceURL"] = doc.metadata["ref_url"]
            out_docs["version"] = doc.metadata["version"]
            out_docs["bibtex"] = doc.metadata["bibtex"]

        out_doc = {"text": doc.text, "ID": doc.id, "predicted_entities": []}

        ner_pipeline(doc, predict_field="entities")

        try:
            predictions = doc.predictions.spans["entities"]
        except KeyError:
            predictions = None

        # get the gold annotations and collect them in evaluation format
        # gold_spans = doc.annotations("entities")
        gold_spans = doc.annotations.spans["entities"]

        for span in gold_spans:
            gold.append(
                {
                    "start": span.start,
                    "end": span.end,
                    "label": span.label,
                }
            )

        # do the same for the predictions: 1) for evaluation, 2) for output
        # format
        if predictions is not None:
            for entity in predictions:
                start = entity.start
                end = entity.end
                entity_text = doc.text[start:end]
                label = entity.label

                out_doc["predicted_entities"].append(
                    {
                        "begin": start,
                        "end": end,
                        "text": entity_text,
                        "type": label,
                    }
                )

                pred.append(
                    {
                        "start": start,
                        "end": end,
                        "label": label,
                    }
                )

        out_docs["documents"].append(out_doc)
        preds.append(pred)
        golds.append(gold)
    # write predictions to file
    # print(json.dumps(out_docs, indent=2))

    # remove the BIO tags from the labels
    bio_labels = list(task_module.label_to_id.keys())
    labels = []
    for l in bio_labels:
        if l == "O":
            continue
        else:
            if l.startswith("B-"):
                labels.append(l.replace("B-", ""))
            elif l.startswith("I-"):
                labels.append(l.replace("I-", ""))

    calculate_results(golds=golds, preds=preds, labels=list(set(labels)))


def run_training(config, final_eval_on_val=False, debug=False):
    pl.seed_everything(42)

    wandb.log({"config_file": config})

    with open(config, "r") as read_handle:
        config = json.load(read_handle)

    # set config defaults
    wandb.config.setdefaults(config)

    print(f"\nConfig: {wandb.config}")

    t = datetime.now().strftime("%d_%m_%y_%H_%M")
    model_dir = "model_output/"
    run_name = f"run_{t}/"
    model_output_path = os.path.join(model_dir, run_name)
    model_out_name = "ner-finetuned"
    model_type = wandb.config["model"]
    num_epochs = wandb.config["epochs"]
    batch_size = wandb.config["batch_size"]

    train_docs, val_docs = prepare_data(config=wandb.config)

    task_module = get_task_module(model_type, config=wandb.config)

    # creates id2label and label2id dicts
    task_module.prepare(train_docs)

    # encode the data
    train_dataset = task_module.encode(train_docs, encode_target=True)
    val_dataset = task_module.encode(val_docs, encode_target=True)
    # test_dataset = task_module.encode(test_docs, encode_target=True)

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=task_module.collate,
        num_workers=8,
    )

    val_dataloader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=task_module.collate,
        num_workers=8,
    )

    finetune_model(
        model_type,
        model_output_path,
        wandb.config,
        task_module,
        train_dataloader,
        val_dataloader,
        model_out_name=model_out_name,
        num_epochs=num_epochs,
        debug=debug,
    )

    wandb.log({"run_name": run_name, "model_dir": model_dir})

    if final_eval_on_val:
        # take dev data before encoding
        eval_on_dev_set(
            data=val_docs,
            task_module=task_module,
            model_output_dir=model_dir,
            run_name=run_name
            #run_name="run_09_03_22_17_04",
        )
    return run_name, model_dir, model_type


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("config", default=None, help="Path to config file.")

    args = parser.parse_args()

    main(args.config)
