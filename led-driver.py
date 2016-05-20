#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# -----------------------------------------------------
# File        fading.py
# Authors     rbdh
# License     GPLv3
# Web         http://www.indianx.nl
# -----------------------------------------------------
#
# Copyright (C) 2016 rbdh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#
# This script needs running pigpio (http://abyz.co.uk/rpi/pigpio/)


###### CONFIGURE THIS ######

# The Pins. Use Broadcom numbers.
RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 24

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.
TRANSITIONSTEPS = 1
FADESTEPS = 1
TRANSITIONFADETIME = 1
MAXBRIGHT = 255
###### END ######

# import os
# import termios
# import tty
# import pigpio
import sys
import time
from threading import Thread
import json
from pprint import pprint

def loadSetting():
    global state
    global brightness

    with open("properties.json") as data_file:
        data = json.load(data_file)
        pprint(data)
        state = data["state"]
        brightness = data["brightness"]

# run if no arguments
if not len(sys.argv) < 1:
    r = 57
    g = 152
    b = 156
else:
    r = int(sys.argv[1])
    g = int(sys.argv[2])
    b = int(sys.argv[3])


# pi = pigpio.pi()

def getRealBrightness(brightnessLevel):
    global realBrightness
    realBrightness = (brightnessLevel * (round(brightness / 100)))
    return realBrightness


def setLights(pin, brightnessLevel):
    global rCurrent
    global gCurrent
    global bCurrent
    global cCurrent

    # pi.set_PWM_dutycycle(pin, getRealBrightness(brightnessLevel))

    if pin == RED_PIN:
        rCurrent = getRealBrightness(brightnessLevel)
        cCurrent = rCurrent
        print("Setting red to: %s" % rCurrent)
    elif pin == GREEN_PIN:
        gCurrent = getRealBrightness(brightnessLevel)
        cCurrent = gCurrent
        print("Setting green to: %s" % gCurrent)
    elif pin == BLUE_PIN:
        bCurrent = getRealBrightness(brightnessLevel)
        cCurrent = bCurrent
        print("Setting blue to: %s" % bCurrent)
    else:
        print("No pin!: " + pin)


def Transition(color, value):
    print("KLEUR: %s " % (color))
    global PIN

    if color == "red":
        # print("rCurrent %s" % rCurrent)
        PIN = RED_PIN
    elif color == "green":
        # print("gCurrent %s" % gCurrent)
        PIN = GREEN_PIN
    elif color == "blue":
        # print("bCurrent %s" % bCurrent)
        PIN = BLUE_PIN
    else:
        print("No valid color")

    delta = abs(cCurrent - value)
    if delta == 0:
        print("Nothing to do for %s" % color)
    else:
        steps = float(TRANSITIONFADETIME) / (float(delta) / float(TRANSITIONSTEPS))
        print("Delta: %s , Steps %s" % (delta,  steps))
        running(delta, steps, value)


def running(delta, steps, value):
    while cCurrent < value:
        for i in range(0, delta):
            if cCurrent == value or cCurrent >= 255:
                value = cCurrent
                print("done!")
                break
                # pi.stop()
            else:
                cUpdate = updateColor(cCurrent, +TRANSITIONSTEPS)
                setLights(PIN, cUpdate)
                time.sleep(steps)
    while cCurrent > value:
        for i in range(0, delta):
            if cCurrent == value or cCurrent >= 255:
                value = cCurrent
                break
                print("done!")
                # pi.stop()
            else:
                cUpdate = updateColor(cCurrent, -TRANSITIONSTEPS)
                setLights(PIN, cUpdate)
                time.sleep(steps)

