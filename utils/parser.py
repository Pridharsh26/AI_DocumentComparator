import json


def save_json(result):

    with open(
        "output/comparison_result.json",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(result)