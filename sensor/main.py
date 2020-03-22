import time
import urequests
from setup import button, led_config, sensor_config, display_config, \
    connection_config, LOG_INTERVAL


class ConnectionControl:
    def __init__(self, connection_config):
        self.ssid = connection_config['WIFI_SSID']
        self.passw = connection_config['WIFI_PASSW']
        self.ap = connection_config['AP_MODE']
        self.wifi = connection_config['WIFI_MODE']
        self.key = connection_config['API_KEY']
        self.url = connection_config['API_URL']
        self.sensor_id = connection_config['SENSOR_ID']
        self.wifi_status = self.wifi.status()
        self.api_status = 0

    def get_wifi_status(self):
        return self.wifi.status()

    def get_api_status(self):
        return self.api_status

    def set_wifi_mode(self):
        self.ap.active(False)
        self.wifi.active(True)

    def set_ap_mode(self):
        self.wifi.active(False)
        self.ap.active(True)

    def connect_to_wifi(self):
        self.set_wifi_mode()

        while not self.wifi.isconnected():
            self.wifi.connect(self.ssid, self.passw)
            time.sleep(5)

    def disconnect_wifi(self):
        self.wifi.disconnect()

    def send_to_api(self, t, h):
        data = {'sensor_id': self.sensor_id,
                'key': self.key,
                'values': {
                    'temperature': t,
                    'humidity': h
                    }
                }
        try:
            r = urequests.post(self.url, json=data)
            self.api_status = r.status_code
        except Exception as e:
            self.api_status = 0
            print(e)


class LedControl:
    def __init__(self, led_config):
        self.l = led_config

    def set_on(self):
        self.l.value(0)

    def set_off(self):
        self.l.value(1)

    def toggle(self):
        if self.l.value():
            self.set_on()
        else:
            self.set_off()

    def blink(self, num=1, duration=0.5):
        start_status = self.l.value()
        self.set_off()
        time.sleep(1)
        for i in range(num):
            self.set_on()
            time.sleep(duration)
            self.set_off()
            time.sleep(duration)
        time.sleep(1)
        self.l.value(start_status)

    def blink_err(self, num):
        self.blink(10, 0.1)
        time.sleep(1)
        self.blink(num)


class DisplayControl:
    def __init__(self, display_config):
        self.d = display_config
        self.d.poweron()
        self.is_active = True

    def show_status(self, wifi_status, api_status):
        self.d.fill(0)
        self.d.text(
            'wifi: {} api: {}'.format(wifi_status, api_status), 0, 48)
        self.d.show()

    def show_temp_humidity(self, t, h):
        self.d.fill(0)
        self.d.text('temp.: {} C'.format(t), 0, 0)
        self.d.text('humidity: {} %'.format(h), 0, 16)
        self.d.show()

    def show_temp_humidity_status(self, t, h, wifi_status, api_status):
        self.d.fill(0)
        self.d.text('temp.: {} C'.format(t), 0, 0)
        self.d.text('humidity: {} %'.format(h), 0, 16)
        self.d.text(
            'wifi: {} api: {}'.format(wifi_status, api_status), 0, 48)
        self.d.show()

    def set_on(self):
        self.d.poweron()
        self.is_active = True

    def set_off(self):
        self.d.poweroff()
        self.is_active = False

    def toggle(self):
        if self.is_active:
            self.set_off()
        else:
            self.set_on()


class SensorControl:
    def __init__(self, sensor_config):
        self.s = sensor_config

    def read(self):
        self.s.measure()
        return self.s.temperature(), self.s.humidity()


con = ConnectionControl(connection_config)
led = LedControl(led_config)
display = DisplayControl(display_config)
sensor = SensorControl(sensor_config)


def run():
    led.set_off()
    led.blink(5)
    t, h = sensor.read()
    display.show_temp_humidity_status(
        t, h, con.get_wifi_status(), con.get_api_status())
    i = 0
    while True:
        if i < 60 * LOG_INTERVAL:
            if button.value() == 0:
                display.toggle()
                time.sleep(1)

            i += 1
            time.sleep(1)

        else:
            if con.wifi_status != 5:
                led.blink_err(3)
                con.connect_to_wifi()

            led.blink()
            t, h = sensor.read()
            con.send_to_api(t, h)
            display.show_temp_humidity_status(
                t, h, con.get_wifi_status(), con.get_api_status())
            i = 0


run()
