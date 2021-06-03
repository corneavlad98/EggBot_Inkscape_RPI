from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from tkinter import messagebox
from PIL import ImageTk,Image 
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

servoSettingsEntries = [4, 92, 110, True]
stepper1SettingsEntries = [14, 15, 18, 21, 20, '1/4', 10, True]
stepper2SettingsEntries = [17, 27, 22, 26, 19, '1/8', 10, True]
lastPenAngle = servoSettingsEntries[1]
servoIsUp = None

path1_PC = "C:/Users/Vlad/Desktop/EggBot_Inkscape_RPI/Licenta_PlanB/egg1_alt.jpg"
path2_PC = "C:/Users/Vlad/Desktop/EggBot_Inkscape_RPI/Licenta_PlanB/egg2.jpg"
path1_RPI = "/home/pi/Desktop/EggBot_Inkscape_RPI/Licenta_PlanB/egg1_alt.jpg"
path2_RPI = "/home/pi/Desktop/EggBot_Inkscape_RPI/Licenta_PlanB/egg2.jpg"
class ServoMotor():
    def __init__(self, pin):
        self.servo = int(pin)      

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.servo, GPIO.OUT )

        self.pwm = pigpio.pi() 
        self.pwm.set_mode(self.servo, pigpio.OUTPUT)

        #self.pwm.set_PWM_frequency(self.servo, 50 )
        self.setFrequency(50)
    def updatePin(self, pin):
        self.servo = int(pin)
    def setFrequency(self, frequency):
        self.pwm.set_PWM_frequency(self.servo, frequency )
    def movePenToAngle(self, angle):     
        addedPulse = math.ceil((angle * 1000) / 90)
        self.pwm.set_servo_pulsewidth(self.servo, 500 + addedPulse)  

        time.sleep(1)
    def movePenToAngleSlow(self, angle, delta):
        global lastPenAngle
        self.setFrequency(50)
        
        startAddedPulse = math.ceil((lastPenAngle * 1000) / 90)
        endAddedPulse = math.ceil((angle * 1000) / 90)

        start = 500 + startAddedPulse
        end = 500 + endAddedPulse
        incMove = (end-start)/100.0
        incTime = delta/100.0

        for x in range(100):
            self.pwm.set_servo_pulsewidth(self.servo, int(start+x*incMove))
            time.sleep(incTime)
        
        lastPenAngle = angle
        self.turnOff()
    def turnOff(self):
        # turning off servo
        print("turning off servo")
        self.pwm.set_PWM_dutycycle(self.servo, 0)
        self.pwm.set_PWM_frequency(self.servo, 0 )
