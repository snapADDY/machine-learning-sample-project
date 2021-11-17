from falcon import App

from package.api import ClassificationController

application = App()
application.add_route("/classification", ClassificationController())
