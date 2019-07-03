# -*- encoding: UTF-8 -*-

import sys
import numpy as np
import argparse
import datetime
import cv2
from naoqi import ALProxy
from pyzbar import pyzbar
#import initDomino
#import mainDomino
import time

def Scan(state):
    global tracker
    global cameraNo, bar, z, headMovement, posBar
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
            help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())

    try:
        # Proxy to camera and motion
        print("Starting video stream...")
        camera = ALProxy("ALVideoDevice", "Mario.local", 9559)
        headMovement = ALProxy("ALMotion", "Mario.local", 9559)
        tracker = ALProxy("ALTracker", "Mario.local", 9559)
    except:
        print("Error connecting to proxies")

    csv = open(args["output"], "w")
    found = set()
    targetName = "Face"
    faceWidth = 0.1 # default
    tracker.registerTarget(targetName, faceWidth)
    # Subscribe to camera
    if state == "unsure":
        cameraNo = 0
    elif state == "deal" or state == "boneyard":
        cameraNo = 1
    # mainDomino.cameraNo
    # mainDomino.cameraNo
    AL_kQVGA = 3 # 1280x960
    AL_kBGRColorSpace = 13

    try:
        captureDevice = camera.subscribeCamera("captureDevice", cameraNo, AL_kQVGA, AL_kBGRColorSpace, 10)
    except:
        print("Error subscribing to camera")
    # init = False
    # Create image
    width = 1280
    height = 960
    image = np.zeros((height, width, 3), np.uint8)

    bar = []
    posBar = []
    
    while True: 
        # Position head at center
        moveHeadCenter() 


        # Get the image
        try:
            result = camera.getImageRemote(captureDevice)
        except:
            print("Error getting image remotely")

        if result == None:
            print 'Error: Cannot capture.'
        elif result[6] == None:
            print 'Error: No image data string.'
        else:
            # Translate value to mat
            values = map(ord, list(result[6]))
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3
                    
            # if cameraNo == 1:
            #     tiles = image[300:800, 0:1280]
            # else:
            tiles = image

            grey = cv2.cvtColor(tiles, cv2.COLOR_BGR2GRAY) # convert image to grey
            ret,thresh1 = cv2.threshold(grey,127,255,cv2.THRESH_BINARY)
            ret3,th3 = cv2.threshold(grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            
            barcodes = pyzbar.decode(th3) # find and decode barcodes

            # Loop over detected barcodes
            for barcode in barcodes:

                (x, y, w, h) = barcode.rect
                # Convert data into string
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                
                # Put barcode data, x and y coords on the image
                text = "{}".format(barcodeData)
                cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
 
                if barcodeData not in found:
                    found.add(barcodeData)
                    # Put new found barcodes into an array                        
                    barcode = map(int, barcodeData) 
                    # Put the barcode x,y position into array
                    posXYZ = [x, y, z]
                    # Add info to barcode position array, so we know where the barcode was found
                    if len(barcode) > 2:
                        break
                    else:
                        bar.insert(0, barcode)
                        posBar.insert(0, posXYZ)
                    print bar
                    print posBar
                    #moveHeadLeft()
                   # moveHeadRight()

                    if state == "deal":
                        # If we haven't seen all tiles that have been dealt, move head from side to side.
                        # if len(bar) < 7:
                        #     moveHeadLeft()
                        #     moveHeadRight()
                        # If we have seen them all, then stop video stream.
                        if len(bar) == 7:

                            # tracker.track(targetName)
                            camera.releaseImage(captureDevice)
                            camera.unsubscribe(captureDevice)
                            # camera.stop()
                            csv.close()
                            cv2.destroyAllWindows()
                            #camera.stop()
                            return bar, posBar
                    elif state == "boneyard" or state == "unsure":
                        if len(bar) == 1:
                            # tracker.track(targetName)
                            camera.releaseImage(captureDevice)
                            camera.unsubscribe(captureDevice)
                            csv.close()
                            cv2.destroyAllWindows()
                            #camera.stop()
                            # camera.stop()
                            return bar, posBar

                        
            # Show video stream

        cv2.imshow("Barcode Scanner", th3)
        #cv2.imshow("Barcode Scanner", image)
        #cv2.imshow("new image", new_image)

            # cv2.waitKey(1)
        key = cv2.waitKey(1) & 0xFF
        
     
            # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
     
    # close the output CSV file do a bit of cleanup
    # print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    camera.stop()

def moveHeadCenter():
    global z, headMovement, tracker
    # Move head to center
    #racker.stopTracker() ########################################## uncomment after testing camera by itself
    names      = ["HeadYaw", "HeadPitch"]
    z = 0 # HeadYaw z
    y = 0 # HeadPitch y
    angleLists = [z, y] # move yaw to 0 and pitch to 0
    timeLists  = [1.0, 1.0] # move to yaw 0 in 1sec, -45deg in 1sec, 45deg in 1sec, pitch to 0 in 1sec
    isAbsolute = True
    headMovement.angleInterpolation(names, angleLists, timeLists, isAbsolute)

def moveHeadLeft():
    global z
    # Move head to the left when looking at initial tiles
    print("Moving head left...")
    name      = ["HeadYaw"]
    z = 0.785 # HeadYaw 45deg
    angle = [z] # move yaw 45deg to the left 
    time  = [1.0] # move to yaw in 1sec
    isAbsolute = True
    headMovement.angleInterpolation(name, angle, time, isAbsolute)
    #time.sleep(2) # wait a sec
    # if barcodeData not in found:
        # x += angle

def moveHeadRight():
    global z
    # Move head to the right when looking at initial tiles
    print("Moving head right...")
    name      = ["HeadYaw"]
    z = -0.785 # HeadYaw -45deg
    angle = [z] # move yaw 90deg to the right 
    time  = [2.0] # move to yaw in 2sec
    isAbsolute = True
    headMovement.angleInterpolation(name, angle, time, isAbsolute)
    #time.sleep(2) # wait a sec
    # x += angle

if __name__ == "__main__":
    Scan("deal")


