import numpy as np
from classification import utils
from classification.dtos import RequestDTO, ResponseDTO
from falcon import Request, Response
from falcon.status_codes import HTTP_OK

MODEL = utils.load_model("logistic-regression.onnx")


def classify_text(text: str) -> tuple[str, float]:
    prediction, probability = MODEL.run(None, {"input": np.array([[text]])})

    return prediction[0], float(probability[0][prediction[0]])


class HealthController:
    def on_get(self, request: Request, response: Response):
        response.status = HTTP_OK


class ClassificationController:
    def on_post(self, request: Request, response: Response):
        body = RequestDTO().loads(request.bounded_stream.read())

        label, probability = classify_text(body["text"])

        response.status = HTTP_OK
        response.text = ResponseDTO().dumps(
            {"label": label, "probability": probability}, ensure_ascii=False
        )
