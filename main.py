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

set_data("red led", 1)
set_data("green led", 0)

setledgreen = get_integer(low_v=0, high_v=10, increment=1, caption="Green Led", field="green led")
#setledred = get_integer(low_v=0, high_v=1, increment=1, caption="Red Led", field="red led")
setledred = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])

test_led = wrap_menu([("LED VERMELHOR", setledred), ("LED VERDE", setledgreen), ("!!BACK!!", back)])
main_menu = wrap_menu([("TESTAR LEDs", test_led), ("SAIR", stop), ("LED VERDE", setledgreen)])

main_menu()
run_menu() 
