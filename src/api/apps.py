import os
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        print("inside app")
        from . import jobs

        if os.environ.get("RUN_MAIN", None) != "true":
            jobs.start_scheduler()
