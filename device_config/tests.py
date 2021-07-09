from django.test import TestCase
from .models import DeviceConfig, Pill, PillForm
import json
from rest_framework import status


class TestFrontendConfigHandler(TestCase):

    def setUp(self) -> None:
        DeviceConfig.objects.create(
            id=1, device_id=1, passcode='1234', timezone_name='America/New_York', active=True
        )
        Pill.objects.create(
            id=1, device_id=1, slot=1, name="Vitamin C", dosage="200 mg", expires="2020-03-14", passcode_required=True, form=PillForm.Cap.value, exact_pill_count=10, max_manual_doses=4, active=True

        )
        self.updating_payload = {
            "passcode": "123456",
            "timezone_name": "America/New_York",
            "pills": [
                {
                    "slot": 1,
                    "name": "Vitamin C",
                    "dosage": "200 mg",
                    "expires": "2020-03-14",
                    "passcode_required": True,
                    "form": "Cap",
                    "exact_pill_count": 10,
                    "max_manual_doses": 4
                },
                {
                    "slot": 2,
                    "name": "Vitamin D",
                    "dosage": "150 mg",
                    "expires": "2020-03-14",
                    "passcode_required": True,
                    "form": "Cap",
                    "exact_pill_count": 10,
                    "max_manual_doses": 4
                }
            ]
        }
        self.non_updating_payload = {
            "passcode": "1234",
            "timezone_name": "America/New_York",
            "pills": [
                {
                    "slot": 1,
                    "name": "Vitamin C",
                    "dosage": "200 mg",
                    "expires": "2020-03-14",
                    "passcode_required": True,
                    "form": "Cap",
                    "exact_pill_count": 10,
                    "max_manual_doses": 4
                },
            ]
        }

    def test_no_changes_config(self):
        response = self.client.post(
            '/api/frontend-config/1',
            data=json.dumps(self.non_updating_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DeviceConfig.objects.filter(device_id=1, active=True).first().id, 1)
        self.assertEqual(Pill.objects.filter(device_id=1, active=True).first().id, 1)

    def test_save_new_config(self):
        response = self.client.post(
            '/api/frontend-config/1',
            data=json.dumps(self.updating_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DeviceConfig.objects.filter(device_id=1, active=True).first().id, 2)
        self.assertEqual(DeviceConfig.objects.filter(pk=1).first().active, False)
        self.assertEqual(Pill.objects.filter(device_id=1, active=True).first().id, 2)
        self.assertEqual(Pill.objects.filter(device_id=1, active=True).last().id, 3)
        self.assertEqual(Pill.objects.filter(pk=1).first().active, False)


class TestDeviceConfigHandler(TestCase):

    def setUp(self) -> None:
        DeviceConfig.objects.create(
            id=1, device_id=1, passcode='1234', timezone_name='America/New_York', active=True
        )
        Pill.objects.create(
            id=1, device_id=1, slot=1, name="Vitamin C", dosage="200 mg", expires="2020-03-14", passcode_required=True, form=PillForm.Cap.value, exact_pill_count=10, max_manual_doses=4, active=True

        )
        self.updating_payload = {
            "Table": {
                "device": {
                    "passcode": "12346",
                    "timezone_name": "America/New_York"
                },
                "consumables": [
                    {
                        "id": "id_1",
                        "name": "Vitamin C",
                        "expiration_date": "2020-03-14",
                        "dosage": "200 mg",
                        "passcode_mandatory": False,
                        "form": "Cap",
                        "max_doses": 4
                    },
                    {
                        "id": "id_2",
                        "name": "Vitamin D",
                        "dosage": "150 mg",
                        "expiration_date": "2020-03-14",
                        "passcode_mandatory": True,
                        "form": "Cap",
                        "max_doses": 4
                    }
                ],
                "slots": [
                    {
                        "slot_index": 1,
                        "consumable_id": "id_1",
                        "exact_pill_count": 20
                    },
                    {
                        "slot_index": 2,
                        "consumable_id": "id_2",
                        "exact_pill_count": 20
                    }
                ]
            }
        }
        self.non_updating_payload = {
            "Table": {
                "device": {
                    "passcode": "1234",
                    "timezone_name": "America/New_York"
                },
                "consumables": [
                    {
                        "id": "id_1",
                        "name": "Vitamin C",
                        "expiration_date": "2020-03-14",
                        "dosage": "200 mg",
                        "passcode_mandatory": True,
                        "form": "Cap",
                        "max_doses": 4
                    }
                ],
                "slots": [
                    {
                        "slot_index": 1,
                        "consumable_id": "id_1",
                        "exact_pill_count": 10
                    }
                ]
            }
        }

    def test_no_changes_config(self):
        response = self.client.post(
            '/api/device-config/1',
            data=json.dumps(self.non_updating_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DeviceConfig.objects.filter(device_id=1, active=True).first().id, 1)
        self.assertEqual(Pill.objects.filter(device_id=1, active=True).first().id, 1)

    def test_save_new_config(self):
        response = self.client.post(
            '/api/device-config/1',
            data=json.dumps(self.updating_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DeviceConfig.objects.filter(device_id=1, active=True).first().id, 2)
        self.assertEqual(DeviceConfig.objects.filter(pk=1).first().active, False)
        self.assertEqual(Pill.objects.filter(device_id=1, active=True).first().id, 2)
        self.assertEqual(Pill.objects.filter(device_id=1, active=True).last().id, 3)
        self.assertEqual(Pill.objects.filter(pk=1).first().active, False)
