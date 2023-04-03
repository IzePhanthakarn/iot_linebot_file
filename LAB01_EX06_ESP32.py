from machine import Pin, I2C
from lcd_pcf8574 import LCD

i2c = I2C(0,scl=Pin(22),sda=Pin(21))
lcd = LCD(i2c,0x27)

lcd.clear()
lcd.print('Hello ESP32')
lcd.goto_line(1)
lcd.print('MicroPython')
