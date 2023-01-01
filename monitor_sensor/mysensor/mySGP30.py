from sgp30 import SGP30
import sys
import time
import datetime

# CONSTANTS
ACCESS_DELAY_TIME = 0.3
SLEEP_TIME_SECONDS = 5

#  I2C ADDRESS for SGP30
SGP30_ADDRESS = 0x58

class mySGP30:
    def  __init__(self, address = SGP30_ADDRESS):
        self.sensor = SGP30(i2c_addr = address)
        self.sensor.start_measurement()
        self.readData()

    def getScanDateTime(self):
        return self.current

    def readData(self):
        self.current = datetime.datetime.now()
        self.eco2, self.tvoc = self.sensor.command('measure_air_quality')

    def geteCO2(self):
        return (self.eco2)

    def getTVOC(self):
        return (self.tvoc)

if __name__ == '__main__':
    sensor = mySGP30()
    try:
        loopCount = 10
        while loopCount > 0:
            currentDateTime = sensor.getScanDateTime()
            print("date time   : %s" % currentDateTime.strftime('%Y–%m–%d %H:%M:%S'))
            print("eCO2:%5d ppm  VOC:%5d ppb" % (sensor.geteCO2(), sensor.getTVOC())) 
            #print(getData())

            loopCount = loopCount - 1
            time.sleep(SLEEP_TIME_SECONDS)
            print(" ")
            sensor.readData()

    except KeyboardInterrupt:
        pass
