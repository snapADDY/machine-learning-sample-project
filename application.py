from falcon import App

from package.api import ClassificationResource

application = App()
application.add_route("/classification", ClassificationResource())
