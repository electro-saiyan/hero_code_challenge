import enum

from django.db import models

# Create your models here.


class DeviceConfig(models.Model):
    device_id = models.IntegerField()
    passcode = models.CharField(max_length=10)
    timezone_name = models.CharField(max_length=25)  # TODO use timezone type?
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PillForm(enum.Enum):
    Cap = "Cap"


class Pill(models.Model):
    device_id = models.IntegerField()
    name = models.CharField(max_length=25)
    dosage = models.CharField(max_length=10)
    form = models.CharField(max_length=10, choices=[(pf.name, pf.value) for pf in PillForm])
    exact_pill_count = models.SmallIntegerField()
    max_manual_doses = models.SmallIntegerField()
    passcode_required = models.BooleanField()
    expires = models.DateField()
    slot = models.SmallIntegerField()
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
