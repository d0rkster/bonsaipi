import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_scd30
import Adafruit_DHT
from picamera import PiCamera
import sys
from datetime import datetime
import os, os.path
import os, psutil
import shutil
#import numpy as np
#import pandas as pd


#GPIO.setmode (GPIO.BOARD)

dht_device = Adafruit_DHT.DHT22

#i2c = busio.I2C(board.SCL, board.SDA)
#scd = adafruit_scd30.SCD30(board.I2C())

dhtpin = 4
lightpin = 25
fanpin = 16
heatingpadpin = 12
waterpumppin = 19
watersensorpin = 26
GPIO.setup(watersensorpin,GPIO.IN)
chan_list = (watersensorpin)
GPIO.input(watersensorpin)

GPIO.setup(lightpin, GPIO.OUT)
GPIO.setup(fanpin, GPIO.OUT)
GPIO.setup(waterpumppin, GPIO.OUT)
GPIO.setup(heatingpadpin, GPIO.OUT)



#time

while True:
    localtime = time.localtime()    
    timenow = time.strftime("%m/%d/%y-%H:%M:%S", localtime)
    timefordata = time.strftime("%m/%d/%y %H:%M:%S", localtime)
    timenowtime = time.strftime("%H:%M:%S", localtime)
    pictime = time.strftime("%m.%d.%y.%H.%M.%S", localtime)
    day = time.strftime("%a", localtime)
    hour = time.strftime("%H", localtime)
    minute = time.strftime ("%M", localtime)
    print ("")
    print ("........................")
    print (timenow)
    print ("...")


    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(board.I2C())
    adafruit_scd30.SCD30.self_calibration_enabled = False
#    adafruit_scd30.SCD30.forced_recalibration_reference = 600
    adafruit_scd30.SCD30.ambient_pressure = 99086.39
    adafruit_scd30.SCD30.altitude = 630
    #adafruit_scd30.measurement_interval (3)	

    s1co2 = float(round(scd.CO2, 2))
    s1co2h = (round(scd.relative_humidity, 3))
    s1tco2c = (round(scd.temperature, 2))
#    s1tco2f = (round(int(scd.temperature*1.8+32),4))
    s1tco2f = (round(scd.temperature, 2)*1.8+32)
    Humidity, Temperature = Adafruit_DHT.read_retry(dht_device, dhtpin)
    s1ch = (round(Humidity, 2))
#    s1ch = (Humidity)
#    s1tcf = (round(int(Temperature*1.8+32),4))
    s1tcf = (round(Temperature, 2)*1.8+32)
    
    with open("/var/www/html/co2only.txt") as file:
        for line in file:
            pass
    previousco2 = float(line)
    
    with open("/var/www/html/temponly.txt") as file:
        for line in file:
            pass
    
    previoustemp = float(line)
    
    with open("/var/www/html/humidonly.txt") as file:
        for line in file:
            pass
    
    previoushumid = float(line)



    changeinco2 = (float(str(s1co2 - previousco2)))
    changeintemp = (float(str(s1tcf - previoustemp)))
    changeinhumid = (float(str(s1ch - previoushumid)))
    
#camera


    if timenowtime > ("06:00:00") and timenowtime < ("06:01:10"):
        camera = PiCamera()
        time.sleep(3)
        camera.resolution = (1280, 720)
        brightness = 80
        camera.contrast = 1
        file_name = "/home/pi/bonsaipi/images/bonsai_" + str(datetime.now().strftime('%b%d%Y_%I%M%p')) + ".jpg"
        camera.capture(file_name)
        camera.close()
        print ("Picture taken")
        print ("...")

    elif timenowtime > ("12:00:00") and timenowtime < ("12:01:10"):
        camera = PiCamera()
        time.sleep(3)
        camera.resolution = (1280, 720)
        brightness = 80
        camera.contrast = 1
        file_name = "/home/pi/bonsaipi/images/bonsai_" + str(datetime.now().strftime('%b%d%Y_%I%M%p')) + ".jpg"
        camera.capture(file_name)
        camera.close()
        print("Picture taken")
        print ("...")
         
    
    elif timenowtime > ("23:58:00") and timenowtime < ("23:59:10"):
        camera = PiCamera()
        time.sleep(3)
        camera.resolution = (1280, 720)
        brightness = 80
        camera.contrast = 1
        file_name = "/home/pi/bonsaipi/images/bonsai_" + str(datetime.now().strftime('%b%d%Y_%I%M%p')) + ".jpg"
        camera.capture(file_name)
        camera.close()
        print("Picture taken")
        print ("...")
         
    
    else:
        path, dirs, files = next(os.walk("/home/pi/bonsaipi/images"))
        piccount = len(files)
        print("No picture taken")
        print ("...")
         


