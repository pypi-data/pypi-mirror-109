import json
from tkinter import Tk, Canvas, BOTH, Frame, Label, Button

import teacherLogin
import hodLogin


def hod_login():
    global rootMain
    rootMain.destroy()
    hodLogin.loginScreen()


def teacher_login():
    global rootMain
    print('Here I am')
    rootMain.destroy()
    print('Here')
    teacherLogin.loginScreen()


def checkLoggedInUser():
    try:
        with open('metadata.json', 'r+') as metadataFile:
            data = json.load(metadataFile)
            print(data)
            metadataFile.close()
        if 'LoggedInUser' in data.keys():
            print(data['LoggedInUser']['Type'])
            if data['LoggedInUser']['Type'] == 'Hod':
                print(data['LoggedInUser']['Type'])
                hod_login()
            elif data['LoggedInUser']['Type'] == 'Teacher':
                teacher_login()
            else:
                raise Exception
    except FileNotFoundError :
        with open('metadata.json', 'w') as metadataFile:
            metadataFile.close()
        return


def fun():
    global rootMain

    rootMain = Tk()
    checkLoggedInUser()

    rootMain.title("Attendance Management")
    rootMain.minsize(width = 400, height = 400)
    rootMain.geometry("600x500+80+150")
    Canvas1 = Canvas(rootMain)
    Canvas1.config(bg = "#3498DB")
    Canvas1.pack(expand = True, fill = BOTH)
    rootMain.state("zoomed")
    rootMain.resizable(True, True)

    # Heading
    headingFrame1 = Frame(rootMain, bg = "#FFBB00", bd = 5)
    headingFrame1.place(relx = 0.2, rely = 0.04, relwidth = 0.6, relheight = 0.16)

    headingLabel = Label(headingFrame1, text = "Welcome to \n Attendance Management", bg = 'black', fg = 'white',
                         font = ('Courier', 20))
    headingLabel.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Frame for Login Area
    labelFrame = Frame(rootMain, bg = 'black')
    labelFrame.place(relx = 0.1, rely = 0.3, relwidth = 0.8, relheight = 0.5)

    label = Label(rootMain, text = "Select Your Option...", bg = 'black', fg = 'white', font = ('Courier', 15))
    label.place(relx = 0.1, rely = 0.3, relwidth = 0.8, relheight = 0.2)

    btnHod = Button(labelFrame, text = "HOD", bg = '#FFBB00', fg = 'black', font = ('Courier', 15), command = hod_login)
    btnHod.place(relx = 0.15, rely = 0.45, relwidth = 0.25, relheight = 0.2)

    btnTeacher = Button(labelFrame, text = "Teacher", bg = '#FFBB00', fg = 'black', font = ('Courier', 15),
                        command = teacher_login)
    btnTeacher.place(relx = 0.6, rely = 0.45, relwidth = 0.25, relheight = 0.2)

    rootMain.mainloop()


global rootMain
if __name__ == '__main__':
    fun()
