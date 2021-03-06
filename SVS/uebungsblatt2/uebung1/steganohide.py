#!/usr/bin/python
# -*- coding: utf8 -*-

import sys #Zum Abbrechen des Programms
import os.path #für die Prüfung der Existenz von Dateien
from PIL import Image
import binascii

#Lesen der Textdatei
def readTxtFile(file):
    fobj = open(file)
    result = ""
    for line in fobj:
        result += line.rstrip()#.lower()
    fobj.close()

    return result

#Prüft, ob Textdatei und Bild existieren
def checkFileExistence(txt, img):
    txtExist = False
    imgExist = False
    if os.path.isfile(txt):
        txtExist = True
    else:
        sys.exit(txt + ' not exist!')

    if os.path.isfile(img):
        imgExist = True
    else:
        sys.exit(img + ' not exist')

    if txtExist and imgExist:
        return True
    else:
        return False

def rgbCodeToHexcode(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hexcodeTorgbCode(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))

def stringToBinary(message):
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]

def binaryToString(binary):
    message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
    return message

def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

#Schreiben in Bild-Datei
def writeTxtInImage(filename, message):
    img = Image.open(filename)
    binary = stringToBinary(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        digit = 0
        for item in datas:
            if (digit < len(binary)):
                newpix = encode(rgbCodeToHexcode(item[0], item[1], item[2]), binary[digit])
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hexcodeTorgbCode(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item)

        img.putdata(newData)

        img.save(filename + ".ste", "PNG")
        return True

    return False


#Lesen aus Bild-Datei
def readTxtFromImage(filename):
    img = Image.open(filename + ".ste")
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(rgbCodeToHexcode(item[0], item[1], item[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if (binary[-16:] == '1111111111111110'):
                    return binaryToString(binary[:-16])

        return binaryToString(binary)
    return False

#Auf Anzahl der Parameter prüfen
if len(sys.argv) != 3:
    sys.exit('Wrong count of parameters. We need two parameters - example: steganohide.py text.txt bild.bmp')

txtFilename = sys.argv[1]
imgFilename = sys.argv[2]

#Auf Existenz prüfen, falls erforgreich dann weiter
if checkFileExistence(txtFilename, imgFilename):
    if writeTxtInImage(imgFilename, readTxtFile(txtFilename)):
        print 'Write text in image was successfull!'
        if readTxtFromImage(imgFilename) != False:
            print readTxtFromImage(imgFilename)
        else:
            sys.exit('ERROR! Read text in image failed!')
    else:
        sys.exit('ERROR! Write text in image failed!')


# Let suppose an image has a size of 1200 * 800 pixel than 1200 x 800= 960,000 pixel
# so for 24-bit scheme that contain 3 bytes it would become 960,000 x 3 =28,80000 bytes and 1 byte consist of 8 bits so 2880000 x 8 = 23040000 bits