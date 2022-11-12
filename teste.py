from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff
from encoder_menu import * 

# Leds
LED_G, LED_R = Pin(0, Pin.OUT), Pin(2, Pin.OUT)

def blink(pin, interval, period):
    start = ticks_ms()
    while period > ticks_diff(ticks_ms(), start):
        pin.on()
        sleep_ms(interval)
        pin.off()
        sleep_ms(interval)
        
# 'led': 'red', 'green led': 0, 'period': 3, 'LED VERMELHOR': '0', 'interval': 1, 'red led': 1

def get_blink():
    global menu_data, LED_R, LED_G
    choice_led = menu_data.get("led")
    if choice_led == "red":
        pin = LED_R
    else:
        pin = LED_G
    interval = menu_data.get("interval")
    period = menu_data.get("period") * 1000
    
    blink(pin, interval, period)
