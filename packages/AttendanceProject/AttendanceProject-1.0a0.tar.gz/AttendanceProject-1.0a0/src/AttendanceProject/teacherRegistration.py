from tkinter import *
from tkinter import messagebox
import re

from firebase import firebase

import hodLogin

firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)


def validate(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)


class TeacherDetails:
    name = ''
    email = ''
    regdBy = ''
    subjects = {}

    def __init__(self, name, email, regdBy, subjects):
        self.name = name
        self.email = email
        self.regdBy = regdBy
        self.subjects = subjects

    def getDetails(self):
        return {'Name': self.name, 'E-mail': self.email, 'Registered By': self.regdBy, 'subjects': self.subjects}


def register():
    name = bookInfo7.get()
    email = bookInfo4.get()
    password = bookInfo5.get()

    hodDetails = hodLogin.loggedInUser

    if name and email and password and validate(email):
        teacherDetails = TeacherDetails(name, email, hodDetails.name, [])
        loginData = {
            'Email': email,
            'Password': password,
            'Name': name,
            'College': hodDetails.clg,
            'Department': hodDetails.dept

        }

        print(teacherDetails)
        print(loginData)

        # result1 = firebaseDb.post(f'/Teachers Data/{hodDetails.clg}/{hodDetails.dept}/{TeacherDetails.name}',
        # {'Subjects': teacherDetails.subjects})
        result1 = firebaseDb.put(f'/Teacher\'s Data/{hodDetails.clg}/{hodDetails.dept}/{name}', 'Registered By',
                                 teacherDetails.regdBy)
        result2 = firebaseDb.post('/TeacherLogin', loginData)
        if result1 and result2:
            print('Registration Successful.')
            messagebox.showinfo(title = 'Success', message = 'Registration Successful...', parent = registerTeacherRoot)
            registerTeacherRoot.destroy()
            registration()
    else:
        messagebox.showinfo(title = 'Invalid Input', message = 'Please Input all Fields.', parent = registerTeacherRoot)


def registration():
    global registerTeacherRoot, bookInfo4, bookInfo5, bookInfo7
    registerTeacherRoot = Tk()
    registerTeacherRoot.title("Teacher Registration")

    registerTeacherRoot.minsize(width = 700, height = 670)
    registerTeacherRoot.geometry('1000x600+150+10')
    Canvas5 = Canvas(registerTeacherRoot)
    Canvas5.config(bg = "#3498DB")
    Canvas5.pack(expand = True, fill = BOTH)

    # Set Heading Frame
    headingFrame5 = Frame(registerTeacherRoot, bg = "#FFBB00", bd = 5)

    headingFrame5.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)

    headingLabel5 = Label(headingFrame5, text = "Teacher Registration", bg = 'black', fg = 'white',
                          font = ('Courier', 15))
    headingLabel5.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Frame for Login Area
    labelFrame5 = Frame(registerTeacherRoot, bg = 'black')
    labelFrame5.place(relx = 0.040, rely = 0.25, relwidth = 0.92, relheight = 0.3)

    # Name
    lb7 = Label(labelFrame5, text = "Name : ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 1, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo7 = Entry(labelFrame5)
    bookInfo7.place(relx = 0.30, rely = 0.1, relwidth = 0.30, relheight = 0.2)

    # Email
    lb4 = Label(labelFrame5, text = "Email-Id: ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 3, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo4 = Entry(labelFrame5)
    bookInfo4.place(relx = 0.30, rely = 0.4, relwidth = 0.30, relheight = 0.2)
    lbnote = Label(labelFrame5, text = "Eg: someone@domain.com ", bg = 'black', fg = 'yellow', font = ('Courier', 15))
    lbnote.place(relx = 0.65, rely = 0.4)

    # Password
    lb5 = Label(labelFrame5, text = "Password: ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 5, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo5 = Entry(labelFrame5)
    bookInfo5.place(relx = 0.30, rely = 0.7, relwidth = 0.30, relheight = 0.2)

    # Button to REGISTER
    btn7 = Button(registerTeacherRoot, text = "Register", bg = 'black', fg = 'white', font = ('Courier', 15),
                  command = register)
    btn7.place(relx = 0.25, rely = 0.70, relwidth = 0.5, relheight = 0.1)

    registerTeacherRoot.resizable(True, True)
    registerTeacherRoot.state("zoomed")
    registerTeacherRoot.mainloop()


global registerTeacherRoot, bookInfo4, bookInfo5, bookInfo7
if __name__ == '__main__':
    registration()
