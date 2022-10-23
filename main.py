from machine import Pin, I2C, ADC, Timer
import time
import ssd1306


sensor = Pin(5, Pin.IN)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def convert(ms):
    millisegundo = ms % 1000
    segundos = ms // 1000
    minutos = segundos // 60
    segundos = segundos % 60
    return str(minutos) + ":" + str(segundos) + ":" + str(millisegundo)
def show_time(t):
    oled.fill(0)
    oled.text(str(t) ,1,1,1)
    oled.show()

    
def att_display(t):
    oled.show()

timer = Timer(0)

timer.init(period = 10, mode=Timer.PERIODIC, callback=att_display)


while True:
    time.sleep_us(100)
    if not sensor.value():
        start = time.ticks_ms()
        while not sensor.value():
            oled.fill(0)
            oled.text("Cronometrando", 1,1,1)
            oled.text("ms: " + convert(time.ticks_diff(time.ticks_ms(), start)), 1,16,1)
           