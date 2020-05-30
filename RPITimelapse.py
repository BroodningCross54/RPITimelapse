#Application: PI Timelaps
#Description: Captures a timelaps
#Author: Sara Wass & Lukas Wass


import os
import sys

#Install picamera: sudo apt-get install python-picamera
import picamera

import datetime #Date time

#Used to create unique file names
import hashlib

import time

#Install psutil: pip3 install psutil
#Used to get CPU and RAM usage
import psutil

#Install keyboard: pip3 install keyboard
import keyboard


#Log file
PROGRAM_PATH = "/media/pi/COMES/timelapse"


#Time to wait before checking if it is time to take a snapshot (time is seconds)
WAIT_TIME = 1


#List of times to capture snapshots at each day. Format hh-mm-ss
SNAPSHOT_TIMES_LIST = [
    "00-00-00",
    "00-30-00",
    "01-00-00",
    "01-30-00",
    "02-00-00",
    "02-30-00",
    "03-00-00",
    "03-30-00",
    "04-00-00",
    "04-30-00",
    "05-00-00",
    "05-30-00",
    "06-00-00",
    "06-30-00",
    "07-00-00",
    "07-30-00",
    "08-00-00",
    "08-30-00",
    "09-00-00",
    "09-30-00",
    "10-00-00",
    "10-30-00",
    "11-00-00",
    "11-30-00",
    "12-00-00",
    "12-30-00",
    "13-00-00",
    "13-30-00",
    "14-00-00",
    "14-30-00",
    "15-00-00",
    "15-30-00",
    "16-00-00",
    "16-30-00",
    "17-00-00",
    "17-30-00",
    "18-00-00",
    "18-30-00",
    "19-00-00",
    "19-30-00",
    "20-00-00",
    "20-30-00",
    "21-00-00",
    "21-30-00",
    "22-00-00",
    "22-30-00",
    "23-00-00",
    "23-30-00"
]


#Returns date time string formated as: yyyy-MM-dd--hh-mm-ss
def GetDateTimeString():
    now = datetime.datetime.now()
    #Date
    yearString = str(now.year)
    monthString = str(now.month).zfill(2)
    dayString = str(now.day).zfill(2)

    #Time
    hourString = str(now.hour).zfill(2)
    minuteString = str(now.minute).zfill(2)
    secondString = str(now.second).zfill(2)

    return (yearString + "-" + monthString + "-" + dayString
            + "--" + hourString + "-" + minuteString + "-" + secondString)


#Returns date string formated as: yyyy-MM-dd
def GetDateString():
    now = datetime.datetime.now()
    yearString = str(now.year)
    monthString = str(now.month).zfill(2)
    dayString = str(now.day).zfill(2)

    return yearString + "-" + monthString + "-" + dayString


#Returns time string formated as: hh-mm-ss
def GetTimeString():
    now = datetime.datetime.now()
    hourString = str(now.hour).zfill(2)
    minuteString = str(now.minute).zfill(2)
    secondString = str(now.second).zfill(2)

    return hourString + "-" + minuteString + "-" + secondString


#Create a unique filename
def CreateUniqueDateTimeFilename(fileExtention):
    #Unique string to ensure unique file names
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    uniqueIdString = str(hash.hexdigest()[:10])
    return str(GetDateTimeString() + "--" + uniqueIdString + fileExtention)


#Create a unique filepath
def CreateImageFilePath():
    dateDirectory = PROGRAM_PATH + "/" + "snapshots" +  "/" + GetDateString()

    #Check if log directory exists else create log directory
    if not os.path.exists(dateDirectory):
        os.makedirs(dateDirectory)
    return str(dateDirectory + "/" + CreateUniqueDateTimeFilename(".jpg"))


#Write content to file at filePath
def WriteLogRow(directoryPath, filename, content):
    #Check if log directory exists else create log directory
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)

    dateTimeStamp = GetDateTimeString()

    filePath = directoryPath + "/" + filename

    #Write log with date time stamp to file
    f = open(filePath, "a")
    f.write("\n" + dateTimeStamp + ":\n" + str(content) + "\n-----")
    f.close()

    print("\nDone logging:\n" + content + "\nTo: " + filePath)


#Get CPU usage
def GetCPUUsage():
    return str(psutil.cpu_percent())


#Get RAM usage
def GetRAMUsage():
    return str(psutil.virtual_memory().percent)


#Main
def Main():
    #Check if program directory exists else create program directory
    if not os.path.exists(PROGRAM_PATH):
        print("Creating program directory: " + PROGRAM_PATH)
        os.makedirs(PROGRAM_PATH)
    
    print("Start timelapse")
    print("Hold q and p to quit program")
    
    #Create camera object
    camera = picamera.PiCamera()
    camera.resolution = (3280, 2464)
    camera.rotation = 180
    #camera.preview_window=(0, 0, 640, 480)
    #camera.start_preview()

    didTakeSnapshot = False


    didSayNoKeyboardConnected = False

    #Timelapse loop
    while(True):
        try:
            if (keyboard.is_pressed("q") and keyboard.is_pressed("p")):
                didSayNoKeyboardConnected = False
                print("Stop timelapse")
                return
        except:
            if not didSayNoKeyboardConnected:
                didSayNoKeyboardConnected = True
                print("No keyboard connected")


        try:
            currentTime = GetTimeString()
            shouldTakeSnapshot = False

            for snapshotTime in SNAPSHOT_TIMES_LIST:
                if (snapshotTime == currentTime):
                    shouldTakeSnapshot = True
                    break
            
            if shouldTakeSnapshot:
                if not didTakeSnapshot:
                    filePath = CreateImageFilePath()

                    #Capture snapshot
                    failedToCaptureSnapshot = False
                    failCounter = 0
                    exeption = ""
                    while(not failedToCaptureSnapshot):
                        try:
                            if (failCounter < 10):
                                camera.capture(filePath)
                                failedToCaptureSnapshot = True
                            else:
                                break
                        except:
                            exeption = sys.exc_info()[0]
                            failedToCaptureSnapshot = False
                            failCounter += 1

                    #Create log snapshot content
                    if (failedToCaptureSnapshot):
                        logContent = ("Snapshot saved to path: " + filePath + "\nCPU: " + GetCPUUsage() + "\nRAM: " + GetRAMUsage())                        
                    else:
                        logContent = ("Could not capture snapshot.\n!!EXEPTION!!: " + exeption + "\nCPU: " + GetCPUUsage() + "\nRAM: " + GetRAMUsage())

                    #Log snapshot
                    WriteLogRow(str(PROGRAM_PATH + "/log"), "Log.txt", logContent)
                        
                    didTakeSnapshot = True
            else:
                didTakeSnapshot = False
        except:
            e = sys.exc_info()[0]
            
            #Log error
            logContent = (str("!!EXEPTION!!: " + str(e)) + "\nCPU: " + GetCPUUsage() + "\nRAM: " + GetRAMUsage())
            WriteLogRow(str(PROGRAM_PATH + "/log"), "Log.txt", logContent)

        #Wait
        time.sleep(WAIT_TIME) 

Main()