class Stepper():
    def __init__(self, stepperNumber, ms1Pin, ms2Pin, ms3Pin, directionPin, stepPin, stepType):
        self.stepperNumber = stepperNumber
        self.stepType = stepType
        self.ms1Pin = ms1Pin
        self.ms2Pin = ms2Pin
        self.ms3Pin = ms3Pin
        self.directionPin = directionPin
        self.stepPin = stepPin
        self.GPIO_pins = (self.ms1Pin, self.ms2Pin, self.ms3Pin)
        self.myStepper = RpiMotorLib.A4988Nema(self.directionPin, self.stepPin, self.GPIO_pins, "A4988")   

    def moveSteps(self, steps, clocwise, sleep):
        self.myStepper.motor_go(not clocwise, self.stepType, steps, 0.005, False, .05)
        time.sleep(sleep)
    def stopStepper(self):
        self.myStepper.motor_stop()
        print("stopping stepper!")
    def updatePins(self, ms1Pin, ms2Pin, ms3Pin, directionPin, stepPin, stepType):
        self.ms1Pin = ms1Pin
        self.ms2Pin = ms2Pin
        self.ms3Pin = ms3Pin
        self.directionPin = directionPin
        self.stepPin = stepPin
        self.stepType = stepType
        self.GPIO_pins = (self.ms1Pin, self.ms2Pin, self.ms3Pin)


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

        self.servoMotor = ServoMotor(servoSettingsEntries[0])
    
    def add_labels(self, tab):
        # Labels
        self.servoPinLabel = Label(tab, text="Servo pin number (GPIO numbering): ", font=labelFont)
        self.servoPinLabel.place(x=50 + self.padding_x,y=65 + self.padding_y)

        self.servoUpLabel = Label(tab, text="Pen up position, servo at (0-180): ", font=labelFont)
        self.servoUpLabel.place(x=50 + self.padding_x,y=120 + self.padding_y)

        self.servoDownLabel = Label(tab, text="Pen down position, servo at (0-180): ", font=labelFont)
        self.servoDownLabel.place(x=50 + self.padding_x,y=175 + self.padding_y)

        self.penGoUpLabel = Label(tab, text="Pen goes up: ", font=labelFont)
        self.penGoUpLabel.place(x=50 + self.padding_x, y=230 + self.padding_y)

        self.details = "-Raise and lower pen to check pen-up and pen-down positions"
        self.detailsLabel = Label(tab, text=self.details, font=detailsTextFont)
        self.detailsLabel.place(x=25 + self.padding_x, y=300 + self.padding_y)
          
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

        self.penGoesUpList = [True, False]
        self.intvar = IntVar(tab)
        self.intvar.set(servoSettingsEntries[3]) # default value
        self.penGoesUpOptionMenu = OptionMenu(tab, self.intvar, *self.penGoesUpList, command=self.optionUpdate)
        self.penGoesUpOptionMenu.config(font=optionMenuFont)
        self.penGoesUpOptionMenu.place(x=378 + self.padding_x,y=227 + self.padding_y, width=86, height=35)
    
    def print_servo_entries(self):
        print(f'Servo pin: {servoSettingsEntries[0]} Up position: {servoSettingsEntries[1]} Down position: {servoSettingsEntries[2]} Pen goes up: {servoSettingsEntries[3]}')      
    def update(self):
        # Get values from entries
        entry_value1 = self.servoPinEntry.get()
        entry_value2 = self.servoUpEntry.get()
        entry_value3 = self.servoDownEntry.get()

        # Save values globally
        servoSettingsEntries[0] = int(entry_value1)
        servoSettingsEntries[1] = int(entry_value2)
        servoSettingsEntries[2] = int(entry_value3)

        self.servoMotor.updatePin(servoSettingsEntries[0])
       
        # Print
        self.print_servo_entries()
    def optionUpdate(self, selection):
        servoSettingsEntries[3] = bool(selection)


    def move(self):
        #print("got into servo move!")      
        servoUpAngle = int(servoSettingsEntries[1])
        servoDownAngle = int(servoSettingsEntries[2])
        penGoesUp = servoSettingsEntries[3]
        global lastPenAngle
        global servoIsUp

        self.servoMotor.setFrequency(50)
               
        if(penGoesUp and not servoIsUp):
            print("going up!")
            lastPenAngle = servoDownAngle
            print(f'Last angle: {lastPenAngle}')          
            self.servoMotor.movePenToAngleSlow(servoUpAngle, 0.5)
            servoIsUp = True
            print("finished servo move!")
        elif(penGoesUp and servoIsUp):
            print("pen is already up!")
        elif(not penGoesUp and servoIsUp):
            print("going down!")
            lastPenAngle = servoUpAngle
            print(f'Last angle: {lastPenAngle}')
            self.servoMotor.movePenToAngleSlow(servoDownAngle, 0.5)
            servoIsUp = False
            print("finished servo move!")
        time.sleep(1)      
      
        # turning off servo
        self.servoMotor.turnOff()

       
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

        self.stepper = Stepper(1, stepper1SettingsEntries[0], stepper1SettingsEntries[1], stepper1SettingsEntries[2], stepper1SettingsEntries[3], stepper1SettingsEntries[4], stepper1SettingsEntries[5])  

    
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

        # varTypes = f'1: {type(stepper1SettingsEntries[0])} 2: {type(stepper1SettingsEntries[1])} 3: {type(stepper1SettingsEntries[2])}'
        # varTypes += f'4: {type(stepper1SettingsEntries[3])} 5:{type(stepper1SettingsEntries[4])} 6: {type(stepper1SettingsEntries[5])}'
        # varTypes += f'7: {type(stepper1SettingsEntries[6])} 8: {type(stepper1SettingsEntries[7])}'
        print(stringToPrint)
        #print(varTypes)

    def option1Update(self, selection):
        stepper1SettingsEntries[5] = selection 
        self.stepper.updatePins(stepper1SettingsEntries[0], stepper1SettingsEntries[1], stepper1SettingsEntries[2], stepper1SettingsEntries[3], stepper1SettingsEntries[4], stepper1SettingsEntries[5])    
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

        self.stepper.updatePins(stepper1SettingsEntries[0], stepper1SettingsEntries[1], stepper1SettingsEntries[2], stepper1SettingsEntries[3], stepper1SettingsEntries[4], stepper1SettingsEntries[5])    

        # Print
        self.print_stepper_entries()
    def move(self):
        print("got into stepper 1 move!")
        walkDistance = stepper1SettingsEntries[6]
        clockwise = stepper1SettingsEntries[7]

        self.stepper.moveSteps(walkDistance, clockwise, 1)
        self.stepper.stopStepper()

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

        self.stepper = Stepper(1, stepper2SettingsEntries[0], stepper2SettingsEntries[1], stepper2SettingsEntries[2], stepper2SettingsEntries[3], stepper2SettingsEntries[4], stepper2SettingsEntries[5])  

    
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

        # varTypes = f'1: {type(stepper2SettingsEntries[0])} 2: {type(stepper2SettingsEntries[1])} 3: {type(stepper2SettingsEntries[2])}'
        # varTypes += f'4: {type(stepper2SettingsEntries[3])} 5:{type(stepper2SettingsEntries[4])} 6: {type(stepper2SettingsEntries[5])}'
        # varTypes += f'7: {type(stepper2SettingsEntries[6])} 8: {type(stepper2SettingsEntries[7])}'
        print(stringToPrint)
        #print(varTypes)

    def option1Update(self, selection):
        stepper2SettingsEntries[5] = selection
        self.stepper.updatePins(stepper2SettingsEntries[0], stepper2SettingsEntries[1], stepper2SettingsEntries[2], stepper2SettingsEntries[3], stepper2SettingsEntries[4], stepper2SettingsEntries[5])    
    
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

        self.stepper.updatePins(stepper2SettingsEntries[0], stepper2SettingsEntries[1], stepper2SettingsEntries[2], stepper2SettingsEntries[3], stepper2SettingsEntries[4], stepper2SettingsEntries[5])    

        # Print
        self.print_stepper_entries()
    def move(self):
        print("got into stepper 2 move!")       
        walkDistance = stepper2SettingsEntries[6]
        clockwise = stepper2SettingsEntries[7]

        self.stepper.moveSteps(walkDistance, clockwise, 1)
        self.stepper.stopStepper()
        print("finished stepper 2 move!")


   
    
  
       
