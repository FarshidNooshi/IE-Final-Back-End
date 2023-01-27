import time

from celery import Celery

app = Celery()


# run bellow function as a single thread
def check_webpage(data):
    now_time = time.time()
    while time.time() < now_time + 1800 * 20:
        print("hello")
        from FinalApp.models import Webpage
        webpage = Webpage.objects.filter(id=data).first()
        print(data)
        webpage.check_status()
        webpage.save()
        print("@" * 100)
        time.sleep(30)
    return True
