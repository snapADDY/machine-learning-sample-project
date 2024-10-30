from falcon import (
    HTTP_OK,
    Request,
    Response,
)
from marshmallow import EXCLUDE

from package.api.dtos import PostClassificationRequestDTO, PostClassificationResponseDTO
from package.classification import classify_text
from package.logging import Logger

LOGGER = Logger(__name__)


class ClassificationResource:
    """Resource for the classification endpoint."""

    def on_post(self, request: Request, response: Response):
        """Handle POST requests.

        Parameters
        ----------
        request : Request
            A client's HTTP request.
        response : Response
            The HTTP response to a client request.
        """
        LOGGER.info("Request has started")
        body = PostClassificationRequestDTO().load(request.get_media(), unknown=EXCLUDE)

        prediction = classify_text(body["text"])

        response.status = HTTP_OK
        response.media = PostClassificationResponseDTO().dump(prediction)
        LOGGER.info("Request has been completed")
