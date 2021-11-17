from pathlib import Path

from onnxruntime import InferenceSession


def load_model(name: str) -> InferenceSession:
    """Load classification model from disk.

    Parameters
    ----------
    name : str
        Filename of the model to load.

    Returns
    -------
    InferenceSession
        Session for inference.
    """
    module_path = Path(__file__).parent.resolve()
    model_filepath = Path(module_path, "model", name)
    return InferenceSession(str(model_filepath))
