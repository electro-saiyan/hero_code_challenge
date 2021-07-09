from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pill, DeviceConfig
from .serializers import PillSerializer, DeviceConfigSerializer


def consumables_to_pills(data):
    pills = []
    for slot in data['Table']['slots']:
        pill = next(item for item in data['Table']['consumables'] if item['id'] == slot['consumable_id'])
        pill['passcode_required'] = pill.pop('passcode_mandatory')
        pill['expires'] = pill.pop('expiration_date')
        pill['max_manual_doses'] = pill.pop('max_doses')

        pill['exact_pill_count'] = slot['exact_pill_count']
        pill['slot'] = slot['slot_index']

        pills.append(pill)
    for pill in pills:
        pill.pop('id')
    return pills


def create_device_config(data, device_id):
    return DeviceConfig(
        device_id=device_id,
        passcode=data['passcode'],
        timezone_name=data['timezone_name'],
        active=True
    )


def create_pills(pills, device_id):
    return [Pill(device_id=device_id, active=True, **pill) for pill in pills]


class BaseConfigHandler(APIView):

    def _get_existing_data(self):
        self.pills = Pill.objects.all().filter(device_id=self.device_id, active=True)
        self.pills_serializer = PillSerializer(self.pills, many=True)
        self.device_config = DeviceConfig.objects.filter(device_id=self.device_id, active=True).first()
        self.device_config_serializer = DeviceConfigSerializer(self.device_config, many=False)

    def _save_new_data(self):
        if self.new_config_serializer.data != self.device_config_serializer.data:
            if self.device_config:
                self.device_config.active = False
                self.device_config.save()
            self.new_config.save()

        if self.new_pills_serializer.data != self.pills_serializer.data:
            if self.pills_serializer.data:
                for pill in self.pills:
                    pill.active = False
                    pill.save()
            for new_pill in self.new_pills:
                new_pill.save()
        return None


class FrontendConfigHandler(BaseConfigHandler):

    def get(self, request, device_id):
        pills = Pill.objects.filter(device_id=device_id, active=True)
        pills_ser = PillSerializer(pills, many=True)
        device_config = get_object_or_404(DeviceConfig, device_id=device_id, active=True)

        return Response(
            {
                "device_id": device_config.device_id,
                "passcode": device_config.passcode,
                "timezone_name": device_config.timezone_name,
                "pills": [p for p in pills_ser.data]

            }
        )

    def post(self, request, device_id):
        self.data = request.data
        self.device_id = device_id

        self._get_existing_data()

        self.new_config = create_device_config(self.data, self.device_id)
        self.new_config_serializer = DeviceConfigSerializer(self.new_config)
        self.new_pills = create_pills(self.data['pills'], self.device_id)
        self.new_pills_serializer = PillSerializer(self.new_pills, many=True)

        self._save_new_data()

        return Response()


class DeviceConfigHandler(BaseConfigHandler):

    def post(self, request, device_id):
        data = request.data
        self.device_id = device_id

        self._get_existing_data()

        self.new_config = create_device_config(data['Table']['device'], device_id)
        self.new_config_serializer = DeviceConfigSerializer(self.new_config)
        new_pills_data = consumables_to_pills(data)
        self.new_pills = create_pills(new_pills_data, device_id)
        self.new_pills_serializer = PillSerializer(self.new_pills, many=True)

        self._save_new_data()

        return Response()
