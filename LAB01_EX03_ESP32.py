from machine import Pin, SPI
import utime
from max7219 import Max7219

spi = SPI(1,sck=Pin(14),mosi=Pin(13))
#CLK=sck=D14,DIN=mosi=D13,cs=D15
cs = Pin(15,Pin.OUT)
display = Max7219(8,8,spi,cs,False) #width=8 height=8
display.brightness(5)

while True:
    for i in range(0,10):
        display.fill(0) # clear
        display.text(str(i),0,0)
        display.show()        
        utime.sleep(2)
