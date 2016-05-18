#!/usr/bin/python
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

import os
import sys
import termios
import tty
import pigpio
import time
from threading import Thread
import json
from pprint import pprint

def loadSetting():
    global state
    global bright

    with open("properties.json") as data_file:
        data = json.load(data_file)
        pprint(data)
        state = data["state"]
        bright = data["brightness"]


if not len(sys.argv) < 1:
    r = 255
    g = 255
    b = 255
else:
    r = int(sys.argv[1])
    g = int(sys.argv[2])
    b = int(sys.argv[3])


pi = pigpio.pi()



def setLights(pin, brightness):
    global rCurrent
    global gCurrent
    global bCurrent

    realBrightness = brightness * (round(bright / 100))
    pi.set_PWM_dutycycle(pin, realBrightness)

    if pin == RED_PIN:
        rCurrent = realBrightness
        print("Setting red to: %s" % rCurrent)
    elif pin == GREEN_PIN:
        gCurrent = realBrightness
        print("Setting green to: %s" % gCurrent)
    elif pin == BLUE_PIN:
        bCurrent = realBrightness
        print("Setting blue to: %s" % bCurrent)
    else:
        print("No pin!")

def redTransition(r):
    rDelta = 1 + abs(rCurrent - r)
    rSteps = float(TRANSITIONFADETIME) / (float(rDelta) / float(1))
    while rCurrent < r:
        for i in range(0, rDelta):
            rUpdate = updateColor(rCurrent, +TRANSITIONSTEPS)
            setLights(RED_PIN, rUpdate)
            time.sleep(rSteps)
    while rCurrent > r:
        for i in range(0, rDelta):
            rUpdate = updateColor(rCurrent, -TRANSITIONSTEPS)
            setLights(RED_PIN, rUpdate)
            time.sleep(rSteps)
    if rCurrent == r:
        print("RED DONE!")
    else:
        print("RED ERROR!")

def greenTransition(g):
    gDelta = 1 + abs(gCurrent - g)
    gSteps = float(TRANSITIONFADETIME) / (float(gDelta) / float(1))
    while gCurrent < g:
        for i in range(0, gDelta):
            gUpdate = updateColor(gCurrent, +TRANSITIONSTEPS)
            setLights(GREEN_PIN, gUpdate)
            time.sleep(gSteps)
    while gCurrent > g:
        for i in range(0, gDelta):
            gUpdate = updateColor(gCurrent, -TRANSITIONSTEPS)
            setLights(GREEN_PIN, gUpdate)
            time.sleep(gSteps)
    if gCurrent == g:
        print("GREEN DONE!")
    else:
        print("GREEN ERROR!")
        
def blueTransition(b):
    bDelta = 1 + abs(bCurrent - b)
    bSteps = float(TRANSITIONFADETIME) / (float(bDelta) / float(1))
    while bCurrent < b:
        for i in range(0, bDelta):
            bUpdate = updateColor(bCurrent, +TRANSITIONSTEPS)
            setLights(BLUE_PIN, bUpdate)
            print("%s %s %s" % (b, bSteps, bUpdate))
            time.sleep(bSteps)
    while bCurrent > b:
        for i in range(0, bDelta):
            bUpdate = updateColor(bCurrent, -TRANSITIONSTEPS)
            setLights(BLUE_PIN, bUpdate)
            print("%s %s %s" % (b, bSteps, bUpdate))
            time.sleep(bSteps)
    if bCurrent == b:
        print("BLUE DONE!")
    else:
        print("BLUE ERROR!")


def doTransition(r, g, b):
    Thread(target=redTransition, args=(r,)).start()
    Thread(target=greenTransition, args=(g,)).start()
    Thread(target=blueTransition, args=(b,)).start()
    # Thread(target=greenTransition, args=(g,)).join()
    # Thread(target=blueTransition, args=(b,)).join()

def updateColor(color, step):
    color += step
    # test
    print("%s %s" % (color,step))

    if color > 255:
        return 255
    if color < 0:
        return 0

    return color


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
setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)
# print("%s %s %s" % (r, g, b))
doTransition(r, g, b)
time.sleep(2)

pi.stop()
