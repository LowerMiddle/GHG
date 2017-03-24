#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import Tkinter as tk
import tkFont
import tkMessageBox
import CalendarDialog
import sys
import os
import time
import subprocess
import urllib

#Loading drivers
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#Font and GUI
root = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')

#Def globals
time1 = ''
temp_c = ''
temp_f = ''
today = ''
Rev = '0.1'
#ClockLabel
ClockLabel = Label(root, font = myFont, bg = "#149dc9")
ClockLabel.place(relx=.5, rely=.4, anchor="c")

#DateLabel
DateLabel = Label(root, font = myFont, bg = "#149dc9")
DateLabel.place(relx=.5, rely=.5, anchor="c")

#TempLabel
TemperatureLabel = Label(root, font = myFont, bg = "#149dc9")
TemperatureLabel.place(relx=.5, rely=.2, anchor="c")

#STLabel
STL = Label(root, font = myFont, bg = "#149dc9")
STL.place(relx=.5, rely=.6, anchor="c")
try:
    STL.config(text="Desired temperature (C/F): %s" % ST)
    if ST == '':
        STL.config(text="Please set the desired temperature")
except:
    STL.config(text="Please set the desired temperature")

#VersionLabel
VersionLabel = Label(root, font = myFont, bg = "#149dc9", fg = "#F0F0F0")
VersionLabel.config(text="Current version: " + Rev)
VersionLabel.place(relx=.8, rely=.9, anchor="c")

#Temp sensor
try:
    temp_sensor = 'sys/bus/w1/devices/28-000005e2fdc3/w1_slave'
    TemperatureLabel.config(text="Temperature (C/F): " + read_temp)
except:
    TemperatureLabel.config(text="Temperature (C/F): There is some type of error") 

#HumidityLabel
HumidityLabel = Label(root, font = myFont, bg = "#149dc9")
HumidityLabel.config(text="Humidity: " + "read_humidity") #tva da se mahne posle
HumidityLabel.place(relx=.5, rely=.3, anchor="c")

####GET VERSION###
def update():
    REVISION = 01;
    revision = get_revision()
    if revision == -1:
        tkMessageBox.showwarning("No internet connection!", "Please check your internet connection!")
    elif revision > REVISION:
        try:
            sock = urllib.urlopen('https://github.com/LowerMiddle/GHG/main.py')
            page = sock.read()
        except IOError:
            page = ''
        if page == '':
            tkMessageBox.showwarning("Error!", "Unable to download latest version")

        f = open('new_main.py', 'w')
        f.write(page)
        f.close()

        this_file = __file__
        if this_file.startswith('./'):
            this_file=this_file[2:]

        f = open('update_ghg.sh', 'w')
        f.write('''#!/bin/sh\n
                    rm -rf ''' + this_file + '''\n
                    rm -rf update_ghg.sh\n
                    chmod +x ''' + this_file + '''\n
                    ''')
        f.close()

        returncode = call(['chmod', '+x', 'update_ghg.sh'])
        if returncode != 0:
            tkMessageBox.showwarning("Error!", "Error!")

        returncode = call(['sh', 'update_ghg.sh'])
        if returncode != 0:
            tkMessageBox.showwarning("Error!", "Error!")
    else:
        tkMessageBox.showwarning("Success!", "Your update is successful!")
        python = sys.executable
        os.execl(python, python, * sys.argv)
            
def get_revision():
    irev = -1
    try:
        sock = urllib.urlopen('https://github.com/LowerMiddle/GHG/main.py')
        page = sock.read()
    except IOError:
        return (-1, '', '')
    # get the revision
    start = page.find('REVISION = ')
    stop = page.find(";", start)
    if start != -1 and stop != -1:
        start += 11
        rev = page[start:stop]
        try:
            irev = int(rev)
        except ValueError:
            rev = rev.split('\n')[0]
            print R + '[+] invalid revision number: "' + rev + '"'

    return irev

#####TEMPERATURE SENSOR#####a
    
def temp_raw():
    try:
        f = open(temp_sensor, 'r')
        lines = f.readlines()
        f.close()
        return lines
    except:
        TemperatureLabel.config(text="Temperature (C/F): There is some type of error")
            
def read_temp():
    try:
        global temp_c
        global temp_f
        lines = temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = temp_raw()
        temp_output = lines[1].find('t=')
        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
            TemperatureLabel.config(text="The temperature is (C/F): " + read_temp)
        TemperatureLabel.after(5000, read_temp)
    except:
        TemperatureLabel.config(text="Temperature (C/F): There is some type of error") 

