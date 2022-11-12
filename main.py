from machine import Pin, ADC
from time import sleep_ms
from rotary_irq_esp import RotaryIRQ
from encoder_menu import * 
from teste import *

# I2C Display
SDA, SCL = Pin(4), Pin(5)

# Encoder
CLK, DT, SW = 13, 12, Pin(14, Pin.IN)

# Leds
LED_G, LED_R = Pin(0, Pin.OUT), Pin(2, Pin.OUT)

# Sensor IR
IR_D, IR_A = Pin(16, Pin.IN), ADC(0)

# set_data(key=, value=) 
set_data("red led", 1)
set_data("green led", 0)

# get_integer(low_v=, high_v=, increment=, caption=, field=)
# selection(field=, choices=)
# wizard funciona como um wrap_menu porem como uma sequencia de funções
# exemplo de wizard
# wizard([("Hours",sethours),("Minutes",setminutes),("Seconds",setseconds)])
BACK = ("!!BACK!!", back)
setledred = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])
setledgreen = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])

setperiod = get_integer(low_v=1, high_v=10, increment=1, caption="periodo (s)", field="period")
setinterval = get_integer(low_v=50, high_v=1000, increment=50, caption="intervalo (ms)", field="interval")
setled = selection("led", [("vermelho", "red"), ("verde", "green")])
config_blink = wizard([("Periodo",setperiod),("Interval",setinterval),("Led",setled)])

blink_menu = wrap_menu([("BLINK config", config_blink),("START", get_blink), BACK])
test = wrap_menu([("blink", blink_menu), BACK])
main_menu = wrap_menu([("Testes", test), ("SAIR", back)])

main_menu()
run_menu() 
