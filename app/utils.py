from pathlib import Path

from onnxruntime import InferenceSession

from app.logging import Logger

LOGGER = Logger(__name__)


def load_model(name: str) -> InferenceSession | None:
    """Load classification model from disk.

    Parameters
    ----------
    name : str
        Name of the model to load.

    Returns
    -------
    InferenceSession | None
        Session for inference (or None if no model available).
    """
    filepath = Path(__file__).parent.resolve() / "model" / name
    if filepath.exists():
        return InferenceSession(filepath)

    LOGGER.warning("No model found (can be ignored during training).")
    return None
