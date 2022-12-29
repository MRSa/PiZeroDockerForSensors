#!/usr/bin/env python
#
# Modified 
#   from https://github.com/pimoroni/bme680-python/blob/master/examples/read-all.py
#
import redis
import bme680
import time
import datetime

REDIS_HOST_PORT = 6379
REDIS_HOST_ADDRESS = 'redis'
REDIS_DB_NUMBER = 0 

DATAID_TEMPERATURE = "ts:bme680temperature"
DATAID_PRESSURE = "ts:bme680pressure"
DATAID_HUMIDITY = "ts:bme680humidity"
DATAID_GAS_RESISTANCE = "ts:bme680gasresistance"

SENSING_INTERVAL_SEC = 300   # 5 minite interval
#SENSING_INTERVAL_SEC = 3

redis_obj = redis.Redis(host=REDIS_HOST_ADDRESS, port=REDIS_HOST_PORT, db=REDIS_DB_NUMBER)


try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

# ----------------------------------------------
#print('\n\nInitial reading:')
#for name in dir(sensor.data):
#    value = getattr(sensor.data, name)
#    if not name.startswith('_'):
#        print('{}: {}'.format(name, value))
# ----------------------------------------------

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

print('\n\nPolling:')
try:
    pipe = redis_obj.pipeline()
    while True:
        timestamp = int(time.time() * 1000)
        if sensor.get_sensor_data():
           pipe.execute_command("ts.add", DATAID_TEMPERATURE, timestamp, sensor.data.temperature)
           pipe.execute_command("ts.add", DATAID_PRESSURE, timestamp, sensor.data.pressure)
           pipe.execute_command("ts.add", DATAID_HUMIDITY, timestamp, sensor.data.humidity) 
           if sensor.data.heat_stable:
               pipe.execute_command("ts.add", DATAID_GAS_RESISTANCE, timestamp, sensor.data.gas_resistance) 
        pipe.execute()
        print(timestamp)
        time.sleep(SENSING_INTERVAL_SEC)

except KeyboardInterrupt:
    pass

print("\n\nDone.\n")
redis_obj.quit()

