from machine import Pin, ADC
from time import sleep_ms
from rotary_irq_esp import RotaryIRQ
from encoder_menu import * 

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

setledred = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])
setledgreen = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])

test_led = wrap_menu([("LED VERMELHOR", setledred), ("LED VERDE", setledgreen), ("!!BACK!!", back)])
main_menu = wrap_menu([("TESTAR LEDs", test_led), ("SAIR", stop), ("LED VERDE", setledgreen)])

main_menu()
run_menu() 