ST = ''
def create_rootdow():
    TempEntry = Toplevel()
    TempEntry.title("Main!")
    TempEntry.geometry('400x240')
    TempEntry.configure(background='#149dc9')
    global ST
    STLabel = Label(TempEntry, font = myFont, bg = "#149dc9")
    STLabel.config(text = "Please enter the desired temperature (t)")
    STLabel.pack()
    var = IntVar()
    Radiobutton(TempEntry, text = "C°", variable = var, value = 1).pack()
    Radiobutton(TempEntry, text = "°F", variable = var, value = 2).pack()
    def rbSel():
        selection = 0
        selection = var.get()
        spinbox = Spinbox(TempEntry, values=(22, 22.50, 23, 23.50, 24, 24.50, 25, 25.50, 26, 26.50, 27, 27.50, 28, 28.50, 29, 29.50, 30, 30.50, 31, 31.50, 32, 32.50, 33, 33.50, 34, 34.50))
        spinbox.pack()
        spinbox2 = Spinbox(TempEntry, from_=72, to=94)
        spinbox2.pack()
        if  selection == 1:
            def retrieve_input():
                    try:
                        ST = float(spinbox.get())
                        if ST <= 22 or ST > 35:
                            tkMessageBox.showwarning("Invalid temperature!", "Please enter a temperature between 22° and 30°")
                        #degr
                        #trii/mb
                        else:
                            STL.config(text="Desired temperature (C°/°F): %s" % ST)
                    except ValueError:
                    #STtextbox.delete('''"1.0", END''')
                        STLabel.config(text = "greshka")
                    #trii/mb
                    SetButton = Button(TempEntry, text='Set', command=retrieve_input).pack()
                    QuitButton = Button(TempEntry, text='Quit', command=TempEntry.destroy).pack()
        elif  selection == 1:
            def retrieve_input():
                try:
                    ST = float(spinbox.get())
                    if ST <= 72 or ST >= 94:
                        tkMessageBox.showwarning("Invalid temperature!", "Please enter a temperature between 22° and 30°")
                        #degr
                        #trii/mb
                    else:
                        STL.config(text="Desired temperature (C°/°F): %s" % ST)
                except ValueError:
                    #STtextbox.delete('''"1.0", END''')
                    STLabel.config(text = "greshka")
                    #trii/mb
    Button(TempEntry, text = "OK", command = rbSel).pack()



    
###############

#####HUMIDITY SENSOR#####



###############

###DATE/TIME###
        
def tick():
    try:
        global time1
        time2 = time.strftime('%H:%M:%S')
        if time2 != time1:
            time1 = time2
            ClockLabel.config(text="Time: " + time2)
        ClockLabel.after(200, tick)
    except:
        ClockLabel.config(text="Time: There is some type of error")

def datetick():
    try:
        global today
        today2 = time.strftime("%A %d. %B %Y")
        if today2 != today:
            today = today2
            DateLabel.config(text="Date: %s" % today2)
        DateLabel.after(200, tick)
    except:
        DateLabel.config(text="Date: There is some type of error")
        
    
##############




###RESTART###
    
def restart():
    result = tkMessageBox.askyesno("GHG","Would you like to restart the system?")
    if result == True:
        command = "/usr/bin/sudo /sbin/shutdown -r now" #LATER - sudoers
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        #os.system('shutdown now')
##############
        

###SHUTDOWN###

def shutdown():
    result = tkMessageBox.askyesno("GHG","Would you like to shutdown the system?")
    if result == True:
        command = "/usr/bin/sudo /sbin/shutdown now" #LATER - sudoers
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        #os.system('shutdown now')
    
##############

        
###EXIT###just in case
    
def exitProgram(): 
    root.destroy()

#####
root.title("Main!")
root.geometry('800x480')
root.configure(background='#149dc9')
root.attributes('-fullscreen', True)

ProgramsButton = Button(root, text = "Programs", font = myFont, command = '???', height = 1, width = 20, relief=RAISED)
ProgramsButton.place(relx=.2, rely=.2, anchor="c")

TemperatureButton = Button(root, text = "t°", font = myFont, command = create_rootdow, height = 1, width = 20, relief=RAISED)
TemperatureButton.place(relx=.2, rely=.3, anchor="c")

HumidityButton = Button(root, text = "Humidity", font = myFont, command = '???', height = 1, width = 20, relief=RAISED)
HumidityButton.place(relx=.2, rely=.4, anchor="c")

LightsButton = Button(root, text = "Lights", font = myFont, command = '???', height = 1, width = 20, relief=RAISED)
LightsButton.place(relx=.2, rely=.5, anchor="c")

FansButton = Button(root, text = "Fans", font = myFont, command = '???', height = 1, width = 20, relief=RAISED)
FansButton.place(relx=.2, rely=.6, anchor="c")

UpdateButton = Button(root, text = "Check for updates", font = myFont, command = update, height = 1, width = 20, relief=RAISED)
UpdateButton.place(relx=.8, rely=.2, anchor="c")

SetTDButton = Button(root, text = "Set time/date", font = myFont, command = CalendarDialog.main, height = 1, width = 20, relief=RAISED)
SetTDButton.place(relx=.8, rely=.33, anchor="c")

ShutdownButton = Button(root, text = "Shutdown", font = myFont, command = shutdown, height = 1, width = 20, relief=RAISED)
ShutdownButton.place(relx=.8, rely=.46, anchor="c")

RestartButton = Button(root, text = "Restart", font = myFont, command = restart, height = 1, width = 20, relief=RAISED)
RestartButton.place(relx=.8, rely=.6, anchor="c")

read_temp()
datetick()
tick()
mainloop()
