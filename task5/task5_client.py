# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
import requests

################### define functions
def master_switch():
    try:
        print("requesting server... master switch")
        requests.get("http://192.168.4.1/pins/pin12")
    except:
        print("request failed!")

def color_switch ():
    try:
        print("requesting server... color switch ")
        requests.get("http://192.168.4.1/pins/pin13")
    except:
        print("request failed!")
def on_purple():
    try:
        print("requesting server... try to change to purple")
        requests.put("http://192.168.4.1/leds/on_purple")
    except:
        print("request failed!")
def on_yellow():
    try:
        print("requesting server... try to change to yellow")
        requests.put("http://192.168.4.1/leds/on_yellow")
    except:
        print("request failed!")
def func_off():
    try:
        print("requesting server... try to turn off")
        requests.put("http://192.168.4.1/leds/off")
    except:
        print("request failed!")


################## create menu
# Create the menu
menu = ConsoleMenu("Task5_Client", "Author:Jianan&Rune&Simona")

check_buttons_status_menu = SelectionMenu([])
open_menu = SelectionMenu([])

check_buttons_status_item = SubmenuItem("Check Button Status", check_buttons_status_menu , menu)

open_item = SubmenuItem("Open", open_menu , menu)

off_item = FunctionItem("Turn off", func_off, [])

### check status menu
master_switch_item = FunctionItem("Master Switch(Pin13)", master_switch, [])
color_switch_item = FunctionItem("Color Switch(Pin12)", color_switch, [])
check_buttons_status_menu.append_item(master_switch_item)
check_buttons_status_menu.append_item(color_switch_item)

### open menu
mode_purple_item = FunctionItem("Mode Purple", on_purple, [])
mode_yellow_item = FunctionItem("Mode Yellow", on_yellow, [])
open_menu.append_item(mode_purple_item)
open_menu.append_item(mode_yellow_item)


menu.append_item(check_buttons_status_item)
menu.append_item(open_item)
menu.append_item(off_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()