#lights

    if timenowtime > ("06:00:00") and timenowtime < ("17:00:00"):
        GPIO.output(lightpin, 0)
        print("Light On: 6AM - 5PM")
        print(("..."))
        os.remove("/var/www/html/lights.txt")
        f = open("/var/www/html/lights.txt", "a+")
        f.write ("lights")
        f.write (" 1")
        f.write ('\n')
        f = open("/var/www/html/keeplightsdata.txt", "a+")
        f.write (str(timefordata))
        f.write (" lights")
        f.write (" 1")
        f.close ()
                
    else:
        GPIO.output(lightpin,1)
        print("Light off: 5PM - 6AM")
        print(("..."))
        os.remove("/var/www/html/lights.txt")
        f = open("/var/www/html/lights.txt", "a+")
        f.write ("lights")
        f.write (" 0")
        f.write ('\n')
        f = open("/var/www/html/keeplightsdata.txt", "a+")
        f.write (str(timefordata))
        f.write (" lights")
        f.write (" 0")
        f.close ()
                
        
#fans    
    
    if  s1co2 > 1200:
        GPIO.output(fanpin, 0)
        print("Fans on, CO2 is", s1co2, "(> 1,200PPM)")
        print(("..."))
        os.remove("/var/www/html/fans.txt")
        f = open("/var/www/html/fans.txt", "a+")
        f.write ("Fans")
        f.write (" 1")
        f.write ('\n')
        f = open("/var/www/html/keepfandata.txt", "a+")
        f.write (str(timefordata))
        f.write (" fans")
        f.write (" 1")
        f.close ()
    
       
    else:
        GPIO.output(fanpin,1)
        print("Fans off, CO2 is", s1co2, "(< 1,200PPM)")
        print(("..."))
        os.remove("/var/www/html/fans.txt")
        f = open("/var/www/html/fans.txt", "a+")
        f.write ("fans")
        f.write (" 0")
        f.write ('\n')
        f = open("/var/www/html/keepfandata.txt", "a+")
        f.write (str(timefordata))
        f.write (" fans")
        f.write (" 0")
        f.close ()
        
        
#water level & pump

    
    if day == "Mon":

        
        if (GPIO.input(watersensorpin)==0) and (day == ("Mon")) and ((hour == ("04")) and minute < ("15")):
            GPIO.output(waterpumppin, 0)
            print("Water level low, pump on")
            print(("..."))
            os.remove("/var/www/html/waterpump.txt")
            f = open("/var/www/html/waterpump.txt", "a+")
            f.write ("waterpump")
            f.write (" 1")
            f.write ('\n')
            f = open("/var/www/html/keepwaterpumpdata.txt", "a+")
            f.write (str(timefordata))
            f.write (" waterpump")
            f.write (" 1")
            f.close ()                    
    
    
    
        else:
            GPIO.output(waterpumppin, 1)
            print("Water level OK, pump off")
            print(("..."))
            os.remove("/var/www/html/waterpump.txt")
            f = open("/var/www/html/waterpump.txt", "a+")
            f.write ("waterpump")
            f.write (" 0")
            f.write ('\n')
            f = open("/var/www/html/keepwaterpumpdata.txt", "a+")
            f.write (str(timefordata))
            f.write (" waterpump")
            f.write (" 0")
            f.close ()      

    else:
        print("Not Monday, not checking for water level")
        print ("...")
        
  
    
#heating pad

    if s1tcf < 70:
        GPIO.output(heatingpadpin, 0)
        print("Heating is On, temp is", s1tcf, " (< 70)")
        print(("..."))
        os.remove("/var/www/html/heatingpad.txt")
        f = open("/var/www/html/heatingpad.txt", "a+")
        f.write ("heatingpad")
        f.write (" 1")
        f.write ('\n')
        f = open("/var/www/html/keepheatingpaddata.txt", "a+")
        f.write (str(timefordata))
        f.write (" heatingpad")
        f.write (" 1")
        f.close ()        

    else:
        GPIO.output(heatingpadpin, 1)
        print("Heating Off, temp is", s1tcf, "(> 70)")
        print(("..."))
        os.remove("/var/www/html/heatingpad.txt")
        f = open("/var/www/html/heatingpad.txt", "a+")
        f.write ("heatingpad")
        f.write (" 0")
        f.write ('\n')
        f = open("/var/www/html/keepheatingpaddata.txt", "a+")
        f.write (str(timefordata))
        f.write (" heatingpad")
        f.write (" 0")
        f.close ()        

