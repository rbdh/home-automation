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

from thread import start_new_thread

bright = 255

total = len(sys.argv)
arg1 = str(sys.argv[1])
arg2 = str(sys.argv[2])
arg3 = str(sys.argv[3])

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
        print
        "Setting red to: %s" % rCurrent
    elif pin == GREEN_PIN:
        gCurrent = realBrightness
        print
        "Setting green to: %s" % gCurrent
    elif pin == BLUE_PIN:
        bCurrent = realBrightness
        print
        "Setting blue to: %s" % bCurrent
    else:
        print
        "No pin"


def redTransition(r):
    while rCurrent < r:
        rDelta = r - rCurrent
        rSteps = float(TRANSITIONFADETIME / (rDelta / TRANSITIONSTEPS))
        r = updateColor(r, +TRANSITIONSTEPS)
        setLights(RED_PIN, r)
        time.sleep(rSteps)
    while rCurrent > r:
        rDelta = rCurrent - r
        rSteps = float(TRANSITIONFADETIME / (rDelta / TRANSITIONSTEPS))
        r = updateColor(r, -TRANSITIONSTEPS)
        setLights(RED_PIN, r)
        time.sleep(rSteps)


def greenTransition(g):
    while gCurrent < g:
        gDelta = g - gCurrent
        gSteps = float(TRANSITIONFADETIME / (gDelta / TRANSITIONSTEPS))
        g = updateColor(g, +TRANSITIONSTEPS)
        setLights(GREEN_PIN, g)
        time.sleep(gSteps)
    while gCurrent > g:
        gDelta = gCurrent - g
        gSteps = float(TRANSITIONFADETIME / (gDelta / TRANSITIONSTEPS))
        g = updateColor(g, -TRANSITIONSTEPS)
        setLights(GREEN_PIN, g)
        time.sleep(gSteps)


def blueTransition(b):
    while bCurrent < b:
        bDelta = b - bCurrent
        bSteps = float(TRANSITIONFADETIME / (bDelta / TRANSITIONSTEPS))
        b = updateColor(b, +TRANSITIONSTEPS)
        setLights(BLUE_PIN, b)
        time.sleep(bSteps)
    while bCurrent > b:
        bDelta = bCurrent - b
        bSteps = float(TRANSITIONFADETIME / (bDelta / TRANSITIONSTEPS))
        b = updateColor(b, -TRANSITIONSTEPS)
        setLights(BLUE_PIN, b)
        time.sleep(bSteps)


def doTransition(r, g, b):
    redthread = threading.Thread(target=redTransition(r))
    greenthread = threading.Thread(target=greenTransition(g))
    bluethread = threading.Thread(target=blueTransition(b))

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


setLights(RED_PIN, r)
setLights(GREEN_PIN, g)
setLights(BLUE_PIN, b)
time.sleep(2)
doTransition(103, 100, 60)

pi.stop()