def print_all():
        print(f'Servo pin: {servoSettingsEntries[0]} Up position: {servoSettingsEntries[1]} Down position: {servoSettingsEntries[2]} Pen goes up: {servoSettingsEntries[3]}')
        
        stepper1ToPrint = f'MS1 pin: {stepper1SettingsEntries[0]} MS2 pin: {stepper1SettingsEntries[1]} MS3 pin: {stepper1SettingsEntries[2]} '
        stepper1ToPrint += f'Direction pin: {stepper1SettingsEntries[3]} Step pin: {stepper1SettingsEntries[4]} Step type: {stepper1SettingsEntries[5]} '
        stepper1ToPrint += f'Walk distance: {stepper1SettingsEntries[6]} Clockwise: {stepper1SettingsEntries[7]}'
        print(stepper1ToPrint)

        stepper2ToPrint = f'MS1 pin: {stepper2SettingsEntries[0]} MS2 pin: {stepper2SettingsEntries[1]} MS3 pin: {stepper2SettingsEntries[2]} '
        stepper2ToPrint += f'Direction pin: {stepper2SettingsEntries[3]} Step pin: {stepper2SettingsEntries[4]} Step type: {stepper2SettingsEntries[5]} '
        stepper2ToPrint += f'Walk distance: {stepper2SettingsEntries[6]} Clockwise: {stepper2SettingsEntries[7]}'
        print(stepper2ToPrint)       
