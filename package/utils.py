from pathlib import Path

from onnxruntime import InferenceSession


def load_model(name: str) -> InferenceSession:
    """[summary]

    Parameters
    ----------
    name : str
        [description]

    Returns
    -------
    InferenceSession
        [description]
    """
    module_path = Path(__file__).parent.resolve()
    model_filepath = Path(module_path, "model", name)
    return InferenceSession(str(model_filepath))
