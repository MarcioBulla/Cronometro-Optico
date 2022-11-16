from time import ticks_ms, ticks_diff
from encoder_menu import * 
from machine import Pin

# Sensor IR
IR = Pin(16, Pin.IN)

class Pendulo():
    
    def __init__(self,IR, LED):
        global oled, menu_data
        self.oled = oled
        self.count = 0
        self.hist = menu_data.get("Pendulo")
        self.IR = IR
        self.LED = LED
        print(menu_data)

    def on_scroll(self,val):
        pass
        
    def on_click(self):
        self.LED.off()
        stop(self.show)
        stop(self.start)
        if self.END != None:
            self.hist.append((self.NT, self.time))
        print(self.hist)
        back()
    
    def display_pend(self, time):
        self.oled.fill_rect(0,16,  128,48,  0)
        self.oled.text(f"Periodos: {str(self.NT)}", 0, 20, 1)
        self.oled.text(f"Esta: {str(self.count)}", 0, 30, 1)
        self.oled.text(f"Tempo: {time}",0,56, 1)
    
    async def show_pend(self,NT):
        while self.count == 0:
            self.display_pend(str(0))
            self.oled.show()
            await asyncio.sleep(1/60)
        while NT > self.count:
            self.display_pend(str(ticks_diff(ticks_ms(), self.START)))    
            self.oled.show()
            await asyncio.sleep(1/60)


    async def start_pend(self, NT, IR):
        await asyncio.sleep(0)
        while not self.IR.value():
            pass
            await asyncio.sleep(0)
        self.START = ticks_ms()
        while self.NT > self.count:
            if self.IR.value():
                self.count += 1
                print("passou o pendulo")
                await asyncio.sleep(.1)
            await asyncio.sleep(0)
        self.END = ticks_ms()
        self.time = ticks_diff(self.END, self.START)
        self.display_pend(str(self.time))   
        self.oled.show()
    
    def on_current(self):
        global menu_data
        self.START = None
        self.END = None
        self.NT = menu_data.get("pend_N", 5)
        self.LED.on()
        self.oled.fill(0)
        self.oled.text("Pendulo", 5,0, 1)
        self.count = 0
        self.show = make_task(self.show_pend, self.NT)
        self.start = make_task(self.start_pend, self.NT, self.IR)
        
        
def pendulo(IR=IR, LED=LED):
    "Wrap simple text output into "
    return wrap_object(Pendulo(IR, LED))