def quit_program():
    exit(0)

def on_closing(servo):
    servo.turnOff()
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

    #Move servo in initial position (up)
    servo = ServoMotor(servoSettingsEntries[0])
    servo.movePenToAngleSlow(servoSettingsEntries[1], 2)
    global servoIsUp
    servoIsUp = True
    print(servoIsUp)

    window.protocol("WM_DELETE_WINDOW", on_closing(servo))
    window.mainloop()

def open_template1_window():
    # Define window configuration
    window = Toplevel(gui)
    window.title("Template 1")
    window.geometry("640x560")
    window.resizable(False,False)

    image = Image.open(path1_RPI)
    resized = image.resize((210, 290), Image.ANTIALIAS)  
    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(resized)

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = Label(window, image = img)
    panel.place(x=390,y=50)

    label1 = Label(window, text="Here's how template 1 should look like:  ", font=labelFont)
    label1.place(x=20, y=70)

    warning1 = "Before plotting, please make sure \n everything was set up properly."
    label2 = Label(window, text=warning1, font=labelFont)
    label2.place(x=20, y=150)

    label3 = Label(window, text="For this, go to the 'Settings' tab", font=labelFont)
    label3.place(x=30, y=250)

    label4 = Label(window, text="When you are ready, press this button", font=labelFont)
    label4.place(x=150, y=440)
    #print_all()
    plotButton = Button(window, text="Plot", font = buttonFont, width = 5, fg = 'black', command=plotTemplate1)
    plotButton.place(x=285,y=490)

    window.mainloop()  
def open_template2_window():
    # Define window configuration
    window = Toplevel(gui)
    window.title("Template 2")
    window.geometry("640x560")
    window.resizable(False,False)

    image = Image.open(path2_RPI)
    resized = image.resize((210, 290), Image.ANTIALIAS)  
    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(resized)

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = Label(window, image = img)
    panel.place(x=390,y=50)

    label1 = Label(window, text="Here's how template 2 should look like:  ", font=labelFont)
    label1.place(x=20, y=70)

    warning1 = "Before plotting, please make sure \n everything was set up properly."
    label2 = Label(window, text=warning1, font=labelFont)
    label2.place(x=20, y=150)

    label3 = Label(window, text="For this, go to the 'Settings' tab", font=labelFont)
    label3.place(x=30, y=250)

    label4 = Label(window, text="When you are ready, press this button", font=labelFont)
    label4.place(x=150, y=440)
    #print_all()
    plotButton = Button(window, text="Plot", font = buttonFont, width = 5, fg = 'black', command=plotTemplate2)
    plotButton.place(x=285,y=490)

    window.mainloop()
def open_template3_window():
    # Define window configuration
    window = Toplevel(gui)
    window.title("Template 3")
    window.geometry("640x560")
    window.resizable(False,False)

    image = Image.open(path1_RPI)
    resized = image.resize((210, 290), Image.ANTIALIAS)  
    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(resized)

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = Label(window, image = img)
    panel.place(x=390,y=50)

    label1 = Label(window, text="Here's how template 3 should look like:  ", font=labelFont)
    label1.place(x=20, y=70)

    warning1 = "Before plotting, please make sure \n everything was set up properly."
    label2 = Label(window, text=warning1, font=labelFont)
    label2.place(x=20, y=150)

    label3 = Label(window, text="For this, go to the 'Settings' tab", font=labelFont)
    label3.place(x=30, y=250)

    label4 = Label(window, text="When you are ready, press this button", font=labelFont)
    label4.place(x=150, y=440)
    #print_all()
    
    plotButton = Button(window, text="Plot", font = buttonFont, width = 5, fg = 'black', command=plotTemplate3)
    plotButton.place(x=285,y=490)

    window.mainloop()

