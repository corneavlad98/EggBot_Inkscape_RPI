from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from tkinter import messagebox
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import pigpio
import math

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

#Define some colors
backgroundColor = '#92b8c5' # cyan-ish color
templateButtonTextColor = '#bf3adc' # purple color
quitTextColor = '#bb0000' # red color


#Initialize the UI
gui = Tk(className = "Eggbot Main Menu")
gui.geometry("800x600")
gui.resizable(False,False)
gui['background']=backgroundColor

# Fonts
templateButtonFont = ("Helvetica", 24 )
buttonFont = ("Helvetica", 18 )
entryFieldFont = ("Helvetica", 18 )
labelFont = ("Helvetica", 15 )
titleLabelFont = ("Helvetica", 15, BOLD)
detailsTextFont =("Helvetica", 14)
optionMenuFont = ("Helvetica", 14)

servoSettingsEntries = ['4', '90', '120']
stepper1SettingsEntries = [14, 15, 18, 21, 20, '1/4', 100, True]
stepper2SettingsEntries = [17, 27, 22, 26, 19, '1/4', 100, True]



class Servo_Settins_Tab():
    def __init__(self, tab):
        # Define some paddings
        self.padding_x = 45
        self.padding_y = 25

        # Title label
        self.titleLabel = Label(tab, text="EggBot: Basic Setup - Servo Motor ", font=titleLabelFont)
        self.titleLabel.place(x=20,y=15)

        self.add_labels(tab)
        self.add_entries(tab)
       
        # Add save & test button to tab
        testButton = Button(tab, text="Test", font = buttonFont, width = 5, fg = 'black', command=self.move)
        testButton.place(x=150,y=470)
    
        saveButton = Button(tab, text="Save", font = buttonFont, width = 5, fg = 'black', command=self.update)
        saveButton.place(x=415,y=470)
    
    def add_labels(self, tab):
        # Labels
        self.servoPinLabel = Label(tab, text="Servo pin number (GPIO numbering): ", font=labelFont)
        self.servoPinLabel.place(x=50 + self.padding_x,y=65 + self.padding_y)

        self.servoUpLabel = Label(tab, text="Pen up position, servo at (0-180): ", font=labelFont)
        self.servoUpLabel.place(x=50 + self.padding_x,y=120 + self.padding_y)

        self.servoDownLabel = Label(tab, text="Pen down position, servo at (0-180): ", font=labelFont)
        self.servoDownLabel.place(x=50 + self.padding_x,y=175 + self.padding_y)

        self.details = "-Raise and lower pen to check pen-up and pen-down positions"
        self.detailsLabel = Label(tab, text=self.details, font=detailsTextFont)
        self.detailsLabel.place(x=25 + self.padding_x, y=275 + self.padding_y)
    
    def add_entries(self, tab):
        # Entries
        self.servoPinEntry = Entry(tab, font=entryFieldFont)
        self.servoPinEntry.insert(0, servoSettingsEntries[0])
        self.servoPinEntry.place(x=400 + self.padding_x,y=67 + self.padding_y, width=46, height=30)

        self.servoUpEntry = Entry(tab, font=entryFieldFont)
        self.servoUpEntry.insert(0, servoSettingsEntries[1])
        self.servoUpEntry.place(x=400 + self.padding_x,y=122 + self.padding_y, width=46, height=30)

        self.servoDownEntry = Entry(tab, font=entryFieldFont)
        self.servoDownEntry.insert(0, servoSettingsEntries[2])
        self.servoDownEntry.place(x=400 + self.padding_x,y=177 + self.padding_y, width=46, height=30)
    
    def print_servo_entries(self):
        print(f'Servo pin: {servoSettingsEntries[0]} Up position: {servoSettingsEntries[1]} Down position: {servoSettingsEntries[2]}')

    def update(self):
        # Get values from entries
        entry_value1 = self.servoPinEntry.get()
        entry_value2 = self.servoUpEntry.get()
        entry_value3 = self.servoDownEntry.get()

        # Save values globally
        servoSettingsEntries[0] = str(entry_value1)
        servoSettingsEntries[1] = str(entry_value2)
        servoSettingsEntries[2] = str(entry_value3)

        # Print
        self.print_servo_entries()
  
    def movePenToAngle(self, angle, servo, pwm):           
        print( str(angle) + " deg" )
        addedPulse = math.ceil((angle * 1000) / 90)
        pwm.set_servo_pulsewidth(servo, 500 + addedPulse)
       
    def move(self):
        print("got into servo move!")
        servo = int(servoSettingsEntries[0])
        servoUpAngle = int(servoSettingsEntries[1])
        servoDownAngle = int(servoSettingsEntries[2])

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( servo, GPIO.OUT )

        pwm = pigpio.pi() 
        pwm.set_mode(servo, pigpio.OUTPUT)

        pwm.set_PWM_frequency( servo, 50 )

        self.movePenToAngle(servoUpAngle, servo, pwm)
        time.sleep(2)

        self.movePenToAngle(servoDownAngle, servo, pwm)
        time.sleep(2)
       
        # turning off servo
        pwm.set_PWM_dutycycle(servo, 0)
        pwm.set_PWM_frequency( servo, 0 )

        print("finished servo move!")
