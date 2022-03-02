import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader
import os
from my_datasets.mutations import load_mutations
from datasets import GenerateMode, set_caching_enabled
from pytorch_ie import Document, Pipeline
from pytorch_lightning.callbacks.early_stopping import EarlyStopping


from pytorch_ie.models import TransformerSpanClassificationModel
from pytorch_ie.models import TransformerTokenClassificationModel

from pytorch_ie.taskmodules import (
    TransformerSpanClassificationTaskModule,
    TransformerTokenClassificationTaskModule,
)

import argparse
import json

from datetime import datetime


SPAN_CLASSIFICATION = False


def prepare_data(config):
    """..."""
    dataset_loaded = load_mutations(
        url=config["data_url"],
        data_mapping={
            "train": config["train"],
            # "test": config["test"],
        },
        # conversion_kwargs=dict(head_argument_name="head", tail_argument_name="tail"),
        download_mode=GenerateMode.FORCE_REDOWNLOAD,
        train_test_split=None,
    )

    # add empty lists for texts without entities
    for split, data in dataset_loaded.items():
        for doc in data:
            entities = doc.span_annotations("entities")
            if entities is None:
                doc._annotations["entities"] = []

    train_docs = dataset_loaded["train"]
    val_docs = dataset_loaded["validation"]
    # test_docs = dataset_loaded["test"]

    print("train docs: ", len(train_docs))
    print("val docs: ", len(val_docs))
    # print("test docs: ", len(test_docs))

    return train_docs, val_docs


def get_task_module(model_name):
    """..."""
    if SPAN_CLASSIFICATION:
        task_module = TransformerSpanClassificationTaskModule(
            tokenizer_name_or_path=model_name,
            max_length=300,
            padding="max_length",
            single_sentence=True,
            sentence_annotation="sentences",
        )
    else:
        task_module = TransformerTokenClassificationTaskModule(
            tokenizer_name_or_path=model_name,
            # max_length=512,
            # label_to_id=LABEL2ID,
            # padding="max_length",
            partition_annotation="sentences",
            truncation=True,
            max_window=512,
        )

    return task_module


def finetune_model(
    model_name, model_output_path, config, task_module, train_dataloader, val_dataloader, num_epochs=3
):
    """..."""
    if SPAN_CLASSIFICATION:

        model = TransformerSpanClassificationModel(
            model_name_or_path=model_name,
            # num_classes=len(task_module.label_to_id),
            t_total=len(train_dataloader) * num_epochs,
            learning_rate=1e-4,
        )
    else:
        model = TransformerTokenClassificationModel(
            model_name_or_path=model_name,
            num_classes=len(task_module.label_to_id),
            # t_total=len(train_dataloader) * num_epochs,
            learning_rate=1e-4,
        )

    checkpoint_callback = ModelCheckpoint(
        monitor="val/f1",
        dirpath=model_output_path,
        # filename="ner-{epoch:02d}-val_f1-{val/f1:.2f}",
        filename="ner-finetuned",
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
        fast_dev_run=False,
        max_epochs=config.get("num_epochs", num_epochs),
        gpus=0,
        enable_checkpointing=True,
        callbacks=[early_stop_callback, checkpoint_callback],
        precision=32,
        log_every_n_steps=10,
    )
    trainer.fit(model, train_dataloader, val_dataloader)

    task_module.save_pretrained(model_output_path)
    # model.save_pretrained(model_output_path)
    # trainer.save_checkpoint(model_output_path + "model.ckpt")


def main(config):
    pl.seed_everything(42)

    with open(config, "r") as read_handle:
        config = json.load(read_handle)

    t = datetime.now().strftime("%d_%m_%y_%H_%M")
    model_output_path = f"./model_output/run_{t}/"
    model_name = "bert-base-cased"
    num_epochs = 30
    batch_size = 12

    train_docs, val_docs = prepare_data(config)

    task_module = get_task_module(model_name)

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
        model_name, model_output_path, config, task_module, train_dataloader, val_dataloader, num_epochs=num_epochs
    )

    ################### PREDICTION ###############
    # print("\nPredicting:")

    # if SPAN_CLASSIFICATION:
    #     ner_taskmodule = TransformerSpanClassificationTaskModule.from_pretrained(
    #         pretrained_model_name_or_path=model_output_path
    #     )

    #     ner_model = TransformerSpanClassificationModel.from_pretrained(
    #         pretrained_model_name_or_path=model_output_path,
    #     )
    # else:
    #     ner_taskmodule = TransformerTokenClassificationTaskModule.from_pretrained(
    #         checkpoint_callback.best_model_path
    #     )
    #     ner_model = TransformerTokenClassificationModel.from_pretrained(
    #         checkpoint_callback.best_model_path
    #     )

    # ner_pipeline = Pipeline(model=ner_model, taskmodule=ner_taskmodule, device=-1)

    # for doc in test_docs:
    #     ner_pipeline(doc, predict_field="entities")
    #     predictions = doc.predictions("entities")
    #     if predictions is None:
    #         continue

    #     print(f"\nText: {doc.text}")
    #     for entity in predictions:
    #         entity_text = doc.text[entity.start : entity.end]
    #         label = entity.label
    #         print(f"{entity_text} -> {label}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("config", default=None, help="Path to config file.")

    args = parser.parse_args()

    main(args.config)