def plotTemplate1():
    print("got into plotting first template!")
    # Initialize servo
    servo = ServoMotor(servoSettingsEntries[0])
    penUpAngle = servoSettingsEntries[1]
    penDownAngle = servoSettingsEntries[2]

    # Initialize stepper 1 (egg)
    stepper1 = Stepper(1, stepper1SettingsEntries[0], stepper1SettingsEntries[1], stepper1SettingsEntries[2], stepper1SettingsEntries[3], stepper1SettingsEntries[4], stepper1SettingsEntries[5])  
    # Initialize stepper 2 (pen)
    stepper2 = Stepper(2, stepper2SettingsEntries[0], stepper2SettingsEntries[1], stepper2SettingsEntries[2], stepper2SettingsEntries[3], stepper2SettingsEntries[4], stepper1SettingsEntries[5])
    
    # Add a stopping variable
    finished = False
    sideSteps = 100
    fullRotation = 840
    global lastPenAngle
    lastPenAngle = penUpAngle

    def drawMiddleCircle():
        # Lower pen
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 1)
        
        # Clockwise rotation
        print("rotating egg!")
        stepper1.moveSteps(fullRotation, True, 1)
        # Lift pen
        print("Lifting pen slow!")
        servo.movePenToAngleSlow(penUpAngle, 1)

    def drawLeftMiddleCircle():
        #Go left
        print("Going left!")
        stepper2.moveSteps(int(sideSteps / 2) + 10, False, 1)
        # Lower pen
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 1)
        # Clockwise Rotation
        print("Rotating egg!")
        stepper1.moveSteps(fullRotation, True, 1)
        # Lift pen
        print("Lifting pen slow!")
        servo.movePenToAngleSlow(penUpAngle, 1)

    def drawLeftCircle():
        #Go left
        print("Going left!")
        stepper2.moveSteps(int(sideSteps / 2) - 10, False, 1)
        # Lower pen
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle - 4, 1)
        # Clockwise Rotation
        print("Rotating egg!")
        stepper1.moveSteps(fullRotation, True, 1)
        # Lift pen
        print("Lifting pen slow!")
        servo.movePenToAngleSlow(penUpAngle, 1)
        
    def drawRightMiddleCircle():
        # Go to right
        print("Going right!")
        stepper2.moveSteps(int(sideSteps / 2), True, 1)
        # Lower pen
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 1)
        # Clockwise Rotation
        print("Rotating egg!")
        stepper1.moveSteps(fullRotation, True, 1)
        # Lift pen
        print("Lifting pen slow!")
        servo.movePenToAngleSlow(penUpAngle, 1)

    def drawRightCircle():
        # Go to right
        print("Going right!")
        stepper2.moveSteps(int(sideSteps / 2), True, 1)
        # Lower pen
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 1)
        # Clockwise Rotation
        print("Rotating egg!")
        stepper1.moveSteps(fullRotation, True, 1)
        # Lift pen
        print("Lifting pen slow!")
        servo.movePenToAngleSlow(penUpAngle, 1)

    while not finished:     
        try:   
            drawMiddleCircle()
            drawLeftMiddleCircle()
            drawLeftCircle()        
            
            # Go back to middle
            print("Going to middle!")
            stepper2.moveSteps(sideSteps, True, 1)         

            drawRightMiddleCircle()
            drawRightCircle()

            # Go back to middle
            print("Going to middle!")
            stepper2.moveSteps(sideSteps, False, 1)

            finished = True
        except KeyboardInterrupt:
            print("got interrupted!")
            break
    
    # stopping motors
    servo.turnOff()
    stepper1.stopStepper()
    stepper2.stopStepper()

 
    print("finished plotting first template!")
