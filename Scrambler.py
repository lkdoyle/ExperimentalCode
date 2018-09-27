# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
Created on Thu Sep 20 16:14:30 2018
image scrambler prototype to focus on low level visual features
@author: Logan
"""
import os, random
from PIL import Image

files = []

#script to fetch  from a stimulus directory
def getImages(directory):
    #walk top down from current directory and return paths of images to pass on
    for (path, dirnames, filenames) in os.walk(directory):
        files.extend(os.path.join(path, name) for name in filenames)

    return(files)

def imageResize(img, width, height):
    print("resizing: " +img)
    pic = Image.open(img)
    pic = pic.resize((width, height), Image.ANTIALIAS)
    pic.save(img)

def scrambleImage(img, boxSize):
    print("scrambling: " +img)
    #open the image to work on it
    pic = Image.open(img)
    #width and height are saved to vars
    width, height = pic.size
    
        
    #find out how many boxes fit into the width and height (best to select % 0s)
    numX = int(width/boxSize)
    numY = int(height/boxSize)
    
    if boxSize % numX != 0 or boxSize % numY != 0:
        print("images are not evenly divided by scramble boxes, please resize")
        return False
    
    boxPos = []
    #create an array of all possible box 0,0 positions
    for i in range(0, width, boxSize):
        for j in range(0, height, boxSize):
            boxPos.append((i, j, i + boxSize, j + boxSize))
    
    posPos = len(boxPos)

    i = 0
    
    #iterate through the entirety of the image
    for x in range(numX):
        #checking to see which box to write to if it is a multiple move to next box
        for y in range(numY):
            thisBox = boxPos[i]
            randBox = boxPos[random.randint(0,posPos-1)]
            
            #get pixel values from first box
            box1 = pic.crop(thisBox)
            #get pixcel values from random box
            box2 = pic.crop(randBox)
            #print("this is randBox: " + randBox)
            
            randCords = (randBox[0], randBox[1])
            thisCords = (thisBox[0], thisBox[1])
            
            print(randCords)
            print(thisCords)
            
            pic.paste(box1, randCords)
            pic.paste(box2, thisCords)
            
            i += 1
            
            #swap the pixel values  of each
    
    newName = img.replace(".jpg", "scrambled.png")
    pic.save(newName)
    return


def main(imgSize, scrambleSize):
    pipeline = getImages('stimuli')

    for i in pipeline:
        imageResize(i, imgSize, imgSize)
        scrambleImage(i, scrambleSize)
    
if __name__ == '__main__':
        main(500, 50)
    
