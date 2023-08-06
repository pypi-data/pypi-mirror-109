import json
from tkinter import *
from tkinter import messagebox

from firebase import firebase

import DataClasses
import teacherHome


def loginWindow():
    rootLogin.destroy()
    print('Here')
    teacherHome.main(loggedInUser)


def check():
    global loggedInUser
    UId, password = '', ''
    enteredUID = bookInfo1.get()
    enteredPass = bookInfo2.get()

    firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
    result = firebaseDb.get('/TeacherLogin', '')
    if result:
        for dt in result:
            if result[dt]["Email"] == enteredUID:
                UId = result[dt]["Email"]
                password = result[dt]["Password"]

            if enteredUID == UId and enteredPass == password and enteredPass and enteredUID:
                user = result[dt]
                if "Subjects" in user.keys():
                    loggedInUser = DataClasses.TeacherDetails(user['Name'], user['Department'], user['Email'],
                                                              user['College'], user['Subjects'])
                else:
                    loggedInUser = DataClasses.TeacherDetails(user['Name'], user['Department'], user['Email'],
                                                              user['College'])
                print(loggedInUser.getDetails())

                with open('metadata.json', 'w') as metadataFile:
                    data = {'LoggedInUser': {'Data': loggedInUser.getDetails(), 'Type': 'Teacher'}}
                    json.dump(data, metadataFile, indent=4)
                    metadataFile.close()

                loginWindow()

    else:
        messagebox.showwarning("Failed", "Invalid Credentials.\n Please Check entered Credentials.")


def checkLoggedInUser():
    global loggedInUser
    try:
        with open('metadata.json', 'r+') as metadataFile:
            data = json.load(metadataFile)
            metadataFile.close()
        print(data)
        if 'LoggedInUser' in data.keys():
            user = data['LoggedInUser']['Data']
            print(user)

            if "Subjects" in user.keys():
                print('here')
                loggedInUser = DataClasses.TeacherDetails(user['Name'], user['Department'], user['Email'],
                                                          user['College'], user['Subjects'])
            else:
                loggedInUser = DataClasses.TeacherDetails(user['Name'], user['Department'], user['Email'],
                                                          user['College'])
            print(loggedInUser.getDetails())
            loginWindow()
        else:
            print('No Data Found in dates File')
            return

    except json.JSONDecodeError or FileNotFoundError or Exception as exception:
        print(exception)
        print('No Data Found in dates File')
        return


def loginScreen():
    global rootLogin, bookInfo1, bookInfo2, loggedInUser
    rootLogin = Tk()
    checkLoggedInUser()
    rootLogin.title("Attendance Management")
    rootLogin.minsize(width=400, height=400)
    rootLogin.geometry("600x500+80+150")
    Canvas1 = Canvas(rootLogin)
    Canvas1.config(bg="#3498DB")
    Canvas1.pack(expand=True, fill=BOTH)

    # Set Heading Frame
    headingFrame1 = Frame(rootLogin, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.2, rely=0.04, relwidth=0.6, relheight=0.16)

    headingLabel = Label(headingFrame1, text="Welcome to \n Attendance Management", bg='black', fg='white',
                         font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Frame for Login Area
    labelFrame = Frame(rootLogin, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.3)

    # Login ID
    lb1 = Label(labelFrame, text="Email-Id : ", bg='black', fg='white', font=('Courier', 15))
    lb1.place(relx=0.05, rely=0.25, relheight=0.08)
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.20)

    # Password
    lb2 = Label(labelFrame, text="Password: ", bg='black', fg='white', font=('Courier', 15))
    lb2.place(relx=0.05, rely=0.60, relheight=0.08)
    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3, rely=0.55, relwidth=0.62, relheight=0.20)

    # Button to LOGIN
    btn1 = Button(rootLogin, text="Login", bg='black', fg='white', font=('Courier', 15), command=check)
    btn1.place(relx=0.28, rely=0.63, relwidth=0.45, relheight=0.1)

    rootLogin.state("zoomed")
    rootLogin.resizable(True, True)
    rootLogin.mainloop()


global rootLogin, bookInfo1, bookInfo2, loggedInUser
