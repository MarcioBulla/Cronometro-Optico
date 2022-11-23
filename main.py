from encoder_menu import * 
from cronos import *

# set_data(key=, value=) 
set_data("Pendulo", [])
set_data("Energy", [])
set_data("Mola", [])

# get_integer(low_v=, high_v=, increment=, caption=, field=)
# selection(field=, choices=)
# wizard funciona como um wrap_menu porem como uma sequencia de funções
# exemplo de wizard
# wizard([("Hours",sethours),("Minutes",setminutes),("Seconds",setseconds)])


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
mola_menu = wrap_menu("Mola", [("Config", mola_config), ("START", mola()), ("Historico", mola_hist), BACK])


# Main Menu
main_menu = wrap_menu("Main Menu", [("Pendulo", pend_menu), ("Energia Mec",energy_menu), ("Mola", mola_menu)])

# Start
# print(gc.mem_free(), gc.mem_alloc())
main_menu()
#pend_menu()
run_menu() 


