from cProfile import Profile

from app.api.resources import ClassificationResource


class RequestMock:
    """Mock for the request object."""

    def get_media(self) -> dict[str, str]:
        """Mock for the `get_media` method."""
        return {"text": "Die Sopranos ist eine US-amerikanische Fernsehserie"}


class ResponseMock:
    """Mock for the response object."""


if __name__ == "__main__":
    # set up profiler
    profiler = Profile()

    # set up controller
    controller = ClassificationResource()

    # mock request and response
    request = RequestMock()
    response = ResponseMock()

    # fire!
    profiler.enable()
    controller.on_post(request, response)
    profiler.disable()

    # dump stats
    profiler.dump_stats("request.prof")
