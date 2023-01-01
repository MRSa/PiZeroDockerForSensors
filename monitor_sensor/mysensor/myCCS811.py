import sys
import smbus
import time
import datetime


##  reboot and issue command 'i2cset -y 1 0x5A 0xF4'  to start measure.

#  CONSTANTS
ACCESS_DELAY_TIME = 0.25
SLEEP_TIME_5SECONDS = 5
SLEEP_TIME_2SECONDS = 2
SLEEP_TIME_SECONDS = 1

#  I2C ADDRESS for CCS811
CCS811_ADDRESS = 0x5a

#  CCS811 REGISTERS
CCS811_REGISTER_STATUS = 0x00
CCS811_REGISTER_MEAS_MODE = 0x01
CCS811_REGISTER_HW_ID = 0x20
CCS811_REGISTER_FW_VER = 0x21
CCS811_REGISTER_START  = 0xF4
CCS811_REGISTER_RESULT = 0x02
CCS811_REGISTER_ERRID = 0xe0

### MEASURE MODE
CCS811_DRIVE_MODE_1SEC = 0x10
CCS811_DRIVE_MODE_10SEC = 0x20
CCS811_DRIVE_MODE_60SEC = 0x30

#  CCS811 HARDWARE ID
CCS811_HW_ID = 0x81

class myCCS811:
    def __init__(self, mode = CCS811_DRIVE_MODE_1SEC, address = CCS811_ADDRESS):
        self._address = address
        self._bus = smbus.SMBus(1)
        self._measure_mode = 0

        self.eco2 = 0
        self.tvoc = 0
        self.dataStatus = 0
        self.dataErrorId = 0
        self.dataRaw = 0
        self.scanDateTime = datetime.datetime.now()

        ## software reset
        self._bus.write_block_data(self._address, 0xff, [0x11, 0xe5, 0x72, 0x8a])

        time.sleep(ACCESS_DELAY_TIME)
        hwId = self.readU8(CCS811_REGISTER_HW_ID) 
        if hwId != CCS811_HW_ID:
           print('HW ID:' + str(hwId), file=sys.stderr)
           raise Exception(" CCS811 HW ID is not correct!")

        fwVer = self.readU8(CCS811_REGISTER_FW_VER)
        print("CCS811 HW-ID: 0x%x FW-VER : 0x%x" % (hwId, fwVer), file=sys.stderr)
        self.readRegisterStatus("START")

        ### start sampling
        self._bus.write_block_data(self._address, 0xF4, [])
        self.readRegisterStatus("(start)")
        print(" - - - - - - - -", file=sys.stderr)

        ### ...set measure mode...
        self._bus.write_byte_data(self._address, 0x01, 0x18)   # set drive mode

        ### read Data
        self.readData()

    def readRegisterStatus(self, appendInfo = ""):
        time.sleep(ACCESS_DELAY_TIME)
        status0 = self._bus.read_byte_data(self._address, 0x00)  # self.readU8(CCS811_REGISTER_STATUS)
        errId0 = 0
        #if status0 & 0x01:
        #    time.sleep(ACCESS_DELAY_TIME)
        #    errId0 = self.readU8(CCS811_REGISTER_ERRID)
        errId0 = self.readU8(CCS811_REGISTER_ERRID)
        print("CCS811 STATUS(0x%x) ERRORID : 0x%x %s" % (status0, errId0, appendInfo), file=sys.stderr)
        time.sleep(ACCESS_DELAY_TIME)

    def write8(self, register, value):
        time.sleep(ACCESS_DELAY_TIME)
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value) 

    def readU8(self, register):
        time.sleep(ACCESS_DELAY_TIME)
        result = self._bus.read_byte_data(self._address, register) & 0xFF
        return result

    def readData(self):
        # wait for Data ready
        waitData = self.readU8(0x00)
        while (waitData & 0x08) == 0:
            print(" STATUS CHANGE WAIT: 0x%x " % (waitData))
            waitData = self.readU8(0x00)
            time.sleep(SLEEP_TIME_SECONDS)

        # read data
        time.sleep(ACCESS_DELAY_TIME)
        currentValue = self._bus.read_i2c_block_data(self._address, CCS811_REGISTER_RESULT,8) 
        self.scanDateTime = datetime.datetime.now()

        self.eco2 = 0
        self.tvoc = 0
        self.dataStatus = 0 
        self.dataErrorId = 0
        self.dataRaw = 0
        self.eco2 = currentValue[0] << 8 | currentValue[1]
        self.tvoc = currentValue[2] << 8 | currentValue[3]
        self.dataStatus = currentValue[4]
        self.dataErrorId = currentValue[5]
        self.dataRaw = currentValue[6] << 8 | currentValue[7]

    def getScanDateTime(self):
        return self.scanDateTime

    def getECO2(self):
        return self.eco2

    def getTVOC(self):
        return self.tvoc

    def getDataStatus(self):
        return self.dataStatus

    def getDataErrorId(self):
        return self.dataErrorId

    def getDataRaw(self):
        return self.dataRaw

def getData():
    sensor = myCCS811()
    sensor.readData()
    tm = sensor.getScanDateTime().isoformat()
    return ("%s,%d,%d,0x%02x,0x%02x,0x%04x,;" % (tm, sensor.getECO2(), sensor.getTVOC(), sensor.getDataStatus(), sensor.getDataErrorId(), sensor.getDataRaw())) 

if __name__ == '__main__':
    sensor = myCCS811()
    try:
        loopCount = 10
        sensor.readData()
        while loopCount > 0:
            print("date time   : %s" % sensor.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
            print("eCO2:%d  TVOC:%d  status:0x%02x errId:0x%02x Raw:0x%04x" % (sensor.getECO2(), sensor.getTVOC(), sensor.getDataStatus(), sensor.getDataErrorId(), sensor.getDataRaw())) 
            #print(getData())

            loopCount = loopCount - 1
            time.sleep(SLEEP_TIME_SECONDS)
            print(" ")
            sensor.readData()

    except KeyboardInterrupt:
        pass

