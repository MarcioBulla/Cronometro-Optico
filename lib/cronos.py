from time import ticks_ms, ticks_diff
from encoder_menu import * 
from machine import Pin

# Sensor IR
IR = Pin(16, Pin.IN)

COUNT = 1
N_mud = 0
START = 0
END = 0


async def crono(inicio, N_mud):
    global COUNT, START, END, IR
    COUNT = 1
    START = 0
    END = 0
    while True:
        state = IR.value()
        await asyncio.sleep_ms(0)
        if state == inicio and state != IR.value():
            START = ticks_ms()
            break
    while COUNT < N_mud:
        state = IR.value()
        await asyncio.sleep_ms(0)
        if state != IR.value():
            COUNT += 1
    END = ticks_ms()
    
    
class Pendulo():
    
    def __init__(self,IR, LED):
        global oled, menu_data
        self.oled = oled
        self.count = 0
        self.hist = menu_data.get("Pendulo")
        self.IR = IR
        self.LED = LED

    def on_scroll(self,val):
        pass
        
    def on_click(self):
        global COUNT, START, END
        stop(self.show)
        stop(self.start)
        if END != 0:
            self.hist.append((self.NT, self.time))
        print(self.hist)
        COUNT = 1
        START = 0
        END = 0
        self.LED.off()
        back()
    
    def display_pend(self, time):
        global COUNT
        self.oled.fill_rect(0,16,  128,48,  0)
        self.oled.text(f"Periodos: {str(self.NT)}", 0, 20, 1)
        self.oled.text(f"Foi: {str(COUNT//4)}", 0, 30, 1)
        self.oled.text(f"Tempo: {str(time)}",0,56, 1)
    
    async def show_pend(self,NT):
        global START, END
        self.display_pend(0)    
        self.oled.show()
        while not START:
            await asyncio.sleep(1/60)
        while not END:
            self.display_pend(ticks_diff(ticks_ms(), START))    
            self.oled.show()
            await asyncio.sleep(1/60)
        self.time = ticks_diff(END, START)
        self.display_pend(self.time)    
        self.oled.show()
           
    def on_current(self):
        self.LED.on()
        global menu_data
        self.NT = menu_data.get("pend_N", 5)
        self.oled.fill(0)
        self.oled.text("Pendulo", 5,0, 1)
        self.show = make_task(self.show_pend, self.NT)
        self.start = make_task(crono, 0, self.NT*4+1)


def pendulo(IR=IR, LED=LED):
    "Função para o pendulo"
    return wrap_object(Pendulo(IR, LED))
