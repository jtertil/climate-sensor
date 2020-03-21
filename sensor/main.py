import time
import urequests
import uasyncio
from setup import button, led, sensor, display, ap, wifi, WLAN_SSID, \
    WLAN_PASSW, API_KEY, API_URL, SENSOR_ID, READ_INTERV


def display_data(temperature, humidity):
    display.fill(0)
    display.text('temp.: {} C'.format(temperature), 0, 0)
    display.text('humidity: {} %'.format(humidity), 0, 32)
    display.show()


def sensor_read():
    sensor.measure()
    led_blink(1)
    return sensor.temperature(), sensor.humidity()


def connect_to_wifi(ssid=WLAN_SSID, passw=WLAN_PASSW):
    ap.active(False)
    wifi.active(True)

    while not wifi.isconnected():
        led_blink(3)
        wifi.connect(ssid, passw)
        time.sleep(5)


def log_data(temperature, humidity):
    data = {'sensor_id': SENSOR_ID,
            'key': API_KEY,
            'values': {
                'temperature': temperature,
                'humidity': humidity
                }
            }

    try:
        urequests.post(API_URL, json=data)
    except Exception as e:
        print(e)


def led_blink(num):
    for i in range(num):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
    led.on()


async def run():
    while True:
        if wifi.isconnected():
            t, h = sensor_read()
            log_data(t, h)
            await uasyncio.sleep(60 * READ_INTERV)
        else:
            connect_to_wifi()


async def display_toggle():
    while True:
        if button.value() == 0:
            print(button)
            await uasyncio.sleep(1)


loop = uasyncio.get_event_loop()
loop.create_task(display_toggle())
loop.create_task(run())
loop.run_forever()