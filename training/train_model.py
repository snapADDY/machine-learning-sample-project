import json
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import Int64TensorType
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

from package.featurization import VOCABULARY, extract_features


def load_dataset(filepath: Path) -> list[dict[str, str | int]]:
    """Load dataset from NDJSON file as list of dictionaries.

    Parameters
    ----------
    filepath : Path
        Filepath to NDJSON file.

    Returns
    -------
    list[dict[str, str | int]]
        Data set as list of dictionaries.
    """
    with filepath.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file]


def export_model(model: LogisticRegression, filepath: Path, num_features: int):
    """Export scikit-learn model to ONNX.

    Parameters
    ----------
    model : LogisticRegression
        Model to export.
    num_features: int
        Number of features the model expects.
    filepath : Path
        Filepath to export model to.
    opset : int
        ONNX opset number.
    """
    initial_type = [("input", Int64TensorType((None, num_features)))]
    onnx = convert_sklearn(model, initial_types=initial_type)

    with filepath.open("wb") as output:
        output.write(onnx.SerializeToString())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--cross-validation", type=int, default=5)

    args = parser.parse_args()

    # load dataset from disk
    dataset = load_dataset(args.dataset)

    # prepare data
    X = np.array([extract_features(example["text"]) for example in dataset])
    y = np.array([example["label"] for example in dataset])

    if args.cross_validation:
        # model for evaluation
        model = LogisticRegression()

        # perform cross-validation
        scores = cross_val_score(model, X, y, scoring="accuracy", cv=args.cross_validation)
        print(f"{args.cross_validation}-fold cross validation:", scores)

    # train final model on full dataset
    model = LogisticRegression()
    model.fit(X, y)

    # export to onnx
    export_model(model, filepath=args.model, num_features=len(VOCABULARY))
