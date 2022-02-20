import RPi.GPIO as GPIO
import subprocess
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Powering Status Pin to indicate that control program is up
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)

# setting up communication pins for binary fanmode transmission
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# define default variables -> fan speed will be at max. if someting goes wrong with getting cpu temps
thermal = -99
fanmode = 100
i = 0

# function to get cpu temperature on linux and macOS and decide on fan speed.
def temp(thermal, fanmode):
    thermal = str(round(float(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True).rstrip())/1000,2))
    if thermal <= 20:
        fanmode = 0
    elif 20 < thermal <= 40:
        fanmode = 25
    elif 40 < thermal <= 60:
        fanmode = 50
    elif 60 < fanmode <= 70:
        fanmode = 75
    elif 70 < fanmode:
        fanmode = 100
    return thermal, fanmode

# main loop
while True:
    # get cpu temp
    temp(thermal, fanmode)
    if fanmode == 0 or fanmode == 25:
        GPIO.output(17, False)
        GPIO.output(18, True)
    elif fanmode == 50:
        GPIO.output(17, True)
        GPIO.output(18, False)
    elif fanmode == 75:
        GPIO.output(17, True)
        GPIO.output(18, True)
    else:
        GPIO.output(17, False)
        GPIO.output(18, False)
    # cpu temp will be updated every 5 seconds
    time.sleep(5)
    i += 1
    # log cpu temp and fan speed
    print("----- Run Nr.:", i, "\nCpu temperature measured: ", thermal + "°C", "- Fanspeed: ", fanmode + "%")