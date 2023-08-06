#----------------------------------------------------------------------
#   MODULES
#----------------------------------------------------------------------
from tqdm import tqdm
import time
import os
import webbrowser
import sys
import requests
from datetime import date
from datetime import datetime
import pynput
import time
import speedtest
import pyttsx3 as tts
from bs4 import BeautifulSoup
import random
#----------------------------------------------------------------------
#   GLOBAL VARIABLES
#----------------------------------------------------------------------
fpfill = "##############################################################"
def pspacer(x=1):
    for i in range(x):
        print("\n")

def rNG(x=0000, y=9999):
    random_number_generator = random.randint(x,y)
    return random_number_generator

#----------------------------------------------------------------------
# DICTIONATIES
#----------------------------------------------------------------------


functions_dict = {"bol()":"Using d:pyttsx3 converts string to audio",
                "open_web_d()": "opens web-browser from links_dict input key",
                "speed_test()":"looks for nearest server and tests the internet speed",
                "bot_commands()": "these commands have a seperate dictionary called bot_dict \n     usage:\n        bot_skills()",
                "web_b()": "Opens new web browser tab \n    Required string input \n    default assigned = blank string",
                "rNG()": "GENERATES A RANDOM NUMBER BETWEEN 0000,9999",
                "linkDownload()" : "(LINK INPUT REQUIRED) DOWNLOADS THE LINKS, GETS THE EXTENTION FROM THE LINK, SAVES IN DEFAULT DIRECTORY",
                }

bot_dict ={"bot_type()":"needs string input of what to type, waits 3 seconds and will paste the input at the cusor position",
        "bot_date()":"print current date",
        "bot_get_mouse_position()":"gets mouse position as tuple of (x,y)",
        "bot_goto_mouse_position()":"goes to specified mouse position as above parameters",
        "bot_leftclick()":"clicks left mouse button and releases right away",
        "bot_time()":"prints and says current time in 12 hour format",
        }

links_dict = {"youtube":"https://www.youtube.com",
        "google": "https://www.google.com/",
        "github": "https://github.com/",
        "pypi":"https://pypi.org/",
        "netflix": "https://www.netflix.com/browse",
        "instagram": "https://www.instagram.com/",
        "scarlett": "https://images.hdqwalls.com/download/2018-scarlett-johansson-1i-1920x1080.jpg",
        "py_wallpaper" : "https://images.hdqwalls.com/wallpapers/python-programming-syntax-4k-1s.jpg",
        "speech_recognition":"https://www.analyticsvidhya.com/blog/2019/07/learn-build-first-speech-to-text-model-python/"}

#----------------------------------------------------------------------
#----------------------------------------------------------------------






#-------------------------------------------------------------------
# THESE ARE NOT IMPLEMENTED PROPERLY YET. 
#-------------------------------------------------------------------
# TEST GROUND STARTS HERE

# BUT THEY WORK FOR WHAT THEY ARE ASSIGNED FOR, FOR NOW
#
#d: tqdm
# progress bar

def progBar():
    for i in tqdm(range(100)):
        time.sleep(0.01)


def htmlText(x=''):
    y = BeautifulSoup(x)
    print(y.body.find('div', attrs={'class':'container'}).text)



#
#d: os
# custom package installer 
# ADDING MORE DEPENDENCIES

def tSetup():
    os.system('pip install Pillow')
    pass








# TEST GROUND FINISHED HERE
#-------------------------------------------------------------------
#-------------------------------------------------------------------






#-------------------------------------------------------------------
# THESE ARE BASIC PLUG AND PLAY FUNCTIONS WHICH CAN BE USED ANYWHERE IF REQUIRED DEPENDENCIES ARE TRUE
#-------------------------------------------------------------------


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#1
#d: pyttsx3
#string to voice
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
def open_web_d(x=""):
    webbrowser.open_new_tab(links_dict[x])

def web_b(x=""):
    webbrowser.open_new_tab(x)
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#3 
# Internet speed test
#d: speedtest-cli
def speed_test():
    test = speedtest.Speedtest()
    print("Looking for servers")
    bol('Looking for near-by servers')
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
# GENERIC BOT FUNCTIONS
# DATETIME MASTER
# Guido_Van_Rossum = datetime.date(1956, 1, 31)
#d: os.system('pip install datetime)
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
        bol("GOOD Morning")
    elif hour_of_the_day>=12 and hour_of_the_day<18:
        print("Good Afternoon")
        bol("GOOD Afternon")
    else:
        print("Good Evening")
        bol('Good evening')

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#6
#d: requests
# REQUIRES DOWNLOAD LINK INPUT as a string
def linkDownload(x=""):
    #extention_hack = x.split(".")[-1]
    naam = ("DOWNLOADED"+str(rNG())+"."+x.split(".")[-1])
    with requests.get(x, stream=True) as r:
        print("Grabbing")
        with open(naam, 'wb')as f:
            print("Writing")
            for purja in r.iter_content(chunk_size=(1024*8)):
                f.write(purja)
    f.close()
    print("Written!")
#-------------------------------------------------------------------
#-------------------------------------------------------------------


#-------------------------------------------------------------------
#-------------------------------------------------------------------




# ALL FUNCTION LISTED THROUGH A FUNCTION HELPER
# ALL FUNCTION LISTED THROUGH A FUNCTION HELPER
# ALL FUNCTION LISTED THROUGH A FUNCTION HELPER


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

def webLinksDict():
    print(fpfill)
    print("KEY : ASSIGNED LINK FOR TESTING")
    print(fpfill)
    print('\n')
    counter = 1
    for key in links_dict:
        print(key, ":", links_dict[key])

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

def bot():
    bot_greet()
    bot_date()
    bot_time()
    bol("I am listing all the available 'FUNCTIONS' down below, feel free to scrool up")
    usage()
    bot_skills()
    bot_get_mouse_position()
    bol('bye now')


if __name__ == '__main__':
    bot()

# ------------------------------------------------
# THATS IT FOR NOW
# -------------------------------------------------


