# Timelapse Project

## Purpose

This project features a Python script that automates time-lapse photography using the gphoto2 library. The script captures images at predefined intervals and organises them into folders on a rasberry pi (or any linux system). Scheduling is managed by a cronjob (example included below) allowing the script to run at specific times automatically. Future enchancments of this project will include an additional script that uploads captured images to an ftp server.

## Build Steps

### To install gphoto2 packages on your Raspberry Pi follow this short tutorial:

`https://pimylifeup.com/raspberry-pi-dslr-camera-control/`

### Timelapse.py build step

Within the `timelapse.py` file there are some parameters that need to be set according to your setup:

Ensure the clear command is using the directory of your camera. Run the `gphoto2 --list-files` command. It should return something like:

```
pitest@raspberrypi:~ $ gphoto2 --list-files
There is no file in folder '/'.
There is no file in folder '/store_00020001'.
There is no file in folder '/store_00020001/DCIM'.
There is no file in folder '/store_00020001/DCIM/100CANON'.
There is no file in folder '/store_00020001/MISC'.
```

In this case the correct directory is: `/store_00020001/DCIM/100CANON`. (Usually the longest)

Change the save_location value to where you would like the images to be saved. Example:
`save_location = "/home/pitest/Desktop/TimelapseApp/Images/" + folder_name`

### launcher.sh build step

This launcher.sh file is called upon by the cron to execute the script in the right directories. You will need to change it to match the directory you have saved the timelapse.py file. Example:

```
cd home/pitest/Desktop/TimelapseApp
sudo python3 timelapse.py
```

### Cronjob build step

First create a new directory anywhere on the Pi called `logs`. Within this directory we will store a file that logs the errors that may occur when the cronjob tries to run.

Open a terminal window and enter the line `sudo crontab -e`

Scroll down to the very bottom of the file and input:

`00 14 * * * sh /path/to/your/launcher.sh >/path/to/your/logdir/cronlog 2>&1`

This cronjob is set to execute at 2:00pm everyday. Refer to the image below to understand how cronjobs can be timed:

![begnners-guide-to-cron-jobs](https://github.com/user-attachments/assets/8ff4843c-ab76-4401-a88e-631d11d5f951)


The cronjob will initialise automatically so there is no need to run a command.

### Features

- Allows Raspberry Pi to act as a camera controller
- Can set the timelapse to run any time/day of the month/year
- Can set intervals between shots

### Future Goals:

- To create a script that pushes the local Raspberry Pi image files to an FTP server then delete them
- To make the script more modular and more feedback from cronjobs

### Problems encountered

- Between different model cameras some gphoto2 commands didn't work as expected. E.g. on the first camera used the trigger command `--trigger-capture` worked. Whereas on second camera I had to use `--capture-image-and-download`
- Initially the cronjob's weren't running however it turned out to be an error with the Pi itself and not my code. Took time to troubleshoot.
- Had issues with the script throttling, which is why I recommend using the `--capture-image` command as it waits for the capture to be complete before moving on.
