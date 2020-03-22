from machine import Pin, I2C
from network import WLAN, AP_IF, STA_IF

from dht import DHT22
from ssd1306 import SSD1306_I2C

# NodeMCU pin definition
pins = {'D0': 16, 'D1': 5, 'D2': 4, 'D3': 0, 'D4': 2,
        'D5': 14, 'D6': 12, 'D7': 13, 'D8': 15}

# pins config
LED_PIN = pins['D4']
DHT22_PIN = pins['D2']
I2C_SCL_PIN = pins['D5']
I2C_SDA_PIN = pins['D6']

# led config
led_config = Pin(LED_PIN, Pin.OUT)

# sensor config
LOG_INTERVAL = 5  # in minutes
sensor_config = DHT22(Pin(DHT22_PIN))


# display config
i2c = I2C(
    scl=Pin(I2C_SCL_PIN),
    sda=Pin(I2C_SDA_PIN))
i2c.scan()
display_config = SSD1306_I2C(128, 64, i2c)

# button config
BUTTON_PIN = pins['D1']
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# connection config
connection_config = {
    'WIFI_SSID': '',
    'WIFI_PASSW': '',
    'AP_MODE': WLAN(AP_IF),  # access point mode
    'WIFI_MODE': WLAN(STA_IF),  # wifi mode
    'API_KEY': '',
    'API_URL': '',
    'SENSOR_ID': 1,
}