class Stepper1_Settings_Tab():
    def __init__(self, tab):
        # Define some paddings
        self.padding_x = 45
        self.padding_y = 25

        # Title label
        self.titleLabel = Label(tab, text="EggBot: Basic Setup - Stepper 1 (egg) ", font=titleLabelFont)
        self.titleLabel.place(x=20,y=15)

        self.add_labels(tab)
        self.add_entries(tab)
       
        # Add save & test button to tab
        testButton = Button(tab, text="Test", font = buttonFont, width = 5, fg = 'black', command=self.move)
        testButton.place(x=150,y=470)
    
        saveButton = Button(tab, text="Save", font = buttonFont, width = 5, fg = 'black', command=self.update)
        saveButton.place(x=415,y=470)
    
    def add_labels(self, tab):
        # Labels
        self.ms1PinLabel = Label(tab, text="MS1 pin (GPIO numbering): ", font=labelFont)
        self.ms1PinLabel.place(x=50 + self.padding_x,y=45 + self.padding_y)

        self.ms2PinLabel = Label(tab, text="MS2 pin (GPIO numbering): ", font=labelFont)
        self.ms2PinLabel.place(x=50 + self.padding_x,y=85 + self.padding_y)

        self.ms3PinLabel = Label(tab, text="MS3 pin (GPIO numbering): ", font=labelFont)
        self.ms3PinLabel.place(x=50 + self.padding_x,y=125 + self.padding_y)

        self.directionPinLabel = Label(tab, text="Direction pin (GPIO numbering): ", font=labelFont)
        self.directionPinLabel.place(x=50 + self.padding_x,y=165 + self.padding_y)

        self.stepPinLabel = Label(tab, text="Step pin (GPIO numbering): ", font=labelFont)
        self.stepPinLabel.place(x=50 + self.padding_x,y=205 + self.padding_y)

        self.stepTypeLabel = Label(tab, text="Step type: ", font=labelFont)
        self.stepTypeLabel.place(x=50 + self.padding_x,y=245 + self.padding_y)

        self.walkDistanceLabel = Label(tab, text="Walk distance (steps): ", font=labelFont)
        self.walkDistanceLabel.place(x=50 + self.padding_x,y=285 + self.padding_y)

        self.clockwiseLabel = Label(tab, text="Clockwise: ", font=labelFont)
        self.clockwiseLabel.place(x=50 + self.padding_x,y=325 + self.padding_y)

        self.details = "-Test stepper 1 (egg) movement"
        self.detailsLabel = Label(tab, text=self.details, font=detailsTextFont)
        self.detailsLabel.place(x=25 + self.padding_x, y=385 + self.padding_y)
    
    def add_entries(self, tab):
        # Entries
        self.ms1PinEntry = Entry(tab, font=entryFieldFont)
        self.ms1PinEntry.insert(0, stepper1SettingsEntries[0])
        self.ms1PinEntry.place(x=400 + self.padding_x,y=47 + self.padding_y, width=46, height=30)

        self.ms2PinEntry = Entry(tab, font=entryFieldFont)
        self.ms2PinEntry.insert(0, stepper1SettingsEntries[1])
        self.ms2PinEntry.place(x=400 + self.padding_x,y=85 + self.padding_y, width=46, height=30)

        self.ms3PinEntry = Entry(tab, font=entryFieldFont)
        self.ms3PinEntry.insert(0, stepper1SettingsEntries[2])
        self.ms3PinEntry.place(x=400 + self.padding_x,y=126 + self.padding_y, width=46, height=30)

        self.directionPinEntry = Entry(tab, font=entryFieldFont)
        self.directionPinEntry.insert(0, stepper1SettingsEntries[3])
        self.directionPinEntry.place(x=400 + self.padding_x,y=166 + self.padding_y, width=46, height=30)

        self.stepPinEntry = Entry(tab, font=entryFieldFont)
        self.stepPinEntry.insert(0, stepper1SettingsEntries[4])
        self.stepPinEntry.place(x=400 + self.padding_x,y=206 + self.padding_y, width=46, height=30)

        self.stepTypesList = ["Full", "Half", "1/4", "1/8", "1/16"]
        self.stringVar1 = StringVar(tab)
        self.stringVar1.set(stepper1SettingsEntries[5]) # default value
        self.stepTypeOptionMenu = OptionMenu(tab, self.stringVar1, *self.stepTypesList, command=self.option1Update)
        self.stepTypeOptionMenu.config(font=optionMenuFont)
        self.stepTypeOptionMenu.place(x=378 + self.padding_x,y=242 + self.padding_y, width=86, height=35)

        self.walkDistanceEntry = Entry(tab, font=entryFieldFont)
        self.walkDistanceEntry.insert(0, stepper1SettingsEntries[6])
        self.walkDistanceEntry.place(x=392 + self.padding_x,y=283 + self.padding_y, width=66, height=30)

        self.clockwiseList = [True, False]
        self.stringVar2 = IntVar(tab)
        self.stringVar2.set(stepper1SettingsEntries[7]) # default value
        self.clockwiseOptionMenu = OptionMenu(tab, self.stringVar2, *self.clockwiseList, command=self.option2Update)
        self.clockwiseOptionMenu.config(font=optionMenuFont)
        self.clockwiseOptionMenu.place(x=378 + self.padding_x,y=320 + self.padding_y, width=86, height=35)
    
    def print_stepper_entries(self):
        stringToPrint = f'MS1 pin: {stepper1SettingsEntries[0]} MS2 pin: {stepper1SettingsEntries[1]} MS3 pin: {stepper1SettingsEntries[2]} '
        stringToPrint += f'Direction pin: {stepper1SettingsEntries[3]} Step pin: {stepper1SettingsEntries[4]} Step type: {stepper1SettingsEntries[5]} '
        stringToPrint += f'Walk distance: {stepper1SettingsEntries[6]} Clockwise: {stepper1SettingsEntries[7]}'

        varTypes = f'1: {type(stepper1SettingsEntries[0])} 2: {type(stepper1SettingsEntries[1])} 3: {type(stepper1SettingsEntries[2])}'
        varTypes += f'4: {type(stepper1SettingsEntries[3])} 5:{type(stepper1SettingsEntries[4])} 6: {type(stepper1SettingsEntries[5])}'
        varTypes += f'7: {type(stepper1SettingsEntries[6])} 8: {type(stepper1SettingsEntries[7])}'
        print(stringToPrint)
        print(varTypes)

    def option1Update(self, selection):
        stepper1SettingsEntries[5] = selection     
    def option2Update(self, selection):
        stepper1SettingsEntries[7] = bool(selection)

    def update(self):
        # Get values from entries
        entry_value1 = self.ms1PinEntry.get()
        entry_value2 = self.ms2PinEntry.get()
        entry_value3 = self.ms3PinEntry.get()
        entry_value4 = self.directionPinEntry.get()
        entry_value5 = self.stepPinEntry.get() 
        entry_value6 = self.walkDistanceEntry.get()          

        # Save values globally
        stepper1SettingsEntries[0] = int(entry_value1)
        stepper1SettingsEntries[1] = int(entry_value2)
        stepper1SettingsEntries[2] = int(entry_value3)
        stepper1SettingsEntries[3] = int(entry_value4)
        stepper1SettingsEntries[4] = int(entry_value5)
        stepper1SettingsEntries[6] = int(entry_value6)

        # Print
        self.print_stepper_entries()
    def move(self):
        print("got into stepper 1 move!")
        # Initialize the stepper
        ms1Pin = stepper1SettingsEntries[0]
        ms2Pin = stepper1SettingsEntries[1]
        ms3Pin = stepper1SettingsEntries[2]
        directionPin = stepper1SettingsEntries[3]
        stepPin = stepper1SettingsEntries[4]
        stepType = stepper1SettingsEntries[5]
        walkDistance = stepper1SettingsEntries[6]
        clockwise = stepper1SettingsEntries[7]

        GPIO_pins = (ms1Pin, ms2Pin, ms3Pin)      
        mymotortest = RpiMotorLib.A4988Nema(directionPin, stepPin, GPIO_pins, "A4988")

        # Execute command      
        mymotortest.motor_go(not clockwise, stepType, walkDistance, 0.01, False, .05)

        print("finished stepper 1 move!")
