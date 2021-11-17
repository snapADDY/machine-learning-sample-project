import numpy as np

VOCABULARY = [
    "fernsehserie",
    "episoden",
    "staffeln",
    "leinwand",
    "museum",
    "öl",
    "studioalbum",
    "rockband",
    "charts",
]


def tokenize(text: str) -> set[str]:
    """Lowercase text and split into a set of tokens.

    Parameters
    ----------
    text : str
        Text to tokenize.

    Returns
    -------
    set[str]
        Set of lowercase tokens.
    """
    return set(text.lower().split())


def extract_features(text: str) -> np.ndarray:
    """Extract features from the given text.

    Parameters
    ----------
    text : str
        Text to extract features from.

    Returns
    -------
    np.ndarray
        Feature vector.
    """
    tokens = tokenize(text)

    vector = [1 if token in tokens else 0 for token in VOCABULARY]

    return np.array(vector)
