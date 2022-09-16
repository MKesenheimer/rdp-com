#!/usr/bin/env python3
# -*- conding: utf-8 -*-
# receiver.py
# Copyright September 2022, Matthias Kesenheimer

import numpy as np
import cv2
from mss import mss
from PIL import Image
import sys
import os
import base64

Black = [0, 0, 0, 255]
Red = [0, 0, 255, 255]
Green = [0, 255, 0, 255]
Yellow = [0, 255, 255, 255]
Blue = [255, 0, 0, 255]
Magenta = [255, 0, 255, 255]
Cyan = [255, 255, 0, 255]
White = [255, 255, 255, 255]
DarkGray = [128, 128, 128, 255]
DarkRed =  [0, 0, 128, 255]
DarkGreen =  [0, 128, 0, 255]
DarkYellow = [240, 240, 240, 255]
DarkBlue = [128, 0, 0, 255]
DarkMagenta = [85, 37, 0, 255]
DarkCyan =  [128, 128, 0, 255]
Gray = [192, 192, 192, 255]
Colors = [Black, Red, Green, Yellow, Blue, Magenta, Cyan, White, DarkGray, DarkRed, DarkGreen, DarkYellow, DarkBlue, DarkMagenta, DarkCyan, Gray]

def average(lst):
    return sum(lst) / len(lst)

def frombits(bits, nbits = 8):
    chars = []
    for b in range(int(len(bits) / nbits)):
        byte = bits[b * nbits : (b + 1) * nbits]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 16)))
    return ''.join(chars)

def inRange(x):
    if x > 170 and x <= 255:
        return 1
    else:
        return 0

def colorToBit(color):
    values = [inRange(x) for x in color]
    return values[2] + values[1] * 2 + values[0] * 4

def distance(l1, l2):
    return np.linalg.norm(l1 - l2)

def colorToBit2(color):
    d = []
    for c in Colors:
        d += [distance(color, c)]
    argmin = np.argmin(d)
    argmin = "{0:x}".format(argmin)
    return argmin

# main program
def main():
    pack = 24 # pack * 2 bits per line
    number_of_bits = 2 * pack + 1
    ps_character_height = 14
    ps_character_width = 7
    margin = 50
    width = number_of_bits * ps_character_width + margin
    height = ps_character_width + margin
    bounding_box = {'top': 500, 'left': 2800, 'width': width, 'height': height}

    # get an instance of the screen shot engine
    sct = mss()

    stringstream = ""
    characterpack = ""
    lastcharpack = ""
    clockbit = 0
    lastclockbit = 1
    always_monitor = True
    calibration_done = False
    while True:
        sct_img = sct.grab(bounding_box)
        img_arry = np.array(sct_img)
        img_arry = cv2.resize(img_arry, (width, height)) # necessary due to HDPI rescaling
        
        if not calibration_done or always_monitor:
            margin2 = int(margin / 2)
            start_point = (margin2, margin2)
            end_point = (width - margin2, height - margin2)
            color = (0, 0, 255)
            thickness = 1
            img_arry = cv2.rectangle(img_arry, start_point, end_point, color, thickness)
            
            #print("margin = {}".format(int(margin / 2)))
            #print("strt = {}, end  = {}".format(start_point, end_point))
            #print("widt = {}, hght = {}".format(sct_img.width, sct_img.height))
            #print("widt = {}, hght = {}".format(width, height))
            
        rows = len(img_arry)
        line = img_arry[int(rows / 2)]
        byte = []
        for i in range(0, number_of_bits):
            # pixel is an array of four values: blue, green, red, alpha (=transparency); BGRA
            pixel = line[int(margin / 2 + ps_character_width / 2 + ps_character_width * i)]
            bit = colorToBit2(pixel)
            #print(bit)
            byte += [bit]

        if not calibration_done or always_monitor:
            img_arry = cv2.resize(img_arry, (width * 2, height * 2))
            cv2.imshow('screen', img_arry)

        #print("{}".format(byte[0:number_of_bits - 1]))
        #print("{}".format(frombits(byte[0:number_of_bits - 1], 2)))
        characterpack = ""
        for i in range(0, pack):
            characterpack += frombits(byte[2 * i: 2 * (i + 1)], 2)
        
        #print("{}, {}, {}, {}".format(characterpack, lastcharpack, clockbit, lastclockbit))
        clockbit = byte[number_of_bits - 1]
        if lastcharpack == characterpack and clockbit == "{0:x}".format(7) and lastclockbit == "{0:x}".format(0):
            calibration_done = True
            stringstream += characterpack
            print("{}".format(stringstream))
        lastcharpack = characterpack
        lastclockbit = clockbit

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            print("Writing received data to out.bin")
            content = base64.b64decode(stringstream)
            with open('out.bin', 'wb') as f:
                f.write(content)

            cv2.destroyAllWindows()
            print("Done.")
            break

# main program
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Done.")
        cv2.destroyAllWindows()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
