import json
from tkinter import *
from tkinter import messagebox
from firebase import firebase

import DataClasses
import hodRegistration
import hodHome


def hod_register():
    rootHodLogin.destroy()
    hodRegistration.registration()


def hodLogin():
    print('here3')
    rootHodLogin.destroy()
    hodHome.main()


def check():
    global loggedInUser
    UId, password = '', ''
    enteredUID = bookInfo1.get()
    enteredPass = bookInfo2.get()

    firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
    result = firebaseDb.get('/HodLogin', '')
    if result:
        for dt in result:
            if result[dt]['Email'] == enteredUID:
                UId = result[dt]['Email']
                password = result[dt]['Password']

            if enteredUID == UId and enteredPass == password and enteredPass and enteredUID:
                user = result[dt]
                loggedInUser = DataClasses.HodDetails(user['Name'], user['Department'], user['Email'], user['College'],
                                                      user['Classes'])
                with open('metadata.json', 'w+') as metadataFile:
                    data = {'LoggedInUser': {'Data': loggedInUser.getDetails(), 'Type': 'Hod'}}
                    json.dump(data, metadataFile, indent = 4)
                    metadataFile.close()
                hodLogin()

    else:
        messagebox.showwarning("Failed", "Invalid Credentials.\n Please Check entered Credentials.")


def checkLoggedUser():
    global loggedInUser
    try:
        with open('Data/metadata.json', 'r+') as metadataFile:
            data = json.load(metadataFile)
            metadataFile.close()

        if 'LoggedInUser' in data.keys():

            if data['LoggedInUser']:

                user = data['LoggedInUser']['Data']
                loggedInUser = DataClasses.HodDetails(user['Name'], user['Department'], user['Email'], user['College'],
                                                      user['Classes'])

                hodLogin()
            else:
                raise Exception

    except json.JSONDecodeError or FileNotFoundError or Exception:
        print('No Data Found in dates File')


def loginScreen():
    global rootHodLogin, bookInfo1, bookInfo2, loggedInUser
    rootHodLogin = Tk()
    checkLoggedUser()
    rootHodLogin.title("Attendance Management")
    rootHodLogin.minsize(width = 400, height = 400)
    rootHodLogin.geometry("600x500+80+150")
    Canvas1 = Canvas(rootHodLogin)
    Canvas1.config(bg = "#3498DB")
    Canvas1.pack(expand = True, fill = BOTH)

    # Set Heading Frame
    headingFrame1 = Frame(rootHodLogin, bg = "#FFBB00", bd = 5)
    headingFrame1.place(relx = 0.2, rely = 0.04, relwidth = 0.6, relheight = 0.16)

    headingLabel = Label(headingFrame1, text = "Welcome to \n Attendance Management", bg = 'black', fg = 'white',
                         font = ('Courier', 15))
    headingLabel.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Frame for Login Area
    labelFrame = Frame(rootHodLogin, bg = 'black')
    labelFrame.place(relx = 0.1, rely = 0.3, relwidth = 0.8, relheight = 0.3)

    # Login ID
    lb1 = Label(labelFrame, text = "Email-Id : ", bg = 'black', fg = 'white', font = ('Courier', 15))
    lb1.place(relx = 0.05, rely = 0.25, relheight = 0.08)
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx = 0.3, rely = 0.2, relwidth = 0.62, relheight = 0.20)

    # Password
    lb2 = Label(labelFrame, text = "Password: ", bg = 'black', fg = 'white', font = ('Courier', 15))
    lb2.place(relx = 0.05, rely = 0.60, relheight = 0.08)
    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx = 0.3, rely = 0.55, relwidth = 0.62, relheight = 0.20)

    # Button to LOGIN
    btn1 = Button(rootHodLogin, text = "Login", bg = 'black', fg = 'white', font = ('Courier', 15), command = check)
    btn1.place(relx = 0.28, rely = 0.63, relwidth = 0.45, relheight = 0.1)

    # Frame for Registration Button Area
    registrationFrame = Frame(rootHodLogin, bg = 'black', bd = 5)
    registrationFrame.place(relx = 0, rely = 0.89, relwidth = 1, relheight = 0.1)

    registrationLabel = Label(registrationFrame, text = "If you are new HOD then Click Here =>", bg = 'black',
                              fg = 'white', font = ('Courier', 10))
    registrationLabel.place(relx = 0, rely = 0, relwidth = 0.65, relheight = 1)

    # Button to REGISTRATION
    btn2 = Button(registrationFrame, text = "Register", bg = '#9D07F9', bd = 4, fg = 'white',
                  font = ('Courier', 15),
                  command = hod_register)
    btn2.place(relx = 0.65, rely = 0.1, relwidth = 0.3, relheight = 0.8)

    rootHodLogin.state("zoomed")
    rootHodLogin.resizable(True, True)
    rootHodLogin.mainloop()


global rootHodLogin, bookInfo1, bookInfo2, loggedInUser
