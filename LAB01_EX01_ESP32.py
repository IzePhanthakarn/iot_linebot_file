from machine import Pin
import utime

led = Pin(23,Pin.OUT)

while True:
    led.on()
    utime.sleep(1)
    led.off()
    utime.sleep(1)
