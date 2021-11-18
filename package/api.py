import json

from falcon import (
    HTTP_NO_CONTENT,
    HTTP_OK,
    HTTPBadRequest,
    HTTPInternalServerError,
    Request,
    Response,
)
from falcon.status_codes import HTTP_INTERNAL_SERVER_ERROR
from marshmallow import ValidationError

from package.classification import classify_text
from package.dtos import RequestDTO, ResponseDTO
from package.logging import Logger

LOGGER = Logger(__name__)


class HealthController:
    def on_get(self, request: Request, response: Response):
        """Handle GET request.

        Parameters
        ----------
        request : Request
            A client's HTTP request.
        response : Response
            The HTTP response to a client request.
        """
        try:
            # classify example text
            prediction = classify_text("Die Sopranos ist eine US-amerikanische Fernsehserie")

            # make sure correct label is predicted
            if prediction["label"] == "show":
                response.status = HTTP_NO_CONTENT
            else:
                response.media = {"error": "Health check failed."}
                response.status = HTTP_INTERNAL_SERVER_ERROR
        except Exception as error:
            LOGGER.error(error)
            raise HTTPInternalServerError(description="Unfortunately, an internal error occurred.")


class ClassificationController:
    def on_post(self, request: Request, response: Response):
        """Handle POST request.

        Parameters
        ----------
        request : Request
            A client's HTTP request.
        response : Response
            The HTTP response to a client request.
        """
        try:
            try:
                # load and validate request body
                body = RequestDTO().loads(request.bounded_stream.read())
            except ValidationError as error:
                LOGGER.error(error.messages)
                raise HTTPBadRequest(description=json.dumps(error.messages, sort_keys=True))

            # classify the given text
            prediction = classify_text(body["text"])

            # send response
            response.status = HTTP_OK
            response.text = ResponseDTO().dumps(prediction, ensure_ascii=False)
        except Exception as error:
            LOGGER.error(error)
            raise HTTPInternalServerError(description="Unfortunately, an internal error occurred.")
