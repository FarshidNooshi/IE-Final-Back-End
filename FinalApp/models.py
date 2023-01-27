from django.db import models


# Create your models here.

class Config(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ExpiredToken(models.Model):
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Webpage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webpages')
    url = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    max_error = models.IntegerField(default=20)

    def __str__(self):
        return self.url + " " + self.user.username

    def check_status(self):
        import requests
        from FinalApp.models import Result
        from django.utils import timezone
        try:
            response = requests.get(self.url, timeout=30, allow_redirects=True)
            Result.objects.create(webpage=self, status_code=response.status_code, response=response.text,
                                  date=timezone.now())
        except requests.exceptions.RequestException as e:
            Result.objects.create(webpage=self, status_code=400, response=e, date=timezone.now())
            errors = Result.objects.filter(webpage=self, date__gte=timezone.now() - timezone.timedelta(days=1),
                                           status_code__gte=300).count()
            if errors >= self.max_error:
                self.active = False
                Alarm.objects.create(webpage=self, time=timezone.now(), message="Too many errors"
                                     , active=True)
                self.save()
            return False
        if response.status_code // 100 == 2:
            return True
        else:
            errors = Result.objects.filter(webpage=self, date__gte=timezone.now() - timezone.timedelta(days=1),
                                           status_code__gte=300).count()
            if errors >= self.max_error:
                self.active = False
                Alarm.objects.create(webpage=self, time=timezone.now(), message="Too many errors", active=True)
                self.save()
            return False


class Result(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE, related_name='results')
    date = models.DateTimeField(auto_now_add=True)
    error = models.IntegerField(default=0)
    response = models.CharField(max_length=1000, default="")
    status_code = models.IntegerField(default=0)

    def __str__(self):
        return self.webpage.name + " " + str(self.date)


class Alarm(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE, null=True, blank=True, related_name='alarms')
    time = models.TimeField()
    active = models.BooleanField(default=True)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
