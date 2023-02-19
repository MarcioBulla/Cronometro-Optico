from time import ticks_ms, ticks_diff
from encoder_menu import * 
from machine import Pin

# Sensor IR
IR = Pin(36, Pin.IN)

# variaveis globais
COUNT = 0
START = 0
END = 0


async def crono(inicio, N_mud):
    """
    Contador de mudanças de estados
    """
    global COUNT, START, END, IR
    COUNT = 0
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
            print(COUNT)
    END = ticks_ms()


async def show_display(display):
    """
    Atualizador do display
    """
    global START, END, menu_data, LED, lcd
    LED.on()
    lcd.move_to(0,3)
    lcd.putstr(f"{"Aguarde":^20}")
    while not START:
        await asyncio.sleep_ms(600)
    while not END:
        display(convert(ticks_diff(ticks_ms(), START)))    
        await asyncio.sleep_ms(600)
    display(convert(ticks_diff(END, START)))
    lcd.move_to(0,3)
    lcd.putstr(f"{"!!Concluido!!":^20}")
    while True:
        LED(not LED())
        await asyncio.sleep_ms(250)


def convert(time):
    """
    Conversor de tempo em string
    """
    global menu_data
    bias = menu_data.get("bias")
    time += bias
    return f"{time//1000:>02}:{time%1000:>03}"


# Classes de Experimentos
class Pendulo():
    """
    Classe para experimento pendulo
    """
    def __init__(self):
        global menu_data
        self.hist = menu_data.get("Pendulo")


    def on_scroll(self,val):
        pass


    def on_click(self):
        global COUNT, START, END, LED
        stop(self.show)
        stop(self.start)
        if END:
            self.hist.append(f"P={self.NT}; T={convert(ticks_diff(END, START))}")
        # print(self.hist)
        COUNT = 0
        START = 0
        END = 0
        LED.off()
        back()
    
    
    def display(self, time):
        global COUNT, lcd
        lcd.move_to(9, 1)
        lcd.putstr(str(COUNT//4))
        lcd.move_to(7, 2)
        lcd.putstr(time)
    
    
    def on_current(self):
        global menu_data, lcd
        self.NT = menu_data.get("pend_N", 5)
        lcd.clear()
        lcd.putstr(f"{"Pendulo":^20}")
        lcd.move_to(0,1)
        lcd.putstr(f"Periodo: 0/{self.NT}")
        lcd.move_to(0,2)
        lcd.putstr("Tempo: ")
        self.show = make_task(show_display, self.display)
        self.start = make_task(crono, 1, self.NT*4)
        
    
class Energy():
    """
    Classe para experimento de Energia Mecanica
    """
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
        
        COUNT = 0
        START = 0
        END = 0
        
        LED.off()
        back()
        
    
    def display(self, time):
        global COUNT, lcd
        lcd.move_to(7, 2)
        lcd.putstr(time)
        
    
    def on_current(self):
        global menu_data, lcd
        
        self.cylinder = menu_data.get("cylinder", "Solido")
        lcd.clear()
        lcd.putstr(f"{"Energia Mecanica":^20}")
        lcd.move_to(0,1)
        lcd.putstr(f"cilindro: {self.cylinder}")
        lcd.move_to(0,2)
        lcd.putstr("Tempo: ")
        
        self.show = make_task(show_display, self.display)
        
        if self.cylinder == "Solido":
            self.start = make_task(crono, 0, 1)
        elif self.cylinder == "2R"+chr(4):
            self.start = make_task(crono, 1, 1)
        elif self.cylinder == "2R"+chr(3):
            self.start = make_task(crono, 0, 3)
        else:
            self.start = make_task(crono, 0, 2)

class Mola():
    """
    Classe para experimento de mola
    """
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
        
        COUNT = 0
        START = 0
        END = 0
        
        LED.off()
        back()
        
    
    def display(self, time):
        global COUNT, lcd
        lcd.move_to(9, 1)
        lcd.putstr(str((COUNT)//2))
        lcd.move_to(7, 2)
        lcd.putstr(time)      
    
    
    def on_current(self):
        global menu_data
        self.NT = menu_data.get("mola_N", 1)
        
        lcd.clear()
        lcd.putstr(f"{"Mola":^20}")
        lcd.move_to(0,1)
        lcd.putstr(f"Periodo: 0/{self.NT}")
        lcd.move_to(0,2)
        lcd.putstr("Tempo: ")
        self.show = make_task(show_display, self.display)
        
        self.start = make_task(crono, 1, self.NT * 2)

 
# Definições para usar as funções
def pendulo():
    "Função para o pendulo"
    return wrap_object(Pendulo())

def energy():
    "Função para a Energia Mecanica"
    return wrap_object(Energy())

def mola():
    "Função para a mola"
    return wrap_object(Mola())