def plotTemplate2():
    print("got into plotting second template!")
    # Initialize servo
    servo = ServoMotor(servoSettingsEntries[0])
    penUpAngle = servoSettingsEntries[1]
    penDownAngle = servoSettingsEntries[2]

    # Initialize stepper 1 (egg)
    stepper1 = Stepper(1, stepper1SettingsEntries[0], stepper1SettingsEntries[1], stepper1SettingsEntries[2], stepper1SettingsEntries[3], stepper1SettingsEntries[4], stepper1SettingsEntries[5])  
    # Initialize stepper 2 (pen)
    stepper2 = Stepper(2, stepper2SettingsEntries[0], stepper2SettingsEntries[1], stepper2SettingsEntries[2], stepper2SettingsEntries[3], stepper2SettingsEntries[4], stepper1SettingsEntries[5])
    
    stepper1SquareSteps = 144
    stepper2SquareSteps = 72
    global lastPenAngle
    lastPenAngle = penUpAngle

    def drawSquare():
        #Go left a little
        print("Going left!")
        stepper2.moveSteps(stepper2SquareSteps, False, 1)

        #Rotate clockwise
        print("Rotating clockwise!")
        stepper1.moveSteps(stepper1SquareSteps, True, 1)

        #Lower pen
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 0.75)

        #Rotate counter-clocwise
        print("Rotating counter-clockwise!")
        stepper1.moveSteps(stepper1SquareSteps, False, 1)

        #Go to opposite right
        print("Going right!")
        stepper2.moveSteps(stepper2SquareSteps * 2, True, 1)

        #Rotate clockwise
        print("Rotating clockwise!")
        stepper1.moveSteps(stepper1SquareSteps, True, 1)

        #Go to opposite left
        print("Going left!")
        stepper2.moveSteps(stepper2SquareSteps * 2, False, 1)

        #Lift pen
        print("Lifting pen!")
        servo.movePenToAngleSlow(penUpAngle, 0.75)
        print("Finished drawing square!")

    def drawFirstEye():
        # Drawing first eye
        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/4), False, 1)

        print("Going right")
        stepper2.moveSteps(int(stepper2SquareSteps/2), True, 1)

        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 0.75)

        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/2), True, 1)
        
        #Lift pen
        print("Lifting pen!")
        servo.movePenToAngleSlow(penUpAngle, 0.75)
        print("Finished drawing first eye!")

    def drawSecondEye():
        # Drawing second eye           
        print("Going left!")
        stepper2.moveSteps(int(stepper2SquareSteps/2), False, 1)

        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/2), False, 1)
                       
        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 0.75)

        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/2), True, 1)
        #Lift pen
        print("Lifting pen!")
        servo.movePenToAngleSlow(penUpAngle, 0.75)
        print("Finished drawing second eye!")

    def drawMouth():
        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/8), False, 1)

        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/4), True, 1)

        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 0.75)

        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/2), True, 1)
         
        print("Rotating clockwise!")
        stepper1.moveSteps(int((stepper1SquareSteps/4)*3) , True, 1)

        print("Going left!")
        stepper2.moveSteps(int(stepper2SquareSteps/2), False, 1)
        #Lift pen
        print("Lifting pen!")
        servo.movePenToAngleSlow(penUpAngle, 0.75)
        print("Finished drawing mouth!")
    def drawAntenna():
        # Going to lower edge
        print("Rotating clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/8), True, 1)
        # Going to left side
        print("Going left!")
        stepper2.moveSteps(int((stepper2SquareSteps * 3)/4), False, 1)

        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/2), False, 1)

        print("Lowering pen!")
        servo.movePenToAngleSlow(penDownAngle, 1)

        print("Going left!")
        stepper2.moveSteps(int(stepper2SquareSteps/4), False, 1)

        print("Rotating clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/16), True, 1)

        print("Going left!")
        stepper2.moveSteps(int(stepper2SquareSteps/8), False, 1)

        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/8), False, 1)

        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/8), True, 1)

        print("Rotating clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/16), True, 1)
        #Lift pen
        print("Lifting pen!")
        servo.movePenToAngleSlow(penUpAngle, 0.75)
        print("Finished drawing antenna!")

    def goToInitialPoint():
        #Going back to initial point
        print("Going left!")
        stepper2.moveSteps(int(stepper2SquareSteps/4), False, 1)

        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps - int((stepper1SquareSteps/8))), False, 1)
    def goToInitialPoint2():
        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/4), True, 1)

        print("Rotating counter-clockwise!")
        stepper1.moveSteps(int(stepper1SquareSteps/2), False, 1)

        print("Going right!")
        stepper2.moveSteps(int(stepper2SquareSteps/2), True, 1)
    # Add a stopping variable
    finished = False
    while not finished:
        try:              
            drawSquare()
            #We should have a square by now
            drawFirstEye()
            drawSecondEye()
            # Should have both eyes by now
            drawMouth()
            # Should have a mouth
            #goToInitialPoint()
            drawAntenna()
            goToInitialPoint2()
            
            finished = True
        except KeyboardInterrupt:
            print("got interrupted!")
            break

    
    # stopping motors
    servo.turnOff()
    stepper1.stopStepper()
    stepper2.stopStepper()

 
    print("finished plotting second template!")


