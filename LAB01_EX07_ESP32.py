from machine import Pin, I2C, ADC
from lcd_pcf8574 import LCD
from utime import sleep_ms

i2c = I2C(0,scl=Pin(22),sda=Pin(21))
lcd = LCD(i2c,0x27)
lcd.clear()

soil = ADC(Pin(32))
soil.atten(ADC.ATTN_11DB) # max input 3.6v
soil.width(ADC.WIDTH_10BIT) # 0 - 1023

while True:  
   soil_value = soil.read()
   lcd.clear()
   lcd.print(str(soil_value))
   lcd.goto_line(1)
   if soil_value > 700:
       lcd.print('Dry')
   else:
       lcd.print('Wet')
   sleep_ms(250)  
