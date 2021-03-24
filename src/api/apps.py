import os
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        from api import jobs
        from api.external import APIKeyHelper

        if os.environ.get("RUN_MAIN", None) != "true":
            APIKeyHelper.set_initial_key()
            jobs.start_scheduler()