class Stepper2_Settings_Tab():
    def __init__(self, tab):
        # Define some paddings
        self.padding_x = 45
        self.padding_y = 25

        # Title label
        self.titleLabel = Label(tab, text="EggBot: Basic Setup - Stepper 2 (pen) ", font=titleLabelFont)
        self.titleLabel.place(x=20,y=15)

        self.add_labels(tab)
        self.add_entries(tab)
       
        # Add save & test button to tab
        testButton = Button(tab, text="Test", font = buttonFont, width = 5, fg = 'black', command=self.move)
        testButton.place(x=150,y=470)
    
        saveButton = Button(tab, text="Save", font = buttonFont, width = 5, fg = 'black', command=self.update)
        saveButton.place(x=415,y=470)
    
    def add_labels(self, tab):
        # Labels
        self.ms1PinLabel = Label(tab, text="MS1 pin (GPIO numbering): ", font=labelFont)
        self.ms1PinLabel.place(x=50 + self.padding_x,y=45 + self.padding_y)

        self.ms2PinLabel = Label(tab, text="MS2 pin (GPIO numbering): ", font=labelFont)
        self.ms2PinLabel.place(x=50 + self.padding_x,y=85 + self.padding_y)

        self.ms3PinLabel = Label(tab, text="MS3 pin (GPIO numbering): ", font=labelFont)
        self.ms3PinLabel.place(x=50 + self.padding_x,y=125 + self.padding_y)

        self.directionPinLabel = Label(tab, text="Direction pin (GPIO numbering): ", font=labelFont)
        self.directionPinLabel.place(x=50 + self.padding_x,y=165 + self.padding_y)

        self.stepPinLabel = Label(tab, text="Step pin (GPIO numbering): ", font=labelFont)
        self.stepPinLabel.place(x=50 + self.padding_x,y=205 + self.padding_y)

        self.stepTypeLabel = Label(tab, text="Step type: ", font=labelFont)
        self.stepTypeLabel.place(x=50 + self.padding_x,y=245 + self.padding_y)

        self.walkDistanceLabel = Label(tab, text="Walk distance (steps): ", font=labelFont)
        self.walkDistanceLabel.place(x=50 + self.padding_x,y=285 + self.padding_y)

        self.clockwiseLabel = Label(tab, text="Clockwise: ", font=labelFont)
        self.clockwiseLabel.place(x=50 + self.padding_x,y=325 + self.padding_y)

        self.details = "-Test stepper 2 (pen) movement"
        self.detailsLabel = Label(tab, text=self.details, font=detailsTextFont)
        self.detailsLabel.place(x=25 + self.padding_x, y=385 + self.padding_y)
    
    def add_entries(self, tab):
        # Entries
        self.ms1PinEntry = Entry(tab, font=entryFieldFont)
        self.ms1PinEntry.insert(0, stepper2SettingsEntries[0])
        self.ms1PinEntry.place(x=400 + self.padding_x,y=47 + self.padding_y, width=46, height=30)

        self.ms2PinEntry = Entry(tab, font=entryFieldFont)
        self.ms2PinEntry.insert(0, stepper2SettingsEntries[1])
        self.ms2PinEntry.place(x=400 + self.padding_x,y=85 + self.padding_y, width=46, height=30)

        self.ms3PinEntry = Entry(tab, font=entryFieldFont)
        self.ms3PinEntry.insert(0, stepper2SettingsEntries[2])
        self.ms3PinEntry.place(x=400 + self.padding_x,y=126 + self.padding_y, width=46, height=30)

        self.directionPinEntry = Entry(tab, font=entryFieldFont)
        self.directionPinEntry.insert(0, stepper2SettingsEntries[3])
        self.directionPinEntry.place(x=400 + self.padding_x,y=166 + self.padding_y, width=46, height=30)

        self.stepPinEntry = Entry(tab, font=entryFieldFont)
        self.stepPinEntry.insert(0, stepper2SettingsEntries[4])
        self.stepPinEntry.place(x=400 + self.padding_x,y=206 + self.padding_y, width=46, height=30)

        self.stepTypesList = ["Full", "Half", "1/4", "1/8", "1/16"]
        self.stringVar1 = StringVar(tab)
        self.stringVar1.set(stepper2SettingsEntries[5]) # default value
        self.stepTypeOptionMenu = OptionMenu(tab, self.stringVar1, *self.stepTypesList, command=self.option1Update)
        self.stepTypeOptionMenu.config(font=optionMenuFont)
        self.stepTypeOptionMenu.place(x=378 + self.padding_x,y=242 + self.padding_y, width=86, height=35)

        self.walkDistanceEntry = Entry(tab, font=entryFieldFont)
        self.walkDistanceEntry.insert(0, stepper2SettingsEntries[6])
        self.walkDistanceEntry.place(x=392 + self.padding_x,y=283 + self.padding_y, width=66, height=30)

        self.clockwiseList = [True, False]
        self.stringVar2 = IntVar(tab)
        self.stringVar2.set(
            stepper2SettingsEntries[7]) # default value
        self.clockwiseOptionMenu = OptionMenu(tab, self.stringVar2, *self.clockwiseList, command=self.option2Update)
        self.clockwiseOptionMenu.config(font=optionMenuFont)
        self.clockwiseOptionMenu.place(x=378 + self.padding_x,y=320 + self.padding_y, width=86, height=35)
    
    def print_stepper_entries(self):
        stringToPrint = f'MS1 pin: {stepper2SettingsEntries[0]} MS2 pin: {stepper2SettingsEntries[1]} MS3 pin: {stepper2SettingsEntries[2]} '
        stringToPrint += f'Direction pin: {stepper2SettingsEntries[3]} Step pin: {stepper2SettingsEntries[4]} Step type: {stepper2SettingsEntries[5]} '
        stringToPrint += f'Walk distance: {stepper2SettingsEntries[6]} Clockwise: {stepper2SettingsEntries[7]}'

        varTypes = f'1: {type(stepper2SettingsEntries[0])} 2: {type(stepper2SettingsEntries[1])} 3: {type(stepper2SettingsEntries[2])}'
        varTypes += f'4: {type(stepper2SettingsEntries[3])} 5:{type(stepper2SettingsEntries[4])} 6: {type(stepper2SettingsEntries[5])}'
        varTypes += f'7: {type(stepper2SettingsEntries[6])} 8: {type(stepper2SettingsEntries[7])}'
        print(stringToPrint)
        print(varTypes)

    def option1Update(self, selection):
        stepper2SettingsEntries[5] = selection     
    def option2Update(self, selection):
        stepper2SettingsEntries[7] = bool(selection)

    def update(self):
        # Get values from entries
        entry_value1 = self.ms1PinEntry.get()
        entry_value2 = self.ms2PinEntry.get()
        entry_value3 = self.ms3PinEntry.get()
        entry_value4 = self.directionPinEntry.get()
        entry_value5 = self.stepPinEntry.get() 
        entry_value6 = self.walkDistanceEntry.get()          

        # Save values globally
        stepper2SettingsEntries[0] = int(entry_value1)
        stepper2SettingsEntries[1] = int(entry_value2)
        stepper2SettingsEntries[2] = int(entry_value3)
        stepper2SettingsEntries[3] = int(entry_value4)
        stepper2SettingsEntries[4] = int(entry_value5)
        stepper2SettingsEntries[6] = int(entry_value6)

        # Print
        self.print_stepper_entries()
    def move(self):
        print("got into stepper 2 move!")
         # Initialize the stepper
        ms1Pin = stepper2SettingsEntries[0]
        ms2Pin = stepper2SettingsEntries[1]
        ms3Pin = stepper2SettingsEntries[2]
        directionPin = stepper2SettingsEntries[3]
        stepPin = stepper2SettingsEntries[4]
        stepType = stepper2SettingsEntries[5]
        walkDistance = stepper2SettingsEntries[6]
        clockwise = stepper2SettingsEntries[7]

        GPIO_pins = (ms1Pin, ms2Pin, ms3Pin)      
        mymotortest = RpiMotorLib.A4988Nema(directionPin, stepPin, GPIO_pins, "A4988")

        # Execute command      
        mymotortest.motor_go(not clockwise, stepType, walkDistance, 0.01, False, .05)

        print("finished stepper 2 move!")


