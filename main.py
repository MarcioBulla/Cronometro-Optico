from encoder_menu import * 
from cronos import *
from ujson import load
from machine import freq
print(gc.mem_free(), gc.mem_alloc())

freq(240000000)

# set_data(key=, value=) 
with open("calibration.json", "r") as file:
    for key, value in load(file).items():
        set_data(key, value)

set_data("Pendulo", [])
set_data("Energy", [])
set_data("Mola", [])

# get_integer(low_v=, high_v=, increment=, caption=, field=)
# selection(field=, choices=)
# wizard funciona como um wrap_menu porem como uma sequencia de funções
# exemplo de wizard
# wizard([("Hours",sethours),("Minutes",setminutes),("Seconds",setseconds)])
print(menu_data)

BACK = ("Voltar", back)

# Pendulo
pend_config = get_integer(low_v=1, high_v=9, increment=1, caption="N° Periodos", field="pend_N")
pend_hist = hist(oled, "Pendulo", "Hist: Pendulo")

## menu Pendulo
pend_menu = wrap_menu("Pendulo", [("START", pendulo()), ("Config", pend_config), ("Historico", pend_hist), BACK])


# Energia Mecanica
energy_config = selection("cylinder", [("Solido", "sol"), ("2 * Interno", "2*I"), ("2 * Externo", "2*E"), ("int + Ext", "I+E")])
energy_hist = hist(oled, "Energy", "Hist: Energy")

## menu Energia Mecanica
energy_menu = wrap_menu("Energia Mec", [("START", energy()), ("Config", energy_config), ("Historico", energy_hist), BACK])


# Mola
mola_config = get_integer(low_v=1, high_v=9, increment=1, caption="N° Periodos", field="mola_N")
mola_hist = hist(oled, "Mola", "Hist: Mola")

## menu Mola
mola_menu = wrap_menu("Mola", [("START", mola()), ("Config", mola_config), ("Historico", mola_hist), BACK])

# Calibragem
bias = get_integer(low_v=0, high_v=1000, increment=10, caption="Bias", field="bias", save=True)
escala = get_integer(low_v=.5, high_v=1.5, increment=0.01, caption="Escala", field="escala", rounded=True, deci=2, save=True)

## menu Calibragem
cal_menu = wrap_menu("Calibragem", [("Bias", bias), ("Escala", escala), BACK])


# Main Menu
main_menu = wrap_menu("Main Menu", [("Pendulo", pend_menu), ("Energia Mec",energy_menu), ("Mola", mola_menu), ("Calibragem", cal_menu)])

# Start
main_menu()
#pend_menu()
run_menu() 

