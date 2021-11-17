from typing import Union

import numpy as np

from package.featurization import extract_features
from package.utils import load_model

MODEL = load_model("logistic-regression.onnx")


def classify_text(text: str) -> dict[str, Union[str, float]]:
    """Classify the given text into one of three Wikipedia categories.

    Parameters
    ----------
    text : str
        Text to classify.

    Returns
    -------
    dict[str, Union[str, float]]
        Label and probability.
    """
    # extract features from text
    vector = extract_features(text)

    # fire!
    prediction, probability = MODEL.run(None, {"input": np.array([vector], dtype=np.int64)})

    return {"label": prediction[0], "probability": float(probability[0][prediction[0]])}
