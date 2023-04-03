from machine import Pin, I2C, Timer
from lcd_pcf8574 import LCD
from utime import sleep
import dht

i2c = I2C(0,scl=Pin(22),sda=Pin(21))
lcd = LCD(i2c,0x27)
lcd.clear()
lcd.print("H = ")
lcd.goto_line(1)          
lcd.print("T = ")
    
dht22 = dht.DHT22(Pin(14))

def update_humi_temp(event):
    dht22.measure()
    lcd.clear()
    lcd.print("H = " + '{:.1f}'.format(dht22.humidity()))
    lcd.goto_line(1)          
    lcd.print("T = " + '{:.1f}'.format(dht22.temperature()))
    
dht_timer = Timer(1)
dht_timer.init(period=2500, mode=Timer.PERIODIC, callback=update_humi_temp)
