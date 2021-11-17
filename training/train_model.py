import json
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
import stopwordsiso
import tqdm
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
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
        return pd.DataFrame(json.loads(line) for line in tqdm.tqdm(file, desc="Loading data set"))


def export_pipeline(pipeline: Pipeline, filepath: Path):
    """Export scikit-learn pipeline to ONNX.

    Parameters
    ----------
    pipeline : Pipeline
        Pipeline to export.
    filepath : Path
        Filepath to export pipeline to.
    """
    onnx = convert_sklearn(
        model=pipeline, initial_types=[("input", StringTensorType([None, 1]))], target_opset=12
    )

    with filepath.open("wb") as output:
        output.write(onnx.SerializeToString())


def create_pipeline() -> Pipeline:
    """Create a pipeline with bag-of-words and logistic regression.

    The CountVectorizer uses German stopwords and no more than 10,000 features.

    Returns
    -------
    Pipeline
        Bag-of-words and logistic regression pipeline.
    """
    return Pipeline(
        [
            (
                "tfidf",
                CountVectorizer(stop_words=stopwordsiso.stopwords("de"), max_features=10000),
            ),
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
        kf = KFold(n_splits=args.cross_validation, shuffle=True, random_state=42)

        for train_index, test_index in kf.split(dataset):
            train, test = dataset.iloc[train_index], dataset.iloc[test_index]

            pipeline = create_pipeline()
            pipeline.fit(train.loc[:, "text"], train.loc[:, "label"])

            prediction = pipeline.predict(test.loc[:, "text"])

            print(classification_report(test.loc[:, "label"], prediction))

    # train final model on full dataset
    pipeline = create_pipeline()
    pipeline.fit(dataset.loc[:, "text"], dataset.loc[:, "label"])

    # export to onnx
    export_pipeline(pipeline, filepath=args.model_filepath)
