import network
from utime import sleep

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

while True:
    nets = wifi.scan()
    for net in nets:
        print('SSID : ' + net[0].decode('UTF-8') + ' , RSSI : ' + str(net[3]))
    print('......')
    sleep(2)
    