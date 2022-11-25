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
pend_config = get_integer(low_v=1, high_v=9, increment=1, caption="N Periodos", field="pend_N")
pend_hist = hist(oled, "Pendulo", "Hist: Pendulo")

## menu Pendulo
pend_menu = wrap_menu("Pendulo", [("START", pendulo()), ("Config", pend_config), ("Historico", pend_hist), BACK])


# Energia Mecanica
energy_config = selection("cylinder", [("Solido", "sol"), ("2 * Interno", "2*I"), ("2 * Externo", "2*E"), ("int + Ext", "I+E")], "Tipos de medida")
energy_hist = hist(oled, "Energy", "Hist: Energy")

## menu Energia Mecanica
energy_menu = wrap_menu("Energia Mecanica", [("START", energy()), ("Config", energy_config), ("Historico", energy_hist), BACK])


# Mola
mola_config = get_integer(low_v=1, high_v=9, increment=1, caption="N Periodos", field="mola_N")
mola_hist = hist(oled, "Mola", "Hist: Mola")

## menu Mola
mola_menu = wrap_menu("Mola", [("START", mola()), ("Config", mola_config), ("Historico", mola_hist), BACK])


# Calibragem
bias_centena = get_integer(low_v=-1000, high_v=0, increment=100, caption="Bias Centena (ms)", field="bias", save=True)
bias_dezena = get_integer(low_v=-1000, high_v=0, increment=10, caption="Bias Dezena (ms)", field="bias", save=True)
bias_unidade = get_integer(low_v=-1000, high_v=0, increment=1, caption="Bias Unidade (ms)", field="bias", save=True)
bias = wizard([("Bias Centena",bias_centena),("Bias Dezena",bias_dezena),("Bias Unidade (ms)",bias_unidade)])


# Criadores
criadores = info("Orientador:\n  Fabiano\nDevOps:\n  Marcio Bulla\n  Jessica Lo")


## menu Calibragem
extra = wrap_menu("Extras", [("Calibragem Bias", bias), ("Desenvolvedores", criadores), BACK])


# Main Menu
main_menu = wrap_menu("Main Menu", [("Pendulo", pend_menu), ("Energia Mecanica",energy_menu), ("Mola", mola_menu), ("Extras", extra)])

# Start
main_menu()
run_menu() 


