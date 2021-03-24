import threading
import time

from schedule import Scheduler

from api.external import GoogleYoutubeAPI
from api.models import YoutubeData


def add_yt_data():
    api_obj = GoogleYoutubeAPI()
    api_data = api_obj.fetch_data()
    model_objects = []
    for api_data_point in api_data:
        model_objects.append(
            YoutubeData(
                title=api_data_point["title"],
                description=api_data_point["description"],
                published_on=api_data_point["publishedAt"],
                thumnail_urls=api_data_point["thumbnails"],
                channel_title=api_data_point["channelTitle"],
            )
        )
    YoutubeData.objects.bulk_create(model_objects)
    print("added data")


def run_continuously(self, interval=10000):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(add_yt_data)
    scheduler.run_continuously()
