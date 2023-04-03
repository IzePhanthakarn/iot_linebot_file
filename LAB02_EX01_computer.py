import paho.mqtt.client as mqttClient
import time
 
broker_address= "mqtt.netpie.io"
port = 1883

client = mqttClient.Client("2334f5ea-bd2e-4c4c-8f75-1996a41c8358") # Client ID
user = "ByJgtZJcWSSAHB3Qph6zGASsD2tzDeZS" # Token
password = "qH~ctll8KUt80a87j0tb*m8Zq~X0MRS0" # Secret
client.username_pw_set(user, password=password)    

try:
    client.connect(broker_address, port=port)
except:
    print("Connection failed")

while True:
    text_out = input("Enter Text to MQTT Broker : ")
    client.publish("@msg/led",text_out)
    time.sleep(1)