def plotTemplate3():
    print("got into plotting third template!")
    # Initialize servo
    servo = ServoMotor(servoSettingsEntries[0])
    penUpAngle = servoSettingsEntries[1]
    penDownAngle = servoSettingsEntries[2]

    # Initialize stepper 1 (egg)
    stepper1 = Stepper(1, stepper1SettingsEntries[0], stepper1SettingsEntries[1], stepper1SettingsEntries[2], stepper1SettingsEntries[3], stepper1SettingsEntries[4], '1/4')  
    # Initialize stepper 2 (pen)
    stepper2 = Stepper(2, stepper2SettingsEntries[0], stepper2SettingsEntries[1], stepper2SettingsEntries[2], stepper2SettingsEntries[3], stepper2SettingsEntries[4], '1/8')
    
    fullArmSteps = 200
    fullEggSteps = 820
    global lastPenAngle
    lastPenAngle = penUpAngle

    def drawRamp(eggClockwise, armClockwise):
        i = 0
        while i < 100:
            stepper2.moveSteps(2, armClockwise, 0)
            stepper1.moveSteps(2, eggClockwise, 0)
            if i % 40 == 0 and i != 0:
                stepper1.moveSteps(2, eggClockwise, 0)
            i += 1


    # Add a stopping variable
    finished = False
    while not finished:
        try:
            print("lifting pen!")
            servo.movePenToAngleSlow(penUpAngle, 0.75)
                          
            print("going right!")
            stepper2.moveSteps(int(fullArmSteps / 2), True, 1)

            print("Lowering pen!")
            servo.movePenToAngleSlow(penDownAngle, 0.75)

            drawRamp(eggClockwise=False, armClockwise=False)
            drawRamp(eggClockwise=False, armClockwise=True)
            drawRamp(eggClockwise=False, armClockwise=False)
            drawRamp(eggClockwise=False, armClockwise=True)

            print("Lifting pen!")
            servo.movePenToAngleSlow(penUpAngle, 0.75)

            # print("rotating clockwise!")
            # stepper1.moveSteps(int(fullEggSteps / 4), True, 1)

            # print("going back to middle")
            # stepper2.moveSteps(int(fullArmSteps / 2), True, 1)

            print("going back to middle")
            stepper2.moveSteps(int(fullArmSteps / 2), False, 1)


            finished = True
        except KeyboardInterrupt:
            print("got interrupted!")
            break

    
    # stopping motors
    servo.turnOff()
    stepper1.stopStepper()
    stepper2.stopStepper()
 
    print("finished plotting third template!")






#Define UI stuff
mylabel = Label(gui, text = "Eggbot", font = ("Helvetica", 36 ), bg=backgroundColor)
mylabel.pack(side=TOP, pady = 50)

template1Button = Button(gui, text="Template 1", font = templateButtonFont, width = 9, fg = templateButtonTextColor, command=open_template1_window)
template1Button.place(x=45,y=200)

template2Button = Button(gui, text="Template 2", font = templateButtonFont, width = 9, fg = templateButtonTextColor, command=open_template2_window)
template2Button.place(x=310,y=200)

template3Button = Button(gui, text="Template 3", font = templateButtonFont, width = 9, fg = templateButtonTextColor, command=open_template3_window)
template3Button.place(x=570,y=200)

settingButton = Button(gui, text="Settings", font = templateButtonFont, width = 9, fg = 'black', command=open_settings_window)
settingButton.place(x=310,y=320)

quitButton = Button(gui, text="Quit", font = templateButtonFont, width=9, fg = quitTextColor, command=quit_program)
quitButton.place(x=310,y=440)

gui.mainloop()  