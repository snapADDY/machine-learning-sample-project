from falcon import App

from package.api import ClassificationController, HealthController

application = App()
application.add_route("/health", HealthController())
application.add_route("/classification", ClassificationController())
