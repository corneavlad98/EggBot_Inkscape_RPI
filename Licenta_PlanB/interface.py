
from tkinter import *

#Define some colors
backgroundColor = '#92b8c5' # cyan-ish color
buttonTextColor = '#bf3adc' # purple color
quitTextColor = '#bb0000' # red color

#Initialize the UI
gui = Tk(className = "Eggbot Main Menu")
gui.geometry("800x600")
gui.resizable(False,False)
gui['background']=backgroundColor

templateButtonFont = ("Helvetica", 24, )


def open_settings_window():
    window = Toplevel(gui)
    window.title("Settings")
    window.geometry("640x480")

def quit_program():
    exit(0)

#Define UI stuff
mylabel = Label(gui, text = "Eggbot", font = ("Helvetica", 36 ), bg=backgroundColor)
mylabel.pack(side=TOP, pady = 50)

template1Button = Button(gui, text="Template 1", font = templateButtonFont, width = 9, fg = buttonTextColor)
template1Button.place(x=45,y=200)

template2Button = Button(gui, text="Template 2", font = templateButtonFont, width = 9, fg = buttonTextColor)
template2Button.place(x=310,y=200)

template3Button = Button(gui, text="Template 3", font = templateButtonFont, width = 9, fg = buttonTextColor)
template3Button.place(x=570,y=200)

settingButton = Button(gui, text="Settings", font = templateButtonFont, width = 9, fg = 'black', command=open_settings_window)
settingButton.place(x=310,y=320)

quitButton = Button(gui, text="Quit", font = templateButtonFont, width=9, fg = quitTextColor, command=quit_program)
quitButton.place(x=310,y=440)



gui.mainloop()  