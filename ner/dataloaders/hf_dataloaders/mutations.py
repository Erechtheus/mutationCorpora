import glob
import logging
from dataclasses import dataclass
from os import listdir, path
from typing import Dict, List, Optional
import json
import os
import datasets
from datasets import (
    BuilderConfig,
    DatasetInfo,
    Features,
    Sequence,
    SplitGenerator,
    Value,
)
import syntok.segmenter as segmenter
import spacy
from spacy.util import filter_spans
from collections import namedtuple

logger = logging.getLogger(__name__)


@dataclass
class MutationsConfig(BuilderConfig):
    """BuilderConfig for BRAT."""

    url: str = None  # type: ignore
    description: Optional[str] = None
    citation: Optional[str] = None
    homepage: Optional[str] = None

    data_mapping: Optional[Dict[str, str]] = None
    # subdirectory_mapping: Optional[Dict[str, str]] = None
    # file_name_blacklist: Optional[List[str]] = None
    # ann_file_extension: str = "ann"
    # txt_file_extension: str = "txt"


class Mutations(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = MutationsConfig

    def _info(self):
        return DatasetInfo(
            description=self.config.description,
            citation=self.config.citation,
            homepage=self.config.homepage,
            features=Features(
                {
                    "context": Value("string"),
                    "file_name": Value("string"),
                    "ID": Value("string"),
                    "sentences": Sequence(Value("string")),
                    "sentence_offsets": Sequence(
                        {"start": Value("int32"), "end": Value("int32")}
                    ),
                    "spans": Sequence(
                        {
                            "id": Value("string"),
                            "type": Value("string"),
                            "locations": Sequence(
                                {
                                    "start": Value("int32"),
                                    "end": Value("int32"),
                                }
                            ),
                            "text": Value("string"),
                        }
                    ),
                    "relations": Sequence(
                        {
                            "id": Value("string"),
                            "type": Value("string"),
                            "arguments": Sequence(
                                {"type": Value("string"), "target": Value("string")}
                            ),
                        }
                    ),
                    "equivalences": Sequence(Value("string")),
                    "metadata": Sequence(Value("string")),
                    "ref_url": Value("string"),
                    "bibtex": Value("string"),
                    "version": Value("string"),
                    # "equivalence_relations": Sequence(
                    #     {
                    #         "type": Value("string"),
                    #         "targets": Sequence(Value("string")),
                    #     }
                    # ),
                    "events": Sequence(
                        {
                            "id": Value("string"),
                            "type": Value("string"),
                            "trigger": Value("string"),
                            "arguments": Sequence(
                                {"type": Value("string"), "target": Value("string")}
                            ),
                        }
                    ),
                    "attributions": Sequence(
                        {
                            "id": Value("string"),
                            "type": Value("string"),
                            "target": Value("string"),
                            "value": Value("string"),
                        }
                    ),
                    "normalizations": Sequence(
                        {
                            "id": Value("string"),
                            "type": Value("string"),
                            "target": Value("string"),
                            "resource_id": Value("string"),
                            "entity_id": Value("string"),
                        }
                    ),
                    "notes": Sequence(
                        {
                            "id": Value("string"),
                            "type": Value("string"),
                            "target": Value("string"),
                            "note": Value("string"),
                        }
                    ),
                }
            ),
        )

    # @staticmethod
    # def _get_location(location_string):
    #     parts = location_string.split(" ")
    #     assert (
    #         len(parts) == 2
    #     ), f"Wrong number of entries in location string. Expected 2, but found: {parts}"
    #     return {"start": int(parts[0]), "end": int(parts[1])}

    def _filter_overlaps(entities):
        """..."""
        if not entities:
            return entities
        Span = namedtuple("Span", ["start", "end", "ID", "type", "text"])
        # [{'ID': 'T21', 'type': 'Gene_protein', 'begin': 1488, 'end': 1492, 'text': 'BRAF'},
        # print(f"\nentities: {entities}\n")
        spans = [
            Span(
                start=ent["begin"],
                end=ent["end"],
                ID=ent["ID"],
                type=ent["type"],
                text=ent["text"],
            )
            for ent in entities
        ]
        # print(f"spans: {spans}")

        filtered = filter_spans(spans)
        # print(f"\nfiltered: {filtered}\n{len(spans)}, {len(filtered)}\n{[span._asdict() for span in filtered]}\n#########################\n")

        if len(spans) != len(filtered):
            print(f"\nFiltered: {len(spans)}, {len(filtered)}\n")

        return [span._asdict() for span in filtered]

    @staticmethod
    def _get_span_annotation(entities):
        """
        example input:
        T1  Organization 0 4    Sony
        """

        # _id, remaining, text = annotation_line.split("\t", maxsplit=2)
        # _type, locations = remaining.split(" ", maxsplit=1)
        # return {
        #     "id": _id,
        #     "text": text,
        #     "type": _type,
        #     "locations": [Brat._get_location(loc) for loc in locations.split(";")],
        # }

        filtered_ents = Mutations._filter_overlaps(entities)
        span_annos = []
        for entity in filtered_ents:
            span_annos.append(
                {
                    "id": entity["ID"],
                    "text": entity["text"],
                    "type": entity["type"],
                    "locations": [{"start": entity["start"], "end": entity["end"]}],
                }
            )

        return span_annos

    @staticmethod
    def _get_equivalence_annotation(equivalences):
        """..."""
        return equivalences

    @staticmethod
    def _get_metadata_annotation(metadata):
        """..."""
        return metadata

    @staticmethod
    def _get_event_annotation(annotation_line):
        """
        example input:
        E1  MERGE-ORG:T2 Org1:T1 Org2:T3
        """
        _id, remaining = annotation_line.strip().split("\t")
        args = [
            dict(zip(["type", "target"], a.split(":"))) for a in remaining.split(" ")
        ]
        return {
            "id": _id,
            "type": args[0]["type"],
            "trigger": args[0]["target"],
            "arguments": args[1:],
        }

    @staticmethod
    def _get_relation_annotation(relations):
        """
        example input:
        R1  Origin Arg1:T3 Arg2:T4
        """

        # _id, remaining = annotation_line.strip().split("\t")
        # _type, remaining = remaining.split(" ", maxsplit=1)
        # args = [dict(zip(["type", "target"], a.split(":"))) for a in remaining.split(" ")]
        # return {"id": _id, "type": _type, "arguments": args}
        rel_annos = []
        for relation in relations:
            rel = relation.copy()
            del rel["ID"]
            del rel["type"]
            arguments = []
            for key, value in rel.items():
                f = {}
                f["type"] = key
                f["target"] = value
                arguments.append(f)

            rel_annos.append(
                {"id": relation["ID"], "type": relation["type"], "arguments": arguments}
            )
        return rel_annos

    @staticmethod
    def _get_equivalence_relation_annotation(annotation_line):
        """
        example input:
        *   Equiv T1 T2 T3
        """
        _, remaining = annotation_line.strip().split("\t")
        parts = remaining.split(" ")
        return {"type": parts[0], "targets": parts[1:]}

    @staticmethod
    def _get_attribute_annotation(annotation_line):
        """
        example input (binary: implicit value is True, if present, False otherwise):
        A1  Negation E1
        example input (multi-value: explicit value)
        A2  Confidence E2 L1
        """

        _id, remaining = annotation_line.strip().split("\t")
        parts = remaining.split(" ")
        # if no value is present, it is implicitly "true"
        if len(parts) == 2:
            parts.append("true")
        return {
            "id": _id,
            "type": parts[0],
            "target": parts[1],
            "value": parts[2],
        }

    @staticmethod
    def _get_normalization_annotation(annotation_line):
        """
        example input:
        N1  Reference T1 Wikipedia:534366   Barack Obama
        """
        _id, remaining, text = annotation_line.split("\t", maxsplit=2)
        _type, target, ref = remaining.split(" ")
        res_id, ent_id = ref.split(":")
        return {
            "id": _id,
            "type": _type,
            "target": target,
            "resource_id": res_id,
            "entity_id": ent_id,
        }

    @staticmethod
    def _get_note_annotation(annotation_line):
        """
        example input:
        #1  AnnotatorNotes T1   this annotation is suspect
        """
        _id, remaining, note = annotation_line.split("\t", maxsplit=2)
        _type, target = remaining.split(" ")
        return {
            "id": _id,
            "type": _type,
            "target": target,
            "note": note,
        }

    @staticmethod
    def _read_annotations(document):
        """
        reads a BRAT v1.3 annotations file (see https://brat.nlplab.org/standoff.html)
        """

        res = {
            "spans": [],
            "events": [],
            "relations": [],
            "equivalences": [],
            "attributions": [],
            "normalizations": [],
            "notes": [],
            "metadata": [],
        }

        # with open(filename) as file:
        #     for i, line in enumerate(file):
        #         if len(line.strip()) == 0:
        #             continue
        #         ann_type = line[0]

        #         # strip away the new line character
        #         if line.endswith("\n"):
        #             line = line[:-1]

        # if ann_type == "T":
        res["spans"] = Mutations._get_span_annotation(document["entities"])
        # elif ann_type == "E":
        # res["events"].append(Mutations._get_event_annotation(line))
        # elif ann_type == "R":
        res["relations"] = Mutations._get_relation_annotation(document["relations"])
        # elif ann_type == "*":
        # res["relations"].append(Mutations._get_equivalence_relation_annotation(line))
        res["equivalences"] = Mutations._get_equivalence_annotation(
            document["equivalences"]
        )
        res["metadata"] = Mutations._get_metadata_annotation(document["metadata"])

        # elif ann_type in ["A", "M"]:
        #     res["attributions"].append(Mutations._get_attribute_annotation(line))
        # elif ann_type == "N":
        #     res["normalizations"].append(Mutations._get_normalization_annotation(line))
        # elif ann_type == "#":
        #     res["notes"].append(Mutations._get_note_annotation(line))
        # else:
        #     raise ValueError(
        #         f'unknown BRAT annotation id type: "{line}" (from file {filename} @line {i}). '
        #         f"Annotation ids have to start with T (spans), E (events), R (relations), "
        #         f"A (attributions), or N (normalizations). See "
        #         f"https://brat.nlplab.org/standoff.html for the BRAT annotation file "
        #         f"specification."
        #     )
        return res

    def _get_sentences_spans(text):
        """Segment the text into sentences and return offsets."""
        sentences = []
        sentence_offsets = []
        for paragraph in segmenter.analyze(text):
            for sent in paragraph:
                # print(sent)
                sentences.append("".join(map(str, sent)).lstrip())
                sentence_offsets.append(
                    {
                        "start": sent[0].offset,
                        "end": sent[-1].offset + len(sent[-1].value),
                    }
                )

        return sentences, sentence_offsets

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)

        with open(filepath, encoding="utf-8") as read_handle:
            data = json.load(read_handle)

        ref_url = data["referenceURL"]
        version = data["version"]
        bibtex = data["bibtex"]

        for example in data["documents"]:

            # print(f"\nDOC ID: {id_}")
            id_ = example["document"]["ID"]

            text = example["document"].get("text")

            # assert False
            # ann_fn = f"{filename}.{self.config.ann_file_extension}"
            brat_annotations = Mutations._read_annotations(example["document"])
            sentences, sentence_offsets = Mutations._get_sentences_spans(text)

            # txt_fn = f"{filename}.{self.config.txt_file_extension}"
            # txt_content = open(txt_fn).read()
            brat_annotations["context"] = text
            brat_annotations["ID"] = id_
            brat_annotations["file_name"] = filepath
            brat_annotations["sentences"] = sentences
            brat_annotations["sentence_offsets"] = sentence_offsets

            brat_annotations["ref_url"] = ref_url
            brat_annotations["version"] = version
            brat_annotations["bibtex"] = bibtex

            yield id_, brat_annotations

    def _split_generators(self, dl_manager) -> List[datasets.SplitGenerator]:
        """Return SplitGenerators."""
        data_mapping = self.config.data_mapping

        print(self.config)

        assert self.config.url is not None, "data url not specified"

        if "train" in data_mapping:

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(self.config.url, data_mapping["train"])
                    },
                ),
                #     datasets.SplitGenerator(
                #         name=datasets.Split.TEST,
                #         gen_kwargs={
                #             "filepath": os.path.join(self.config.url, data_mapping["test"])
                #         },
                #     ),
                #
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(self.config.url, data_mapping["test"])
                    },
                ),
            ]
