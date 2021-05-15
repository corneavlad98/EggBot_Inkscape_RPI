from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD

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

def servo_settings_tab(tab):
    # Title Label
    titleLabel = Label(tab, text="EggBot: Basic Setup - Servo Motor ", font=titleLabelFont)
    titleLabel.place(x=20,y=15)

    padding_x = 45
    padding_y = 25
    # Labels
    servoPinLabel = Label(tab, text="Servo pin number (GPIO numbering): ", font=labelFont)
    servoPinLabel.place(x=50 + padding_x,y=65 + padding_y)

    servoUpLabel = Label(tab, text="Pen up position, servo at (0-180): ", font=labelFont)
    servoUpLabel.place(x=50 + padding_x,y=120 + padding_y)

    servoDownLabel = Label(tab, text="Pen down position, servo at (0-180): ", font=labelFont)
    servoDownLabel.place(x=50 + padding_x,y=175 + padding_y)

    details = "-Raise and lower pen to check pen-up and pen-down positions"
    detailsLabel = Label(tab, text=details, font=detailsTextFont)
    detailsLabel.place(x=25 + padding_x, y=275 + padding_y)

    # Entry fields
    servoPinEntry = Entry(tab, font=entryFieldFont)
    servoPinEntry.insert(0, '4')
    servoPinEntry.place(x=400 + padding_x,y=67 + padding_y, width=46, height=30)

    servoUpEntry = Entry(tab, font=entryFieldFont)
    servoUpEntry.insert(0, '105')
    servoUpEntry.place(x=400 + padding_x,y=122 + padding_y, width=46, height=30)

    servoDownEntry = Entry(tab, font=entryFieldFont)
    servoDownEntry.insert(0, '140')
    servoDownEntry.place(x=400 + padding_x,y=177 + padding_y, width=46, height=30)
    
    # Add save button
    saveButton = Button(tab, text="Save", font = saveButtonFont, width = 5, fg = 'black')
    saveButton.place(x=290,y=420)

def open_settings_window():
    # Define window configuration
    window = Toplevel(gui)
    window.title("Settings")
    window.geometry("640x520")
    window.resizable(False,False)

    # Define tab control widget & tabs
    tabControl = ttk.Notebook(window)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)

    # Add tabs to tab control widget
    tabControl.add(tab1, text='Servo settings')
    tabControl.add(tab2, text='Stepper 1 (egg) settings')    
    tabControl.add(tab3, text='Stepper 2 (pen) settings')
    # Render
    tabControl.pack(expand=1,fill='both')

    servo_settings_tab(tab1)

    # saveButton2 = Button(tab2, text="Save", font = saveButtonFont, width = 5, fg = 'black')
    # saveButton2.place(x=290,y=420)

    # saveButton3 = Button(tab3, text="Save", font = saveButtonFont, width = 5, fg = 'black')
    # saveButton3.place(x=290,y=420)


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