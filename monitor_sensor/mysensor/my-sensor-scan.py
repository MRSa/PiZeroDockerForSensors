#!/usr/bin/python3
# -*- coding: utf-8 -*-

import redis
import myBME280
import mySHT31d
import myCCS811
import myBME680
import mySGP30
import time

# ---------- settings for Redis
REDIS_HOST_PORT = 6379
REDIS_HOST_ADDRESS = 'redis'
REDIS_DB_NUMBER = 0 

# ---------- dataid for BME280
DATAID_BME280_TEMPERATURE = "ts:bme280temperature"
DATAID_BME280_PRESSURE = "ts:bme280pressure"
DATAID_BME280_HUMIDITY = "ts:bme280humidity"

# ---------- dataid for SHT31d
DATAID_SHT31D_TEMPERATURE = "ts:sht31temperature"
DATAID_SHT31D_HUMIDITY = "ts:sht31humidity"

# ---------- dataid for CCS811
DATAID_CCS811_ECO2 = "ts:ccs811eco2"
DATAID_CCS811_TVOC = "ts:ccs811tvoc"

# ---------- dataid for SGP30
DATAID_SGP30_ECO2 = "ts:sgp30eco2"
DATAID_SGP30_TVOC = "ts:sgp30tvoc"

# ---------- dataId for BME680/BME688
DATAID_BME680_TEMPERATURE    = "ts:bme680temperature"
DATAID_BME680_PRESSURE       = "ts:bme680pressure"
DATAID_BME680_HUMIDITY       = "ts:bme680humidity"
DATAID_BME680_GAS_RESISTANCE = "ts:bme680gasresistance"

# ---------- COLLECTION INTERVAL TIME (Unit: Seconds)
SENSING_INTERVAL_SEC = 300
#SENSING_INTERVAL_SEC = 3


def showCurrentData():
    bme280 = myBME280.myBME280()
    sht31d = mySHT31d.mySHT31d()
    ccs811 = myCCS811.myCCS811()
    bme680 = myBME680.myBME680()
    sgp30  = mySGP30.mySGP30()

    loopCount = 10
    while loopCount > 0:
        try:
            print(" - - - - - - - - - - - - - - - - -")
            bme280.readData()
            print("[BME280]date time      : %s" % bme280.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
            print("[BME280]temperature    : %-6.2f ℃" % bme280.getTemperature())
            print("[BME280]pressure       : %7.2f hPa" % bme280.getPressure())
            print("[BME280]humidity       : %6.2f ％" % bme280.getHumidity())

            print(" - - - - - - - - - - - - - - - - -")
            bme680.readData()
            print("[BME680]date time      : %s" % bme680.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
            print("[BME680]temperature    : %-6.2f ℃" % bme680.getTemperature())
            print("[BME680]pressure       : %7.2f hPa" % bme680.getPressure())
            print("[BME680]humidity       : %6.2f ％" % bme680.getHumidity())
            print("[BME680]gas registance : %9.2f" % bme680.getGasRegistance())

            print(" - - - - - - - - - - - - - - - - -")
            sht31d.readData()
            print("[SHT31d]date time      : %s" % sht31d.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
            print("[SHT31d]temperature    : %-6.2f ℃" % sht31d.getTemperature())
            print("[SHT31d]humidity       : %6.2f ％" % sht31d.getHumidity())

            print(" - - - - - - - - - - - - - - - - -")
            sgp30.readData()
            print("[SGP30 ]date time      : %s" % sgp30.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
            print("[SGP30 ]eCO2           : %d ppm" % sgp30.geteCO2())
            print("[SGP30 ]TVOC           : %d ppb" % sgp30.getTVOC())

            print(" - - - - - - - - - - - - - - - - -")
            ccs811.readData()
            print("[CCS811]date time      : %s" % ccs811.getScanDateTime().strftime('%Y–%m–%d %H:%M:%S'))
            print("[CCS811]eCO2           : %d ppm" % ccs811.getECO2())
            print("[CCS811]TVOC           : %d ppb" % ccs811.getTVOC())

            loopCount = loopCount - 1
            time.sleep(5)
            print(" ")
        except:
            print(" ")

# -------------------
redis_obj = redis.Redis(host=REDIS_HOST_ADDRESS, port=REDIS_HOST_PORT, db=REDIS_DB_NUMBER)

# -------------------
if __name__ == '__main__':
    bme280 = myBME280.myBME280()
    sht31d = mySHT31d.mySHT31d()
    ccs811 = myCCS811.myCCS811()
    bme680 = myBME680.myBME680()
    sgp30  = mySGP30.mySGP30()

    print('\n\nPolling:')
    try:
        pipe = redis_obj.pipeline()
        while True:
            try:
                # ----- BME280
                bme280.readData()
                timestamp1 = int(bme280.getScanDateTime().timestamp() * 1000)
                pipe.execute_command("ts.add", DATAID_BME280_TEMPERATURE, timestamp1, bme280.getTemperature())
                pipe.execute_command("ts.add", DATAID_BME280_PRESSURE, timestamp1, bme280.getPressure())
                pipe.execute_command("ts.add", DATAID_BME280_HUMIDITY, timestamp1, bme280.getHumidity())

                # ----- SHT31D
                sht31d.readData()
                timestamp2 = int(sht31d.getScanDateTime().timestamp() * 1000)
                pipe.execute_command("ts.add", DATAID_SHT31D_TEMPERATURE, timestamp2, sht31d.getTemperature())
                pipe.execute_command("ts.add", DATAID_SHT31D_HUMIDITY, timestamp2, sht31d.getHumidity())

                # ----- CCS811
                ccs811.readData()
                timestamp3 = int(ccs811.getScanDateTime().timestamp() * 1000)
                pipe.execute_command("ts.add", DATAID_CCS811_ECO2, timestamp3, ccs811.getECO2())
                pipe.execute_command("ts.add", DATAID_CCS811_TVOC, timestamp3, ccs811.getTVOC())

                # ----- SGP30
                sgp30.readData()
                timestamp4 = int(sgp30.getScanDateTime().timestamp() * 1000)
                pipe.execute_command("ts.add", DATAID_SGP30_ECO2, timestamp4, sgp30.geteCO2())
                pipe.execute_command("ts.add", DATAID_SGP30_TVOC, timestamp4, sgp30.getTVOC())

                # ----- BME680
                bme680.readData()
                timestamp5 = int(bme680.getScanDateTime().timestamp() * 1000)
                pipe.execute_command("ts.add", DATAID_BME680_TEMPERATURE, timestamp5, bme680.getTemperature())
                pipe.execute_command("ts.add", DATAID_BME680_PRESSURE, timestamp5, bme680.getPressure())
                pipe.execute_command("ts.add", DATAID_BME680_HUMIDITY, timestamp5, bme680.getHumidity())
                pipe.execute_command("ts.add", DATAID_BME680_GAS_RESISTANCE, timestamp5, bme680.getGasRegistance())

                # ----- Entry data to Redis
                pipe.execute()

                #####  WAIT FOR NEXT DATA ENTRY
                #print(timestamp5)
                time.sleep(SENSING_INTERVAL_SEC)

            except:
                print(" --- xxx ---")
                time.sleep(5)
                #time.sleep(SENSING_INTERVAL_SEC)

    except KeyboardInterrupt:
        pass

# -------------------
print("\n\nDone.\n")
redis_obj.quit()
