from falcon import MEDIA_JSON
from falcon import App as _App

from app.api.resources import ClassificationResource, HealthResource
from app.api.utils import handle_error


class App(_App):
    """App to handle HTTP requests."""

    def __init__(self):
        super().__init__(media_type=MEDIA_JSON)

        # global error handler to delegate respective http status codes
        self.add_error_handler(Exception, handle_error)

        # endpoints
        self.add_route("/health", HealthResource())
        self.add_route("/v1/classification", ClassificationResource())


def create_app() -> App:
    """Create a new instance of the App.

    Returns
    -------
    App
        A new instance of the App.
    """
    return App()
