#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bme680
import time
import datetime

class myBME680:
    def __init__(self, busNumber=1):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)
        self.current = datetime.datetime.now()
        self.sensor.get_sensor_data()

    def getScanDateTime(self):
        return self.current

    def getPressure(self):
        try:
            return self.sensor.data.pressure
        except:
            return 0.0

    def getTemperature(self):
        try:
            return self.sensor.data.temperature
        except:
            return 0.0

    def getHumidity(self):
        try:
            return self.sensor.data.humidity
        except:
            return 0.0

    def getGasRegistance(self):
        try:
            if self.sensor.data.heat_stable:
                return self.sensor.data.gas_resistance
            return 0.0
        except:
            return 0.0

    def readData(self):
        mySensor.sensor.get_sensor_data()

# ---------------------------------------------
if __name__ == '__main__':
    mySensor = myBME680()
    try:
        loopCount = 10
        while loopCount > 0: 
            if mySensor.sensor.get_sensor_data():
                print("date time      : %s" % mySensor.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
                print("temperature    :  %-6.2f ℃" % mySensor.getTemperature())
                print("pressure       : %7.2f hPa" % mySensor.getPressure())
                print("humidity       : %6.2f ％" % mySensor.getHumidity())
                if mySensor.sensor.data.heat_stable:
                    print("gas registance : %6.2f" % mySensor.getGasRegistance())
                loopCount = loopCount - 1
                time.sleep(5)
                print(" ")

    except KeyboardInterrupt:
        pass