def open_settings_window():
    # Define window configuration
    window = Toplevel(gui)
    window.title("Settings")
    window.geometry("640x560")
    window.resizable(False,False)

    # Define tab control widget & tabs
    tabControl = ttk.Notebook(window)
    tab1Frame = ttk.Frame(tabControl)
    tab2Frame = ttk.Frame(tabControl)
    tab3Frame = ttk.Frame(tabControl)

    firstTab = Servo_Settins_Tab(tab1Frame)
    firstTab.print_servo_entries()

    secondTab = Stepper1_Settings_Tab(tab2Frame)
    secondTab.print_stepper_entries()

    thirdTab = Stepper2_Settings_Tab(tab3Frame)
    thirdTab.print_stepper_entries()

    # Add tabs to tab control widget
    tabControl.add(tab1Frame, text='Servo settings')
    tabControl.add(tab2Frame, text='Stepper 1 (egg) settings')    
    tabControl.add(tab3Frame, text='Stepper 2 (pen) settings')

    # Render
    tabControl.pack(expand=1,fill='both')

    window.mainloop()



def quit_program():
    exit(0)

#Define UI stuff
mylabel = Label(gui, text = "Eggbot", font = ("Helvetica", 36 ), bg=backgroundColor)
mylabel.pack(side=TOP, pady = 50)

template1Button = Button(gui, text="Template 1", font = templateButtonFont, width = 9, fg = templateButtonTextColor)
template1Button.place(x=45,y=200)

template2Button = Button(gui, text="Template 2", font = templateButtonFont, width = 9, fg = templateButtonTextColor)
template2Button.place(x=310,y=200)

template3Button = Button(gui, text="Template 3", font = templateButtonFont, width = 9, fg = templateButtonTextColor)
template3Button.place(x=570,y=200)

settingButton = Button(gui, text="Settings", font = templateButtonFont, width = 9, fg = 'black', command=open_settings_window)
settingButton.place(x=310,y=320)

quitButton = Button(gui, text="Quit", font = templateButtonFont, width=9, fg = quitTextColor, command=quit_program)
quitButton.place(x=310,y=440)

gui.mainloop()  