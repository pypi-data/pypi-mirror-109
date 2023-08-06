#----------------------------------------------------------------------
##################    MODULES     #####################################
#----------------------------------------------------------------------
import os
import sys
import cv2
import time
import random
import pynput
import requests
import speedtest
import webbrowser
import numpy as np
import pyttsx3 as tts
from tqdm import tqdm
import mediapipe as mp
from datetime import date
from bs4 import BeautifulSoup
from datetime import datetime

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
                "MasterHandDetector" : "Detects hand: d: cv2, mediapipe",
                "tImageBlack" : "numpy array generrated black image pop-up on screen",
                "fileSave" : "saves files(no-overwrites) in default directory with DOWNLOADED_name",
                "tImageRead" : "Shows image on screen: source required parameter",
                "tImageResize" : "(source, scale=50)",
                "tImageGray": "Shows grayscaled image of source",
                "tImageBlur" : "Shows blurrer image",
                "tVideoRead" : "Shows video on screen from source"}

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
################## OPEN CV FUNCTIONS ###################
#d:         os.system('pip install opencv-python') 
###########################################################

#----------------------------------------------------------------------
#  cv2 IMAGE RELATED FUNTIONS
#----------------------------------------------------------------------
# REQUIRES NUMPY
kernel = np.ones((5,5),np.uint8)
numpyImage = np.zeros((512,512,3),np.uint8)

def tImageBlack():
    cv2.imshow("BLACK", numpyImage)
    cv2.waitKey(0)

test_img = "DOWNLOADED_py1.jpg" 
pyPic = "DOWNLOADED3100.jpg"

import random

def fileSave(x=""):# takes .extention as input
    naam = str("DOWNLOADED"+str(random.randint(0000,9999))+x)
    return naam

def tImageRead(x=""):
    imageReader = cv2.imread(x)
    cv2.imshow("Image Reader", imageReader)
    cv2.waitKey(0)

# SOURCE = x AND DEFAULT SCALE IS SET TO 50
# CHANGE IT BY PASSING INT VALUE ON A SCALE OF 1 TO 100
def tImageResize(x="", scale=50):
    imageReader = cv2.imread(x, cv2.IMREAD_UNCHANGED)
    print("Original Dimentions:", imageReader.shape)
    scale_percent = scale
    width = int(imageReader.shape[1] * scale_percent / 100)
    height = int(imageReader.shape[0] * scale_percent / 100)
    newShape = (width, height)
    reSizer = cv2.resize(imageReader, newShape, interpolation=cv2.INTER_AREA)
    print("Resized dimentions:", reSizer.shape)
    fileName = str(fileSave(".jpg"))
    cv2.imwrite(fileName, reSizer)
    print(f"Saved in default directory as: {fileName}")
    cv2.imshow("Resized Image", reSizer)
    cv2.waitKey(0)
    cv2.destroyAllWindows

def tImageGray(x=""):
    imageReader = cv2.imread(x)
    grayedImage = cv2.cvtColor(imageReader, cv2.COLOR_BGR2GRAY)
    cv2.imshow("GREY IMAGE", grayedImage)
    cv2.waitKey(0)

def tImageBlur(x=""):
    imageReader = cv2.imread(x)
    # blur vale takes a kernel value which is used 7,7 below; 0 is the sigma x
    # it has to be odd number
    blurredImage = cv2.GaussianBlur(imageReader,(7,7),0)
    cv2.imshow("Blurred IMAGE", blurredImage)
    cv2.waitKey(0)

#Canny Edge detector
def tImageEdgeDetect(x="", y=150, z=200):
    imageReader = cv2.imread(x)
    # 100,100 is the threshhold
    edgeCanny = cv2.Canny(imageReader, y, z)
    # iteration changes thickness
    imageDialation = cv2.dilate(edgeCanny, kernel, iterations=1)
    imageErosion = cv2.erode(imageReader, kernel, iterations=1)
    diaEro = cv2.erode(edgeCanny, kernel, iterations=1)
    cv2.imshow("Canny Edge Detector", edgeCanny)
    cv2.imshow("Dialation Erosion", diaEro)
    cv2.imshow("Dialated even more", imageDialation)
    cv2.imshow("Eroded Image", imageErosion)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#----------------------------------------------------------------------
