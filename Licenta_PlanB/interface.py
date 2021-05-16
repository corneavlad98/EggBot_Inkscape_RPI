from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from tkinter import messagebox

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
saveButtonFont = ("Helvetica", 18 )
entryFieldFont = ("Helvetica", 18 )
labelFont = ("Helvetica", 15 )
titleLabelFont = ("Helvetica", 15, BOLD)
detailsTextFont =("Helvetica", 14)

servoSettingsEntries = ['4', '90', '120']



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
       
        # Add save button to tab
        saveButtonServo = Button(tab, text="Save", font = saveButtonFont, width = 5, fg = 'black', command=self.update)
        saveButtonServo.place(x=290,y=420)
    
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
  

def open_settings_window():
    # Define window configuration
    window = Toplevel(gui)
    window.title("Settings")
    window.geometry("640x520")
    window.resizable(False,False)

    # Define tab control widget & tabs
    tabControl = ttk.Notebook(window)
    tab1Frame = ttk.Frame(tabControl)
    # tab2 = ttk.Frame(tabControl)
    # tab3 = ttk.Frame(tabControl)

    #servo_settings_tab(tab1)
    firstTab = Servo_Settins_Tab(tab1Frame)
    firstTab.print_servo_entries()

    # Add tabs to tab control widget
    tabControl.add(tab1Frame, text='Servo settings')
    # tabControl.add(tab2, text='Stepper 1 (egg) settings')    
    # tabControl.add(tab3, text='Stepper 2 (pen) settings')

    # Render
    tabControl.pack(expand=1,fill='both')

    # saveButton2 = Button(tab2, text="Save", font = saveButtonFont, width = 5, fg = 'black')
    # saveButton2.place(x=290,y=420)

    # saveButton3 = Button(tab3, text="Save", font = saveButtonFont, width = 5, fg = 'black')
    # saveButton3.place(x=290,y=420)
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