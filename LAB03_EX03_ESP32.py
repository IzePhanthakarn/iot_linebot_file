from machine import Pin, SPI
from max7219 import Max7219
from utime import sleep_ms
from umqtt.simple import MQTTClient
import network

spi = SPI(1,sck=Pin(14),mosi=Pin(13))
#CLK=sck=D14,DIN=mosi=D13,cs=D15
cs = Pin(15,Pin.OUT)
display = Max7219(32,8,spi,cs,False)
display.brightness(5)

wifi_ssid = "ECS_4G_01"
wifi_pwd = "1111100000"

MQTT_BROKER = "mqtt.netpie.io"  
MQTT_CLIENT = "94158fb0-7acc-48d5-a3a6-399180f4746d" # Client ID
MQTT_USER = "ByiMqAVSXVs1bFrYhkCAr3GrBm9GC8mH" # Token
MQTT_PWD = "GWJjLpcQFJT_BgBConxwwAUBpy72e!Dv" # Secret
text_show = ''

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_pwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def sub_callback(topic, msg):
    print((topic, msg))
    if topic == b'@msg/led_mt':
        global text_show
        text_show = msg

def init_client():
    global client
    print("Trying to connect to MQTT Broker.")
    try:
        client = MQTTClient(MQTT_CLIENT, MQTT_BROKER, port=1883, user=MQTT_USER,password=MQTT_PWD)
        client.connect()
        print("Connected to ",MQTT_BROKER)
        topic_sub = b"@msg/led_mt"
        client.set_callback(sub_callback)
        client.subscribe(topic_sub)
    except:
        print("Trouble to init mqtt.") 

wifi_connect()  # connect to WiFi network
init_client()

while True:
    client.check_msg()
    if len(text_show) == 1:
        display.fill(0) #clear
        display.text(text_show,0,0)
        display.show()        
    elif len(text_show) > 1:
        display.marquee(text_show)
    sleep_ms(500)
