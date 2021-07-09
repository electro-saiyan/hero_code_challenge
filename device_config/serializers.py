from rest_framework import serializers
from .models import Pill, DeviceConfig


class PillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        fields = [
            'device_id',
            'name',
            'dosage',
            'form',
            'exact_pill_count',
            'max_manual_doses',
            'passcode_required',
            'expires',
            'slot'
        ]


class DeviceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConfig
        fields = ['device_id', 'passcode', 'timezone_name']
