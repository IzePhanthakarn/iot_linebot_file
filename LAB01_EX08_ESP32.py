from machine import Pin, I2C
from lcd_pcf8574 import LCD
from utime import sleep_ms
from hcsr04 import HCSR04

i2c = I2C(0,scl=Pin(22),sda=Pin(21))
lcd = LCD(i2c,0x27)
lcd.clear()

sensor = HCSR04(trigger_pin=13, echo_pin=12)

while True:
    distance = int(sensor.distance_cm())
    if distance < 50:
        lcd.clear()
        lcd.print(str(distance) + ' cm')
    sleep_ms(300)
    
