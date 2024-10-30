from typing import Any

from falcon import HTTPBadRequest, HTTPError, HTTPInternalServerError, Request, Response
from marshmallow import ValidationError

from app.logging import Logger

LOGGER = Logger(__name__)


def handle_error(
    request: Request,
    response: Response,
    exception: Exception,
    params: dict[str, Any],
):
    """Handle generic errors.

    Parameters
    ----------
    exception : Exception
        Exception raised anywhere in the code.
    """
    if isinstance(exception, ValidationError):
        raise HTTPBadRequest(title="Validation error", description=exception.normalized_messages())

    if not isinstance(exception, HTTPError):
        LOGGER.error(exception)
        raise HTTPInternalServerError(
            title="Internal server error",
            description="An unexpected error occurred :(",
        )

    raise exception
