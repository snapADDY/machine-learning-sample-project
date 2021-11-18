import json
from cProfile import Profile

from package.api import ClassificationController


class BoundedStreamMock:
    def read(self) -> dict[str, str]:
        return json.dumps({"text": "Die Sopranos ist eine US-amerikanische Fernsehserie"})


class RequestMock:
    bounded_stream = BoundedStreamMock()


class ResponseMock:
    pass


if __name__ == "__main__":
    # set up profiler
    profiler = Profile()

    # set up controller
    controller = ClassificationController()

    # mock request and response
    request = RequestMock()
    response = ResponseMock()

    # fire!
    profiler.enable()
    controller.on_post(request, response)
    profiler.disable()

    # dump stats
    profiler.dump_stats("request.prof")
