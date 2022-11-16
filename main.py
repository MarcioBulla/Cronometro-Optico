from encoder_menu import * 
from machine import Pin
from cronos import *

# set_data(key=, value=) 


set_data("Pendulo", [])
set_data("pend_N", 5)



# get_integer(low_v=, high_v=, increment=, caption=, field=)
# selection(field=, choices=)
# wizard funciona como um wrap_menu porem como uma sequencia de funções
# exemplo de wizard
# wizard([("Hours",sethours),("Minutes",setminutes),("Seconds",setseconds)])


BACK = ("Voltar", back)

# Pendulo
pend_nperidos = get_integer(low_v=1, high_v=10, increment=1, caption="N° Periodos", field="pend_N")
pend_hist = hist(oled, "Pendulo", "Hist: Pendulo")

## menu
pend_menu = wrap_menu("Pendulo", [("START", pendulo()), ("Config", pend_nperidos), ("Historico", pend_hist), BACK])
# Eng Mec

## menu
engmec_menu = wrap_menu("Energia Mec", [("Config", dummy), ("START", dummy), ("Historico", dummy), BACK])
# Mola

## menu
mola_menu = wrap_menu("Mola", [("Config", dummy), ("START", dummy), ("Historico", dummy), BACK])
# Main Menu
main_menu = wrap_menu("Main Menu", [("Pendulo", pend_menu), ("Eng Mec",engmec_menu), ("Mola", mola_menu)])

# Start
main_menu()
#pend_menu()
run_menu() 
