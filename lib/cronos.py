from time import ticks_ms, ticks_diff
from encoder_menu import * 
from machine import Pin

# Sensor IR
IR = Pin(36, Pin.IN)

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
    
async def show_display(display):
    global START, END, menu_data
    display(0)    
    while not START:
        await asyncio.sleep(1/60)
    while not END:
        display(convert(ticks_diff(ticks_ms(), START)))    
        await asyncio.sleep(1/60)
    display(convert(ticks_diff(END, START)))

def convert(time):
    global menu_data
    bias = menu_data.get("bias")
    # print(f"bias: {bias}")
    # print(time)
    time += bias
#     if time < 0:
#         s = time//-1000
#         ms = time%-1000
#     else:    
#         s = time//1000
#         ms = time%1000
     # print(s, ms)
#     return f"{s:>02}:{ms:>03}"
    return f"{time//1000:>02}:{time%1000:>03}"


class Pendulo():
    
    def __init__(self):
        global menu_data
        self.hist = menu_data.get("Pendulo")

    def on_scroll(self,val):
        pass
        
    def on_click(self):
        global COUNT, START, END, LED
        stop(self.show)
        stop(self.start)
        if END != 0:
            self.hist.append(f"P={self.NT}; T={convert(ticks_diff(END, START))}")
        print(self.hist)
        COUNT = 1
        START = 0
        END = 0
        LED.off()
        back()
    
    def display(self, time):
        global COUNT, lcd
        lcd.move_to(8, 1)
        lcd.putstr(f"{str(COUNT//4)}")
        lcd.move_to(0, 2)
        lcd.putstr(f"Tempo: {time}")
           
    def on_current(self):
        global LED, menu_data, lcd
        LED.on()
        self.NT = menu_data.get("pend_N", 5)
        lcd.clear()
        lcd.putstr(f"{"Pendulo":^20}")
        lcd.move_to(0,1)
        lcd.putstr(f"Periodo: /{self.NT}")
        self.show = make_task(show_display, self.display)
        self.start = make_task(crono, 0, self.NT*4+1)
        
    
class Energy():
    
    def __init__(self):
        global menu_data
        self.hist = menu_data.get("Energy")
    
    def on_scroll(self, val):
        pass
    
    
    def on_click(self):
        global COUNT, START, END, LED
        
        stop(self.show)
        stop(self.start)
        
        if END != 0:
            self.hist.append(f"{self.cylinder:>6}; T={convert(ticks_diff(END, START))}")
        print(self.hist)
        
        COUNT = 1
        START = 0
        END = 0
        
        LED.off()
        back()
        
    
    def display(self, time):
        global COUNT, lcd
        lcd.move_to(0, 2)
        lcd.putstr(f"Tempo: {time}")
        
    
    def on_current(self):
        global LED, menu_data, lcd
        LED.on()
        
        self.cylinder = menu_data.get("cylinder", "Solido")
        lcd.clear()
        lcd.putstr(f"{"Energia Mecanica":^20}")
        lcd.move_to(0, 1)
        lcd.putstr(f"cilindro: {self.cylinder}")
        
        self.show = make_task(show_display, self.display)
        
        if self.cylinder == "Solido":
            self.start = make_task(crono, 1, 2)
        elif self.cylinder == "2R"+chr(4):
            self.start = make_task(crono, 0, 2)
        elif self.cylinder == "2R"+chr(3):
            self.start = make_task(crono, 1, 4)
        else:
            self.start = make_task(crono, 1, 3)

class Mola():
    
    def __init__(self):
        global menu_data
        self.hist = menu_data.get("Mola")
    
    
    def on_scroll(self, val):
        pass
    
    
    def on_click(self):
        global COUNT, START, END, LED
        
        stop(self.show)
        stop(self.start)
        
        if END != 0:
            self.hist.append(f"P={self.NT}; T={convert(ticks_diff(END, START))}")
        print(self.hist)
        
        COUNT = 1
        START = 0
        END = 0
        
        LED.off()
        back()
        
    
    def display(self, time):
        global COUNT, lcd
        lcd.move_to(8, 1)
        lcd.putstr(f"{str((COUNT-1)//2)}")
        lcd.move_to(0, 2)
        lcd.putstr(f"Tempo: {time}")      
    
    def on_current(self):
        global LED, menu_data
        LED.on()
        self.NT = menu_data.get("mola_N", 1)
        
        
        lcd.clear()
        lcd.putstr(f"{"Mola":^20}")
        lcd.move_to(0,1)
        lcd.putstr(f"Periodo: /{self.NT}")
        self.show = make_task(show_display, self.display)
        
        self.start = make_task(crono, 0, self.NT * 2 +1)

        
def pendulo():
    "Função para o pendulo"
    return wrap_object(Pendulo())

def energy():
    "Função para a Energia Mecanica"
    return wrap_object(Energy())

def mola():
    "Função para a mola"
    return wrap_object(Mola())