#   cv2 VIDEO RELATED FUNCTIONS
#----------------------------------------------------------------------

def tVideoRead(x=""):
    watcher = cv2.VideoCapture(x)
    watching = True
    while watching:
        guard, frame = watcher.read()
        cv2.imshow("Video Reader", frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    watching = False
    cv2.destroyAllWindows()

#----------------------------------------------------------------------
#----------------------------------------------------------------------

##################### HAND DETECTOR #######################
#d:         os.system('pip install mediapipe') 
#d:         os.system('pip install opencv-python') 
###########################################################

#----------------------------------------------------------------------
#----------------------------------------------------------------------
class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []
    def findHands(self, img, draw=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                            self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True):
        """
        Finds landmarks of a single hand and puts them in a list
        in pixel format. Also finds the bounding box around the hand.
        :param img: main image to find hand in
        :param handNo: hand id if more than one hand detected
        :param draw: Flag to draw the output on the image.
        :return: list of landmarks in pixel format; bounding box
        """
        xList = []
        yList = []
        bbox = []
        bboxInfo =[]
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                px, py = int(lm.x * w), int(lm.y * h)
                xList.append(px)
                yList.append(py)
                self.lmList.append([px, py])
                if draw:
                    cv2.circle(img, (px, py), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + (bbox[3] // 2)
            bboxInfo = {"id": id, "bbox": bbox,"center": (cx, cy)}
            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                            (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                            (0, 255, 0), 2)
        return self.lmList, bboxInfo
    def fingersUp(self):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        if self.results.multi_hand_landmarks:
            myHandType = self.handType()
            fingers = []
            # Thumb
            if myHandType == "Right":
                if self.lmList[self.tipIds[0]][0] > self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if self.lmList[self.tipIds[0]][0] < self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # 4 Fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers
    def findDistance(self, p1, p2, img, draw=True):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1 - Index of Landmark 1.
        :param p2: Point2 - Index of Landmark 2.
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                Image with output drawn
                Line information
        """
        if self.results.multi_hand_landmarks:
            x1, y1 = self.lmList[p1][0], self.lmList[p1][1]
            x2, y2 = self.lmList[p2][0], self.lmList[p2][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if draw:
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]
    def handType(self):
        """
        Checks if the hand is left or right
        :return: "Right" or "Left"
        """
        if self.results.multi_hand_landmarks:
            if self.lmList[17][0] < self.lmList[5][0]:
                return "Right"
            else:
                return "Left"


def MasterHandDetector(x=""):
    # 'x' is the source/takes source as input.
    watcher = cv2.VideoCapture(x)
    detector = HandDetector(maxHands=1, detectionCon=0.7)
    watching = True
    while True:
        success, frame = watcher.read()
        handerson = detector.findHands(frame)
        lmlist, bbox = detector.findPosition(handerson)
        cv2.imshow("M: Hand Detector", handerson)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    watching = False
    cv2.destroyAllWindows()

#----------------------------------------------------------------------
#----------------------------------------------------------------------
######################## HOR DASS AAMB BHALDI? ########################
#----------------------------------------------------------------------
#----------------------------------------------------------------------


############# ALL FUNCTION LISTED THROUGH FUNCTION HELPER FUNCTIONS ###############
############# ALL FUNCTION LISTED THROUGH FUNCTION HELPER FUNCTIONS ###############
def usage():
    print(fpfill)
    print("     All functions are listed below, use as you may.")
    print(fpfill)
    print('\n')
    counter = 1
    for key in functions_dict:
        print(counter, ":", key, "::", functions_dict[key])
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
        print(counter, ":", key, "::", bot_dict[key])
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

#----------------------------------------------------------------------
#----------------------------------------------------------------------
######################## HOR DASS AAMB BHALDI? ########################
#----------------------------------------------------------------------
#----------------------------------------------------------------------

