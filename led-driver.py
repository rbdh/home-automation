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
TRANSITIONFADETIME = 1

###### END ######

import os
import sys
import termios
import tty
import pigpio
import time
import threading

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

total = len(sys.argv)
arg1 = int(str(sys.argv[1]))
arg2 = int(str(sys.argv[2]))
arg3 = int(str(sys.argv[3]))
bright = 255

if total == 0:
    r = 10
    g = 10
    b = 10
else:
    r = arg1
    g = arg2
    b = arg3


# brightChanged = False
# abort = False
# state = True

pi = pigpio.pi()


def setLights(pin, brightness):
    global rCurrent
    global gCurrent
    global bCurrent

    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)

    if pin == RED_PIN:
        rCurrent = realBrightness
        # print("Setting red to: %s" % rCurrent)
    elif pin == GREEN_PIN:
        gCurrent = realBrightness
        # print("Setting green to: %s" % gCurrent)
    elif pin == BLUE_PIN:
        bCurrent = realBrightness
        # print("Setting blue to: %s" % bCurrent)
    else:
        print("No pin!")

def redTransition(r):
    rDelta = 1 + abs(rCurrent - r)
    rSteps = float(TRANSITIONFADETIME) / (float(int(rDelta)) / float(1))
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
    else:
        print("DONE!")

def greenTransition(g):
    gDelta = 1 + abs(gCurrent - g)
    gSteps = float(TRANSITIONFADETIME) / (float(int(gDelta)) / float(1))
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
    else:
        print("DONE!")
        
def blueTransition(b):
    bDelta = 1 + abs(bCurrent - b)
    bSteps = float(TRANSITIONFADETIME) / (float(int(bDelta)) / float(1))
    while bCurrent < b:
        for i in range(0, bDelta):
            bUpdate = updateColor(bCurrent, +TRANSITIONSTEPS)
            setLights(BLUE_PIN, bUpdate)
            # print("%s %s %s" % (b, bSteps, bUpdate))
            time.sleep(bSteps)
    while bCurrent > b:
        for i in range(0, bDelta):
            bUpdate = updateColor(bCurrent, -TRANSITIONSTEPS)
            setLights(BLUE_PIN, bUpdate)
            # print("%s %s %s" % (b, bSteps, bUpdate))
            time.sleep(bSteps)
    else:
        print("DONE!")


def doTransition(r, g, b):
    redthread = FuncThread(redTransition, r)
    greenthread = FuncThread(greenTransition, g)
    bluethread = FuncThread(blueTransition, b)

    redthread.start()
    greenthread.start()
    bluethread.start()
    redthread.join()
    greenthread.join()
    bluethread.join()

def updateColor(color, step):
    color += step

    if color > 255:
        return 255
    if color < 0:
        return 0

    return color


setLights(RED_PIN, 255)
setLights(GREEN_PIN, 255)
setLights(BLUE_PIN, 255)
time.sleep(1)
doTransition(r, g, b)

pi.stop()
