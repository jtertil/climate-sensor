import urequests, time

from setup import led, sensor, ap, wifi, WLAN_SSID, WLAN_PASSW, \
    API_KEY, API_URL, SENSOR_ID, READ_INTERV


def sensor_read():
    sensor.measure()
    led_blink(1)
    return sensor.temperature(), sensor.humidity()


def connect_to_wifi():
    ap.active(False)
    wifi.active(True)

    if not wifi.isconnected():
        led_blink(3)
        while not wifi.isconnected():
            wifi.connect(WLAN_SSID, WLAN_PASSW)
            time.sleep(5)


def log_data(temperature, humidity):
    data = {'sensor_id': SENSOR_ID, 'key': API_KEY,
            'values': {'temperature': temperature, 'humidity': humidity}}

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


def run():
    while True:
        connect_to_wifi()
        t, h = sensor_read()
        log_data(t, h)
        time.sleep(60 * READ_INTERV)


run()