# def redTransition(r):
#     rDelta = 1 + abs(rCurrent - r)
#     rSteps = float(TRANSITIONFADETIME) / (float(rDelta) / float(TRANSITIONSTEPS))
#     print("rDelta: %s, rSteps %s" % (rDelta, rSteps))
#     while rCurrent < r:
#         for i in range(0, rDelta):
#             if (rCurrent == r or rCurrent >= 255):
#                 r = rCurrent
#                 print("RED DONE!")
#                 # pi.stop()
#             else:
#                 rUpdate = updateColor(rCurrent, +TRANSITIONSTEPS)
#                 setLights(RED_PIN, rUpdate)
#                 time.sleep(rSteps)
#     while rCurrent > r:
#         for i in range(0, rDelta):
#             if (rCurrent == r or rCurrent >= 255):
#                 r = rCurrent
#                 print("RED DONE!")
#                 # pi.stop()
#             else:
#                 rUpdate = updateColor(rCurrent, -TRANSITIONSTEPS)
#                 setLights(RED_PIN, rUpdate)
#                 time.sleep(rSteps)
#     if (rCurrent == r or rCurrent >= 255):
#         r = rCurrent
#         print("RED DONE!")
#         # pi.stop()
#     else:
#         print("RED ERROR!")
#
# def greenTransition(g):
#     gDelta = 1 + abs(gCurrent - g)
#     gSteps = float(TRANSITIONFADETIME) / (float(gDelta) / float(TRANSITIONSTEPS))
#     while gCurrent < g:
#         for i in range(0, gDelta):
#             if (gCurrent == g or gCurrent >= 255):
#                 g = gCurrent
#                 print("GREEN DONE!")
#                 # pi.stop()
#             else:
#                 gUpdate = updateColor(gCurrent, +TRANSITIONSTEPS)
#                 setLights(GREEN_PIN, gUpdate)
#                 time.sleep(gSteps)
#     while gCurrent > g:
#         for i in range(0, gDelta):
#             if (gCurrent == g or gCurrent >= 255):
#                 g = gCurrent
#                 print("GREEN DONE!")
#                 # pi.stop()
#             else:
#                 gUpdate = updateColor(gCurrent, -TRANSITIONSTEPS)
#                 setLights(GREEN_PIN, gUpdate)
#                 time.sleep(gSteps)
#
# def blueTransition(b):
#     bDelta = 1 + abs(bCurrent - b)
#     bSteps = float(TRANSITIONFADETIME) / (float(bDelta) / float(TRANSITIONSTEPS))
#     while bCurrent < b:
#         for i in range(0, bDelta):
#             if (bCurrent == b or bCurrent >= 255):
#                 b = bCurrent
#                 print("BLUE DONE!")
#                 # pi.stop()
#             else:
#                 bUpdate = updateColor(bCurrent, +TRANSITIONSTEPS)
#                 setLights(BLUE_PIN, bUpdate)
#                 # print("%s %s %s" % (b, bSteps, bUpdate))
#                 time.sleep(bSteps)
#
#     while bCurrent > b:
#         for i in range(0, bDelta):
#             if (bCurrent == b or bCurrent >= 255):
#                 b = bCurrent
#                 print("BLUE DONE!")
#                 # pi.stop()
#             else:
#                 bUpdate = updateColor(bCurrent, -TRANSITIONSTEPS)
#                 setLights(BLUE_PIN, bUpdate)
#                 # print("%s %s %s" % (b, bSteps, bUpdate))
#                 time.sleep(bSteps)


def doTransition(redValue, greenValue, blueValue):
    # Transition("red", r)
    # Transition("green", g)
    # Transition("blue", b)
    Thread(target=Transition, args=("red", redValue,)).start()
    Thread(target=Transition, args=("green", greenValue, )).start()
    Thread(target=Transition, args=("blue", blueValue,)).start()
    Thread(target=Transition, args=("green", greenValue,)).join()
    Thread(target=Transition, args=("blue", blueValue,)).join()


def updateColor(colorUpdate, step):
    x = colorUpdate + step
    print("Getting %s, doing %s" % (colorUpdate,step))
    if x >= 255:
        return 255
    elif x <= 0:
        return 0
    # print("colorUpdate: %s" % colorUpdate)
    return x



def fadeColor(state):
    while state == True:
        print("Red %s, Green %s, Blue %s" % (rCurrent, gCurrent, bCurrent))
        if rCurrent == 255 and bCurrent == 0 and gCurrent < 255:
            doTransition(255, 255, 0)
        elif gCurrent == 255 and bCurrent == 0 and rCurrent > 0:
            doTransition(0, 255, 0)
        elif rCurrent == 0 and gCurrent == 255 and bCurrent < 255:
            doTransition(0, 255, 255)
        elif rCurrent == 0 and bCurrent == 255 and gCurrent > 0:
            doTransition(0, 0, 255)
        elif gCurrent == 0 and bCurrent == 255 and rCurrent < 255:
            doTransition(255, 0, 255)
        elif rCurrent == 255 and gCurrent == 0 and bCurrent > 0:
            doTransition(255, 0, 0)
        elif rCurrent == 0 and bCurrent == 0 and gCurrent == 0:
            setLights(RED_PIN, 255)

loadSetting()
setLights(RED_PIN, 150)
setLights(GREEN_PIN, 150)
setLights(BLUE_PIN, 150)
doTransition(r, g, b)
# fadeColor(True)
time.sleep(2)
