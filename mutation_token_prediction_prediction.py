import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader
import os
from my_datasets.mutations import load_mutations
from datasets import GenerateMode, set_caching_enabled
from pytorch_ie import Document, Pipeline
from pytorch_lightning.callbacks.early_stopping import EarlyStopping


# from pytorch_ie.data.datasets.conll2003 import load_conll2003

from pytorch_ie.models import TransformerSpanClassificationModel
from pytorch_ie.models import TransformerTokenClassificationModel

# from pytorch_ie.models.transformer_token_classification import TransformerSpanClassificationModel

from pytorch_ie.taskmodules import (
    TransformerSpanClassificationTaskModule,
    TransformerTokenClassificationTaskModule,
)

import argparse
import json


SPAN_CLASSIFICATION = False


def main(config):
    pl.seed_everything(42)

    with open(config, "r") as read_handle:
        config = json.load(read_handle)

    run_name = "run_25_02_22_12_06"
    model_output_path = f"./model_output/{run_name}/ner-finetuned.ckpt"
    model_name = "bert-base-cased"
    taskmodule_config_file = f"./model_output/{run_name}/taskmodule_config.json"
    predictions_output = f"./model_output/{run_name}/predictions_{run_name}.json"
    num_epochs = 2
    batch_size = 8

    with open(taskmodule_config_file) as read_handle:
        taskmodule_config = json.load(read_handle)

    dataset_loaded = load_mutations(
        url=config["data_url"],
        data_mapping={
            "test": config["test"],
        },
        download_mode=GenerateMode.FORCE_REDOWNLOAD,
        train_test_split=None,
    )

    for split, data in dataset_loaded.items():
        for doc in data:
            entities = doc.span_annotations("entities")
            if entities is None:
                doc._annotations["entities"] = []

    test_docs = dataset_loaded["test"]

    print("test docs: ", len(test_docs))

    if SPAN_CLASSIFICATION:
        ner_taskmodule = TransformerSpanClassificationTaskModule(
            tokenizer_name_or_path=model_name,
            max_length=300,
            padding="max_length",
            label_to_id=taskmodule_config["label_to_id"],
            single_sentence=False,
        )

        ner_model = TransformerSpanClassificationModel.from_pretrained(
            model_output_path
        )
    else:
        ner_taskmodule = TransformerTokenClassificationTaskModule(
            tokenizer_name_or_path=model_name,
            # max_length=512,
            # label_to_id=LABEL2ID,
            # padding="max_length",
            partition_annotation="sentences",
            label_to_id=taskmodule_config["label_to_id"],
            truncation=True,
            max_window=512,
        )

        # ner_model = TransformerTokenClassificationModel.from_pretrained(
        #     model_output_path
        # )

        ner_model = TransformerTokenClassificationModel.load_from_checkpoint(model_output_path)

    # creates id2label and label2id dicts
    # task_module.prepare(train_docs)

    # train_dataset = task_module.encode(train_docs, encode_target=True)
    # val_dataset = task_module.encode(val_docs, encode_target=True)
    test_dataset = ner_taskmodule.encode(test_docs, encode_target=True)

    ner_pipeline = Pipeline(model=ner_model, taskmodule=ner_taskmodule, device=-1)

    print("\nPredicting ...")
    out_docs = {"documents": []}
    for doc in test_docs:

        out_doc = {"text": doc.text, "ID": doc.id, "predicted_entities": []}

        ner_pipeline(doc, predict_field="entities")

        predictions = doc.predictions("entities")

        if predictions is None:

            out_doc["predicted_entities"] = []

        else:
            for entity in predictions:
                entity_text = doc.text[entity.start : entity.end]
                out_doc["predicted_entities"].append(
                    {
                        "begin": entity.start,
                        "end": entity.end,
                        "text": entity_text,
                        "type": entity.label,
                    }
                )
                label = entity.label

        out_docs["documents"].append(out_doc)

    with open(predictions_output, "w") as write_handle:
        json.dump(out_docs, write_handle)
    print("\nDone!\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("config", default=None, help="Path to config file.")

    args = parser.parse_args()

    main(args.config)