# print the various data
        
    print ("DHT22 Temp (f) Current:  ", s1tcf)
    print ("DHT22 Temp (f) Previous: ", previoustemp)
    print ("DHT22 Temp (f) Change:   ",changeintemp)
    print ("CO2 Temp (f) Current:    ", s1tco2f)
    print ("DHT22 Humidity Current:  ", s1ch)
    print ("DHT22 Humidity previous: ", previoushumid)
    print ("DHT22 Humidity Change:   ", changeinhumid)
    print ("CO2 Humidity Current:    "  , s1co2h)
    print ("CO2 (PPM) Current:       ", s1co2)
    print ("CO2 (PPM) Previous:      ", previousco2)
    print ("Change in CO2:           ", changeinco2)
    print ("...")
    path, dirs, files = next(os.walk("/home/pi/bonsaipi/images"))
    piccount = len(files)
    print("Total pictures taken:", piccount)
    process = psutil.Process(os.getpid())
    print ("...")
    print ('CPU usage is: ', psutil.cpu_percent(4), "%")
    print ('RAM usage is: ', psutil.virtual_memory()[2], "%") 
    total, used, free = (shutil.disk_usage(__file__))
    print ("Ttl disk space (MB):", (round(total / 1024 / 1024)))
    print ("Usd disk space (MB):", (round(used / 1024 / 1024)))
    print ("Fre disk space (MB):", (round(free / 1024 / 1024)))
    print("Ambient Pressure:", scd.ambient_pressure)
    print("Altitude:", scd.altitude, "feet above sea level")
    print("Measurement interval:", scd.measurement_interval)
    print("Temperature offset:", scd.temperature_offset)
    print ("...")
    print ("uptime & sysinfo:")
    os.system ('uptime')
    print ("........................")


# send the various data for keeping or scrapers

    f = open("/var/www/html/time.txt", "a+")
    f.write ("time,")
    f.write (str(timefordata))
    f.write ('\n')
    f.close()
    
    f = open("/var/www/html/dht22humidity.txt", "a+")
    f.write ("time,")
    f.write (str(timefordata))
    f.write (",dht22humidity,")
    f.write (str(s1ch))
    f.write ('\n')
    f.close ()
    
    f = open("/var/www/html/dht22temp.txt", "a+")
    f.write ("time,")
    f.write (str(timefordata))
    f.write (",dht22tempf,")
    f.write (str(s1tcf))
    f.write ('\n')
    f.close ()
     
    f = open("/var/www/html/co2humidity.txt", "a+")
    f.write ("time,")
    f.write (str(pictime))
    f.write (",co2humidity,")
    f.write (str(s1co2h))
    f.write ('\n')
    f.close ()
    
    f = open("/var/www/html/co2temp.txt", "a+")
    f.write ("time,")
    f.write (str(pictime))
    f.write (",co2tempf,")
    f.write (str(s1tco2f))
    f.write ('\n')
    f.close ()
    
    f = open("/var/www/html/co2.txt", "a+")
    f.write ("time,")
    f.write (str(timefordata))
    f.write (",co2,")
    f.write (str(s1co2))
    f.write ('\n')
    f.close ()
    
    f = open("/var/www/html/co2only.txt", "a+")
    f.write (str(s1co2))
    f.write ('\n')
    f.close ()
    
    f = open("/var/www/html/temponly.txt", "a+")
    f.write (str(s1tcf))
    f.write ('\n')
    f.close ()
    
    f = open("/var/www/html/humidonly.txt", "a+")
    f.write (str(s1ch))
    f.write ('\n')
    f.close ()
    
    os.remove("/var/www/html/alldataforinflux.txt")
    f = open("/var/www/html/alldataforinflux.txt", "a+")
    f.write ("dht22humidity ")
    f.write (str(s1ch))
    f.write ('\n')
    f.write ("dht22temp ")
    f.write (str(s1tcf))
    f.write ('\n')
    f.write ("co2humidity ")
    f.write (str(s1co2h))
    f.write ('\n')
    f.write ("co2tempf ")
    f.write (str(s1tco2f))
    f.write ('\n')
    f.write ("co2 ")
    f.write (str(s1co2))
    f.write ('\n')
    f.close()    

    
    f = open("/var/www/html/keepalldata.txt", "a+")
    f.write ("time ")
    f.write (str(timefordata))
    f.write ('\n')
    f.write ("dht22humidity ")
    f.write (str(s1ch))
    f.write ('\n')
    f.write ("dht22temp ")
    f.write (str(s1tcf))
    f.write ('\n')
    f.write ("co2humidity ")
    f.write (str(s1co2h))
    f.write ('\n')
    f.write ("co2tempf ")
    f.write (str(s1tco2f))
    f.write ('\n')
    f.write ("co2 ")
    f.write (str(s1co2))
    f.write ('\n')
    f.close()    

    
    for remaining in range(59, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write(" {:2d} seconds to refresh".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    
    time.sleep (1)
    
