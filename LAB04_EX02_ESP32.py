from machine import Pin, PWM, Timer
from utime import sleep_ms
from umqtt.simple import MQTTClient
import network
import dht

r = PWM(Pin(18),duty=0)
g = PWM(Pin(19),duty=0)
b = PWM(Pin(21),duty=0)

r.duty(1023) #ทำให้หลอดติดสีแดงในตอนแรก
g.duty(0)
b.duty(0)

dht22 = dht.DHT22(Pin(14))
led = Pin(23,Pin.OUT)

wifi_ssid = "ECS_4G_01"
wifi_pwd = "1111100000"

MQTT_BROKER = "mqtt.netpie.io"  
MQTT_CLIENT = "94158fb0-7acc-48d5-a3a6-399180f4746d" # Client ID
MQTT_USER = "ByiMqAVSXVs1bFrYhkCAr3GrBm9GC8mH" # Token
MQTT_PWD = "GWJjLpcQFJT_BgBConxwwAUBpy72e!Dv" # Secret


def update_humi_temp(event):
    global client
    dht22.measure()
    publish_str = "Temp: " + str(dht22.temperature()) + "°C, Humi: " + str(dht22.humidity()) + "%"
    #print(publish_str)     #"24.0,40.0"
    client.publish("@msg/t_h",'{:.1f}'.format(dht22.temperature()) + ',' + '{:.1f}'.format(dht22.humidity()))
    
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
    
    if topic == b'@msg/led':
        if msg == b'ledon':
            led.on()
        elif msg == b'ledoff':
            led.off()
            
    if topic == b'@msg/color':
        if msg == b'red':
            r.duty(1023)
            g.duty(0)
            b.duty(0)
        elif msg == b'green':
            r.duty(0)
            g.duty(1023)
            b.duty(0)
        elif msg == b'blue':
            r.duty(0)
            g.duty(0)
            b.duty(1023)

def init_client():
    global client
    print("Trying to connect to MQTT Broker.")
    try:
        client = MQTTClient(MQTT_CLIENT, MQTT_BROKER, port=1883, user=MQTT_USER,password=MQTT_PWD)
        client.connect()
        print("Connected to ",MQTT_BROKER)
        topic_sub = b'@msg/#'
        client.set_callback(sub_callback)
        client.subscribe(topic_sub)
    except:
        print("Trouble to init mqtt.") 

wifi_connect()  # connect to WiFi network
init_client()

dht_timer = Timer(1)
dht_timer.init(period=2000, mode=Timer.PERIODIC, callback=update_humi_temp)

while True:
    client.check_msg()
    sleep_ms(500)
