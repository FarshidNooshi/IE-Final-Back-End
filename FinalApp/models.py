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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
            print("webpage status code: ", response.status_code)
        except requests.exceptions.RequestException as e:
            Result.objects.create(webpage=self, status_code=0, response_time=0, response=e)
            return False
        if response.status_code // 100 == 2:
            Result.objects.create(webpage=self, status_code=response.status_code, date=timezone.now(),
                                  response=response.text)
            return True
        else:
            Result.objects.create(webpage=self, status_code=response.status_code, date=timezone.now(),
                                  response=response.text)
            # get the number of errors of the last 24 hours
            errors = Result.objects.filter(webpage=self, date__gte=timezone.now() - timezone.timedelta(days=1),
                                           status_code__gte=400).count()
            if errors >= self.max_error:
                self.active = False
                Alarm.objects.create(webpage=self,
                                     message=f"Webpage {self.name} has been deactivated because it has {errors} errors in the last 24 hours",
                                     user=self.user,
                                     time=timezone.now(),
                                     name=f"Webpage {self.name} deactivated",
                                     active=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms')
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    time = models.TimeField()
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
