# from gpiozero import MCP3008
import random


class MoistureController:
    def __init__(self, channel):
        # self.sensor = MCP3008(channel=channel)

        # the absolute values for dry and wet recorded from the sensor
        self.absolute_dry = 0.7498778700537372
        self.absolute_wet = 0.3082559843673669

        self.interval = self.absolute_dry - self.absolute_wet

    def get_moisture(self):
        return 0.5
        # return self.sensor.value

    def get_moisture_percentage(self):
        return random.randint(0, 100)
        # return round(1 - (self.get_moisture() - self.absolute_wet) / self.interval, 2) * 100
