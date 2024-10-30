from falcon import (
    HTTP_OK,
    Request,
    Response,
)

from app.classification import classify_text
from app.logging import Logger

LOGGER = Logger(__name__)


class HealthResource:
    """Resource for the health endpoint."""

    def on_post(self, request: Request, response: Response):
        """Handle POST requests.

        Parameters
        ----------
        request : Request
            A client's HTTP request.
        response : Response
            The HTTP response to a client request.
        """
        LOGGER.info("Health check has started")

        classify_text("Die Sopranos ist eine US-amerikanische Fernsehserie.")
        response.status = HTTP_OK

        LOGGER.info("Health check has been completed")
