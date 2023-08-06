#GLOBAL VARIABLES
fpfill = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
def pspacer():
    for i in range(5):
        print("\n")



# ALL THE AVAILABLE FUNCTIONS ARE LISTED IN THE DICTIONARIES:
functions_dict = {"bol()":"Using d:pyttsx3 converts string to audio",
                "open_web_b()": "opens web-browser from links_dict input key",
                "speed_test()":"looks for nearest server and tests the internet speed",
                "bot_commands()": "these commands have a seperate dictionary called bot_dict \n     usage:\n        bot_skills()",
                "web_b()": "Opens new web browser tab \n    Required string input \n    default assigned = blank string",
                }

bot_dict ={"bot_type()":"needs string input of what to type, waits 3 seconds and will paste the input at the cusor position",
        "bot_date()":"print current date",
        "bot_get_mouse_position()":"gets mouse position as tuple of (x,y)",
        "bot_goto_mouse_position()":"goes to specified mouse position as above parameters",
        "bot_leftclick()":"clicks left mouse button and releases right away",
        "bot_time()":"prints and says current time in 12 hour format",
        }

#printing dict function 
def usage():
    print(fpfill)
    print("All functions are listed below, use as you may;")
    print(fpfill)
    print('\n')
    counter = 1
    for key in functions_dict:
        print(counter, ":", key)
        print("     ", ":", functions_dict[key])
        print("\n")
        counter += 1

def bot_skills():
    print(fpfill)
    print("Current bot skills are listed below:")
    print(fpfill)
    print('\n')
    counter = 1
    for key in bot_dict:
        print(counter, ":", key)
        print("     ", ":", bot_dict[key])
        print("\n")
        counter += 1


#1
#d: pyttsx3
#string to voice

import pyttsx3 as tts

def bol(audio):
    t = tts.init()
    rate = t.getProperty('rate')
    t.setProperty('rate', '125')
    volume = t.getProperty('volume')
    t.setProperty('volume', 1)
    voices = t.getProperty('voices')
    t.setProperty('voice', voices[1].id)
    t.say(audio)
    t.runAndWait()

#-------------------------------------------------------------------
#-------------------------------------------------------------------

#2
#d: sys, webbrowser
# open default webbbrowser
import webbrowser
import sys

links_dict = {"youtube":"https://www.youtube.com",
        "google": "https://www.google.com/",
        "github": "https://github.com/",
        "pypi":"https://pypi.org/",
        "netflix": "https://www.netflix.com/browse"}

def open_web_b(x=""):
    webbrowser.open_new_tab(links_dict[x])
# currently set to open youtube, change it as you may

def web_b(x=""):
    webbrowser.open_new_tab(x)

#-------------------------------------------------------------------
#-------------------------------------------------------------------

#3 
# Internet speed test
#d: speedtest-cli

import speedtest

def speed_test():
    test = speedtest.Speedtest()
    print("Looking for servers")
    bol('looking for near-by servers')
    test.get_servers()
    print("Getting closest server details")
    bol('Getting information of the nearest server')
    best = test.get_best_server()
    print(f"Located in {best['name']}, {best['country']}, \n")
    bol(f"Located in {best['name']}, {best['country']}, \n")
    download_result = test.download()
    upload_result = test.upload()
    ping_result = test.results.ping
    print(f"Download speed: {download_result/1024/1024 : .2f} Mbit/second")
    bol(f"Download speed: {download_result/1024/1024 : .2f} Mbit/second")
    print(f"Upload speed: {upload_result/1024/1024 : .2f} Mbit/second")
    bol(f"Upload speed: {upload_result/1024/1024 : .2f} Mbit/second")
    print(f"Latency: {ping_result : .2f}ms")
    bol(f"Latency: {ping_result}ms")


#-------------------------------------------------------------------
#-------------------------------------------------------------------

#4
#d: os.system('pip install pynput')
# control keyboard and mouse using python
# it also supports keyboard and mouse monitoring 
# check pynput documnetation on pypi
# from pynput.keyboard import Key, Controller
# from pynput.mouse import Button, Controller

import pynput
import time

def bot_type(x=""):
    keyboard = pynput.keyboard.Controller()
    #sleep time delay; change it according to the task requirement
    time.sleep(3)
    keyboard.type(x)

def bot_get_mouse_position():
    mouse = pynput.mouse.Controller()
    print('The current cursor position is {0}'.format(mouse.position))

def bot_goto_mouse_position(x=0, y=0):
    mouse = pynput.mouse.Controller()
    mouse.position = (x,y)

def bot_leftclick():
    mouse = pynput.mouse.Controller()
    button = pynput.mouse.Button
    mouse.press(button.left)
    mouse.release(button.left)
    #right click should work the same way saying right

#-------------------------------------------------------------------
#-------------------------------------------------------------------

#5
# DATETIME MASTER
# Guido_Van_Rossum = datetime.date(1956, 1, 31)
#d: os.system('pip install datetime)

from datetime import date
from datetime import datetime

bot_days_dict = {'0':'Monday',
        '1':'Tuesday',
        '2':'Wednesday',
        '3':'Thursday',
        '4':'Friday',
        '5':'Saturday',
        '6':'Sunday'}

bot_month_dict = {'1':'Janauary',
		'2':'February',
		'3':'March',
		'4':'April',
		'5':'May',
		'6':'June',
		'7':'July',
		'8':'August',
		'9':'September',
		'10':'October',
		'11':'November',
		'12':'December'}

def bot_date():
    today = date.today()
    weekday = str(today.weekday())
    day = str(today.day)
    month = str(today.month)
    year = str(today.year)
    print(f"Today is {bot_days_dict[weekday]}, {day}, {bot_month_dict[month]}, {year}")
    bol(f"Today is {bot_days_dict[weekday]}, {day}, {bot_month_dict[month]}, {year}")

def bot_time():
    current_time = datetime.now()
    time_24f = current_time.strftime('%H:%M')
    time_12f = current_time.strftime('%I:%M %p')
    time = str(time_12f)
    print(time)
    bol(f"Current time is {time}")

def bot_greet():
    hour_of_the_day = datetime.now().hour
    if hour_of_the_day>=0 and hour_of_the_day<12:
        print("Good Morning")
        bol("Morning darling")
    elif hour_of_the_day>=12 and hour_of_the_day<18:
        print("Good Afternoon")
        bol("Afternon darling")
    else:
        print("Good Evening")
        bol('Good evening darling')

#-------------------------------------------------------------------

if __name__ == '__main__':
    bot_greet()
    bot_date()
    bot_time()
    bol("I am listing all the available 'FUNCTIONS' down below, feel free to scrool up")
    usage()
    bot_skills()
    bot_get_mouse_position()
    bol('bye now')
