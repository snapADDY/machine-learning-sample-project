from pathlib import Path

from onnxruntime import InferenceSession


def load_model(name: str) -> InferenceSession:
    """Load classification model from disk.

    Parameters
    ----------
    name : str
        Name of the model to load.

    Returns
    -------
    InferenceSession
        Session for inference.
    """
    filepath = Path(__file__).parent.resolve() / "model" / name
    return InferenceSession(filepath)
