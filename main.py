from encoder_menu import * 
from teste import *
from cronos import *

# set_data(key=, value=) 
set_data("Pendulo", {})



# get_integer(low_v=, high_v=, increment=, caption=, field=)
# selection(field=, choices=)
# wizard funciona como um wrap_menu porem como uma sequencia de funções
# exemplo de wizard
# wizard([("Hours",sethours),("Minutes",setminutes),("Seconds",setseconds)])


BACK = ("!!BACK!!", back)
setledred = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])
setledgreen = selection("LED VERMELHOR", [("LIGADO", "1"), ("DESLIGADO", "0")])

setperiod = get_integer(low_v=1, high_v=10, increment=1, caption="periodo (s)", field="period")
setinterval = get_integer(low_v=50, high_v=1000, increment=50, caption="intervalo (ms)", field="interval")
config_blink = wizard([("Periodo",setperiod),("Interval",setinterval)])

blink_menu = wrap_menu([("BLINK config", config_blink),("START", get_blink), BACK])
test = wrap_menu([("blink", blink_menu),("Pendulo", pendulo()) ,BACK])
main_menu = wrap_menu([("Testes", test), ("SAIR", back)])

main_menu()
run_menu() 
