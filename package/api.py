import json

from falcon import (
    HTTP_OK,
    HTTPBadRequest,
    HTTPInternalServerError,
    Request,
    Response,
)
from marshmallow import ValidationError

from package.classification import classify_text
from package.dtos import RequestDTO, ResponseDTO
from package.logging import Logger

LOGGER = Logger(__name__)


class ClassificationResource:
    """Classification resource."""

    def on_post(self, request: Request, response: Response):
        """Handle POST request.

        Parameters
        ----------
        request : Request
            A client's HTTP request.
        response : Response
            The HTTP response to a client request.
        """
        LOGGER.info("Incoming request")

        try:
            try:
                # load and validate request body
                body = RequestDTO().loads(request.bounded_stream.read())
            except ValidationError as error:
                LOGGER.error(error.messages)
                raise HTTPBadRequest(
                    description=json.dumps(error.messages, sort_keys=True)
                ) from error

            LOGGER.info("Classifying text")
            prediction = classify_text(body["text"])
            LOGGER.info("Done with classification")

            # send response
            response.status = HTTP_OK
            response.text = ResponseDTO().dumps(prediction, sort_keys=True)
            LOGGER.info("Sent response")
        except Exception as error:
            LOGGER.error(error)
            raise HTTPInternalServerError(
                description="Unfortunately, an internal error occurred."
            ) from error
