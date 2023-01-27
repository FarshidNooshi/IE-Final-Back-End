import time

from celery import Celery

SLEEP_TIME = 3  # in seconds
REPEAT_COUNT = 10

app = Celery()


# run bellow function as a single thread
def check_webpage(data):
    now_time = time.time()
    while time.time() < now_time + SLEEP_TIME * REPEAT_COUNT:
        print('something!')
        from FinalApp.models import Webpage
        webpage = Webpage.objects.filter(id=data).first()
        webpage.check_status()
        webpage.save()
        time.sleep(SLEEP_TIME)
    return True
