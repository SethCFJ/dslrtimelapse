


from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

#Kill gphoto2 process that blocks imagecapture

def killgphoto2Process ():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate ()

    #Search for the line that has the process to kill
    for line in out.splitlines ():
        if b'gvfsd-gphoto2' in line:
            # Kill the process
            pid = int(line.split(None,1) [0])
            os.kill(pid, signal.SIGKILL)


shot_date = datetime.now().strftime("%Y%m%d")


#Title of the project
picID = "TimelapseTest"


#In the second param of the clear command put directory of your camera found with 
#gphoto2 --list-files

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "-R", "--delete-all-files"]
triggerAndDownloadCommand = ["--capture-image-and-download"]


folder_name = picID + shot_date
save_location = "/home/pitest/Desktop/TimelapseApp/Images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)

    except:
        print (">>>Local directory exists, capturing image.")
        os.chdir(save_location)

    else:
        print (">New Local Directory created successfully")

def captureImages():
    print("Triggering capture...")
    gp(triggerAndDownloadCommand)
    sleep(10) #Do not change#
    print("Clearing camera SD card...")
    gp(clearCommand)

    

def renameFiles(ID):
    
    shot_time = datetime.now().strftime("%Y%m%d-%H:%M:%S")
    print("Current working directory:", os.getcwd())
    print("Files found for renaming:", os.listdir("."))
    for filename in os.listdir("."):
        if len (filename) < 14:
            if filename.endswith(".jpg"):
                os.rename(filename, (ID + shot_time + ".JPG"))
                print (">>>>Copied JPG image to Pi and renamed successfully.")
            elif filename.endswith(".cr2"):
                os.rename(filename, (ID + shot_time + ".CR2"))
                print (">>>>Copied CR2 image to Pi and renamed successfully.")

killgphoto2Process()
print ("**********  To end Timelapse press ctrl-c **********")
gp(clearCommand)

while True:
    print (">>Camera SD Card Cleared, Checking for Local Directory.")
    createSaveFolder()
    captureImages()
    renameFiles(picID)
    sleep(10) #Interval Delay 


#The interval delay represents time between captures