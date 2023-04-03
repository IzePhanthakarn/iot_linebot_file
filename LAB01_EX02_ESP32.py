from machine import Pin, PWM
import utime

r = PWM(Pin(18),duty=0)
g = PWM(Pin(19),duty=0)
b = PWM(Pin(21),duty=0)

while True:
    r.duty(1023)
    g.duty(0)
    b.duty(0)
    utime.sleep(1)
    r.duty(0)
    g.duty(1023)
    b.duty(0)
    utime.sleep(1)
    r.duty(0)
    g.duty(0)
    b.duty(1023)
    utime.sleep(1)
    r.duty(800)
    g.duty(200)
    b.duty(30)
    utime.sleep(1)
