import datasets
import json

class LocalTestDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features({
                "text": datasets.Value("string"),
                "label": datasets.Value("int64"),
            })
        )

    def _split_generators(self, dl_manager):
        # We assume the file is resolved via HF Hub
        # Use simple path, dl_manager handles resolution relative to script base
        downloaded_files = dl_manager.download_and_extract({
            "train": "train.jsonl"
        })
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            for i, line in enumerate(f):
                yield i, json.loads(line)
