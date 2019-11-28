from django.db import models
import datetime

# Create your models here.

class Host(models.Model):
    host_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)


class Meeting(models.Model):
    meeting_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)


class Guest(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_phone = models.IntegerField()
    guest_mail = models.EmailField(max_length=100)
    checked_in = models.BooleanField(default=True)
    check_in_time = models.DateTimeField(default=datetime.datetime.now())
    checked_out_time = models.DateTimeField(blank=True, null=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    token = models.IntegerField()
