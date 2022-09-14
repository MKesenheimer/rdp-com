#!/usr/bin/env python3
# -*- conding: utf-8 -*-

import numpy as np
import cv2
from mss import mss
from PIL import Image
import sys
import os
import base64

def average(lst):
    return sum(lst) / len(lst)

def frombits(bits, nbits = 8):
    chars = []
    for b in range(int(len(bits) / nbits)):
        byte = bits[b * nbits : (b + 1) * nbits]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 8)))
        #print(chars)
    return ''.join(chars)

def inRange(x, lower, upper):
    if x >= lower and x < upper:
        return 0
    else:
        return 1

def colorToBit(color):
    values = [inRange(x, 0, 127) for x in color]
    #print(values)
    return values[2] + values[1] * 2 + values[0] * 4

# main program
def main():
    pack = 24 # pack * 3 bits per line
    number_of_bits = 3 * pack + 1
    ps_character_height = 14
    ps_character_width = 7
    margin = 50
    width = number_of_bits * ps_character_width + margin
    height = ps_character_width + margin
    bounding_box = {'top': 500, 'left': 800, 'width': width, 'height': height}

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
            pixel = line[int(margin / 2 + ps_character_width / 2 + ps_character_width * i)]
            bit = colorToBit(pixel)
            byte += [bit]

        if not calibration_done or always_monitor:
            img_arry = cv2.resize(img_arry, (width * 2, height * 2))
            cv2.imshow('screen', img_arry)

        #print("{}".format(byte[0:number_of_bits - 1]))
        ##print("{}".format(frombits(byte[0:number_of_bits - 1], number_of_bits - 1)))
        characterpack = ""
        for i in range(0, pack):
            characterpack += frombits(byte[3 * i: 3 * (i + 1)], 3)
        
        #print("{}, {}, {}, {}".format(characterpack, lastcharpack, clockbit, lastclockbit))
        clockbit = byte[number_of_bits - 1]
        if lastcharpack == characterpack and clockbit == 7 and lastclockbit == 0:
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
