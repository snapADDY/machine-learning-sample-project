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


def extract_features(text: str) -> list[int]:
    """Extract features from the given text.

    Parameters
    ----------
    text : str
        Text to extract features from.

    Returns
    -------
    list[int]
        Feature vector.
    """
    # split text into tokens
    tokens = tokenize(text)

    # create binary feature vector (1 if token of vocabulary is in text, 0 otherwise)
    return [1 if token in tokens else 0 for token in VOCABULARY]
