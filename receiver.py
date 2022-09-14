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
        byte = bits[b*nbits:(b+1)*nbits]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

# main program
def main():
    pack = 8 # number of bits packed
    number_of_bits = 8 * pack + 1 # pack * 8 bits per line + one clock bit
    ps_character_height = 16
    ps_character_width = 12
    margin = 50
    width = number_of_bits * ps_character_width + margin
    height = ps_character_width + margin
    bounding_box = {'top': 500, 'left': 2900, 'width': width, 'height': height}

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
        
        if not calibration_done or always_monitor:
            start_point = (int(margin / 2), int(margin  / 2))
            end_point = (int(width - margin / 2), int(height - margin / 2))
            color = (0, 0, 255)
            thickness = 1
            img_arry = cv2.rectangle(img_arry, start_point, end_point, color, thickness)
        
        rows = len(img_arry)
        cols = len(img_arry[0])

        #print("rows = {}, cols = {}".format(rows, cols))
        line = img_arry[int(rows / 2)]
        byte = []
        for i in range(0, number_of_bits):
            pixel = line[int(margin / 2 + ps_character_width / 2 + ps_character_width * i)]
            # average all color channels
            avg = int(average(pixel))
            bit = 0
            if avg >= 0 and avg < 255 / 3:
                bit = 0
            if avg > 255 * 2/3 and avg <= 255:
                bit = 1
            byte += [bit]

        if not calibration_done or always_monitor:
            img_arry = cv2.resize(img_arry, (width * 2, height * 2)) 
            cv2.imshow('screen', img_arry)

        #print("{}".format(byte[0:number_of_bits - 1]))
        #print("{}".format(frombits(byte[0:number_of_bits - 1], number_of_bits - 1)))
        characterpack = ""
        for i in range(0, pack):
            characterpack += frombits(byte[8 * i: 8 * (i + 1)])

        clockbit = byte[number_of_bits - 1]
        if lastcharpack == characterpack and clockbit == 1 and lastclockbit == 0:
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