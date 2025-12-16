import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupied(self, sensor: Mock):
        sensor.return_value=True
        smart_room = SmartRoom()
        room_occupancy=smart_room.check_room_occupancy()
        self.assertTrue(room_occupancy)

    @patch.object(GPIO, "input")
    def test_check_room_not_occupied(self, sensor: Mock):
        sensor.return_value=False
        smart_room = SmartRoom()
        room_occupancy=smart_room.check_room_occupancy()
        self.assertFalse(room_occupancy)

    @patch.object(GPIO, "input")
    def test_enough_light(self, photoresistor: Mock):
        photoresistor.return_value=True
        smart_room = SmartRoom()
        enough_light=smart_room.check_enough_light()
        self.assertTrue(enough_light)

    @patch.object(GPIO, "input")
    def test_not_enough_light(self, photoresistor: Mock):
        photoresistor.return_value = False
        smart_room = SmartRoom()
        enough_light = smart_room.check_enough_light()
        self.assertFalse(enough_light)

    @patch.object(GPIO, "input")
    @patch.object(GPIO, "input")
    @patch.object(GPIO, "output")
    def test_turn_on_light_when_room_occupied_and_not_enough_light(self,
                                                                   light_bulb: Mock,photoresistor: Mock,sensor: Mock):
        sensor.return_value=True
        photoresistor.return_value=False
        smart_room = SmartRoom()
        smart_room.light_on=False
        smart_room.manage_light_level()
        self.assertTrue(smart_room.light_on)