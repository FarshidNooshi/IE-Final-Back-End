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
    name = models.CharField(max_length=50, default="")
    active = models.BooleanField(default=True)
    max_error = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class Result(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    error = models.IntegerField(default=0)
    response = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.webpage.name + " " + str(self.date)


class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    time = models.TimeField()
    days = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
