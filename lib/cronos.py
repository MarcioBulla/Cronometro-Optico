from time import sleep_ms, ticks_ms, ticks_diff
from encoder_menu import * 


# Sensor IR
IR = Pin(16, Pin.IN)

set_data("Pendulo", {})
set_data("pend_N", 5)

async def pend_show(N_f, N_a, time):
    oled.fill(0)
    oled.text("PENDULO",0,0)
    oled.text(f"T: {str(N_a)}", 0, 20)
    oled.text(f"Tf: {str(N_f)}", 48, 20)
    oled.text(str(time),0,56)
    oled.show()
    await asyncio.sleep(1/60)

class Pendulo():
    
    def __init__(self, menu_data, IR):
        self.pend_N = menu_data.get("pend_N", 5)
        self.pend_hist = menu_data.get("Pendulo", {})
        self.IR = IR
        
    def on_scroll(self):
        back()
    
    
    def on_click(self):
        back()
    
    def on_current(self):
        count = 0
        asyncio.run(pend_show(self.pend_N, count, 0))
        while self.IR.value() == 1:
            pass
        start = ticks_ms()
        while count < self.pend_N:
            if self.IR.value() == 1:
                count += 1
            asyncio.run(pend_show(self.pend_N, count, ticks_diff(ticks_ms(), start)))
        end = ticks_ms()
        asyncio.run(pend_show(self.pend_N, count, ticks_diff(end, start)))
            

def pendulo(menu_data=menu_data, IR=IR):
    "Wrap simple text output into "
    return wrap_object(Pendulo(menu_data, IR))