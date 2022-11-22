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
    print(f"START: {START}")
    print(f"END: {END}")

async def show_display(display):
    global START, END
    display(0)    
    oled.show()
    while not START:
        await asyncio.sleep(1/60)
    while not END:
        display(ticks_diff(ticks_ms(), START))    
        oled.show()
        await asyncio.sleep(1/60)
    display(ticks_diff(END, START))    
    oled.show()

    
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
            self.hist.append((self.NT, ticks_diff(END, START)))
        print(self.hist)
        COUNT = 1
        START = 0
        END = 0
        LED.off()
        back()
    
    def display_pend(self, time):
        global COUNT, oled
        oled.fill_rect(0,16,  128,48,  0)
        oled.text(f"Periodos: {str(self.NT)}", 0, 20, 1)
        oled.text(f"Foi: {str(COUNT//4)}", 0, 30, 1)
        oled.text(f"Tempo: {str(time)}",0,56, 1)
           
    def on_current(self):
        global LED, menu_data
        LED.on()
        self.NT = menu_data.get("pend_N", 5)
        
        oled.fill(0)
        oled.text("Pendulo", 5,0, 1)
        self.show = make_task(show_display, self.display_pend)
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
            self.hist.append((self.cylinder, ticks_diff(END, START)))
        print(self.hist)
        
        COUNT = 1
        START = 0
        END = 0
        
        LED.off()
        back()
        
    
    def display_energy(self, time):
        global COUNT, oled
        oled.fill_rect(0,16,  128,48,  0)
        oled.text(f"cilin: {self.cylinder}", 0, 20, 1)
        oled.text(f"Tempo: {str(time)}",0,56, 1)
        
    
    def on_current(self):
        global LED, menu_data
        LED.on()
        self.cylinder = menu_data.get("cylinder", "solido")
        
        
        oled.fill(0)
        oled.text("Pendulo", 5,0, 1)
        self.show = make_task(show_display, self.display_energy)
        
        if self.cylinder == "solido":
            self.start = make_task(crono, 1, 2)
        elif self.cylinder == "oco 2*int":
            self.start = make_task(crono, 0, 2)
        elif self.cylinder == "oco 2*ext":
            self.start = make_task(crono, 1, 4)
        else:
            self.start = make_task(crono, 1, 3)
            
        
def pendulo():
    "Função para o pendulo"
    return wrap_object(Pendulo())

def energy():
    "Função para o pendulo"
    return wrap_object(Energy())
