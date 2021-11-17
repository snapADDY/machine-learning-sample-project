from falcon import App

from classification.api import ClassificationController

application = App()
application.add_route("/classification", ClassificationController())
