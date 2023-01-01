import sys
import smbus
import time
import datetime


# CONSTANTS
ACCESS_DELAY_TIME = 0.3
SLEEP_TIME_SECONDS = 5

#  I2C ADDRESS for SHT31-D
SHT31D_ADDRESS = 0x44

class mySHT31d:
    def  __init__(self, address = SHT31D_ADDRESS):
        self._address = address
        self._bus = smbus.SMBus(1)

        self.temperature = 0.0
        self.humidity = 0.0
        self.scanDateTime = datetime.datetime.now()

        self._bus.write_byte_data(self._address, 0x21, 0x30)
        time.sleep(ACCESS_DELAY_TIME)
        self.readData()

    def convertTemperature(self, msb, lsb):
        mlsb = ((msb << 8) | lsb)                                  
        return (-45 + 175 * int(str(mlsb), 10) / (pow(2, 16) - 1))

    def convertHumidity(self, msb, lsb):
        mlsb = ((msb << 8) | lsb)
        return (100 * int(str(mlsb), 10) / (pow(2, 16) - 1))

    def readData(self):
        time.sleep(ACCESS_DELAY_TIME)
        self._bus.write_byte_data(self._address, 0xE0, 0x00)               
        data = self._bus.read_i2c_block_data(self._address, 0x00, 6)
        self.temperature = self.convertTemperature(data[0], data[1])
        self.humidity = self.convertHumidity(data[3], data[4])
        self.scanDateTime = datetime.datetime.now()

    def getScanDateTime(self):
        return self.scanDateTime

    def getTemperature(self):
        return float(self.temperature)

    def getHumidity(self):
        return float(self.humidity)


def getData():
    sensor = mySHT31d()
    current = sensor.getScanDateTime()
    tm = current.isoformat()
    return ("%s,%6.2f,%6.2f,;" % (tm, sensor.getTemperature(), sensor.getHumidity())) 

if __name__ == '__main__':
    sensor = mySHT31d()
    try:
        loopCount = 10
        while loopCount > 0:
            currentDateTime = sensor.getScanDateTime()
            print("date time   : %s" % currentDateTime.strftime('%Y–%m–%d %H:%M:%S'))
            print("Temperature:%6.2f ℃  Humidity.:%6.2f %%" % (sensor.getTemperature(), sensor.getHumidity())) 
            #print(getData())

            loopCount = loopCount - 1
            time.sleep(SLEEP_TIME_SECONDS)
            print(" ")
            sensor.readData()

    except KeyboardInterrupt:
        pass

