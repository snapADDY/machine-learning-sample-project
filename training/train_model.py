import json
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
import stopwordsiso
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline


def load_dataset(filepath: Path) -> pd.DataFrame:
    """Load dataset from NDJSON file as DataFrame.

    Parameters
    ----------
    filepath : Path
        Filepath to NDJSON file.

    Returns
    -------
    pd.DataFrame
        DataFrame with text and labels.
    """
    with filepath.open("r", encoding="utf-8") as file:
        return pd.DataFrame(json.loads(line) for line in file)


def export_pipeline(pipeline: Pipeline, filepath: Path, opset: int = 12):
    """Export scikit-learn pipeline to ONNX.

    Parameters
    ----------
    pipeline : Pipeline
        Pipeline to export.
    filepath : Path
        Filepath to export pipeline to.
    opset : int
        ONNX opset number.
    """
    initial_types = [("input", StringTensorType([None, 1]))]
    onnx = convert_sklearn(model=pipeline, initial_types=initial_types, target_opset=opset)

    with filepath.open("wb") as output:
        output.write(onnx.SerializeToString())


def create_pipeline() -> Pipeline:
    """Create a pipeline for bag-of-words and logistic regression.

    The CountVectorizer uses German stopwords and no more than 10,000 features.

    Returns
    -------
    Pipeline
        Bag-of-words and logistic regression pipeline.
    """
    return Pipeline(
        [
            ("bow", CountVectorizer(stop_words=stopwordsiso.stopwords("de"))),
            ("clf", LogisticRegression()),
        ]
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dataset-filepath", type=Path, required=True)
    parser.add_argument("--model-filepath", type=Path, required=True)
    parser.add_argument("--cross-validation", type=int, default=5)

    args = parser.parse_args()

    # load dataset from disk
    dataset = load_dataset(args.dataset_filepath)

    # print some stats
    print(dataset.loc[:, "label"].value_counts())

    if args.cross_validation:
        print(f"Using {args.cross_validation}-fold cross validation")

        # model for evaluation
        model = LogisticRegression()

        # perform cross-validation
        scores = cross_val_score(
            model,
            dataset.loc[:, "text"],
            dataset.loc[:, "label"],
            scoring="accuracy",
            cv=args.cross_validation,
            n_jobs=-1,
        )

        print(scores)

    # train final model on full dataset
    model = LogisticRegression()
    model.fit(dataset.loc[:, "text"], dataset.loc[:, "label"])

    # export to onnx
    export_pipeline(model, filepath=args.model_filepath)
