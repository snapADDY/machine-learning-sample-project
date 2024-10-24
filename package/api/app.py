from falcon import MEDIA_JSON, App

from package.api.resources import ClassificationResource, HealthResource
from package.api.utils import handle_error


class Application(App):
    """Application to handle HTTP requests."""

    def __init__(self):
        super().__init__(media_type=MEDIA_JSON)

        # global error handler to delegate respective http status codes
        self.add_error_handler(Exception, handle_error)

        # endpoints
        self.add_route("/health", HealthResource())
        self.add_route("/v1/classification", ClassificationResource())
