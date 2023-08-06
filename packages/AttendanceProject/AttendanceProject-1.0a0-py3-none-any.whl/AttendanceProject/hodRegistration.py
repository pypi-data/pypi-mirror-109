from tkinter import *
from tkinter import messagebox, ttk

from firebase import firebase
import re

import DataClasses
import hodLogin

firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)


def login():
    registerHodRoot.destroy()
    hodLogin.loginScreen()


def generateClasses():
    global hodDetails, loginData
    eng = ['FE', 'SE', 'TE', 'BE']
    others = ['FY', 'SY', 'TY', 'LY']
    secs = ['A', 'B', 'C', 'D']

    print('stream', 'years', 'divs')
    print(streams.get(), years.get(), divs.get())
    stream = streams.get()
    year = int(years.get())
    div = int(divs.get())
    print(stream, year, div)

    classes = {}
    if stream == 'Engineering':
        for i in range(int(year)):
            tempDivs = []
            for j in range(int(div)):
                tempDivs.append(secs[j])
            classes[eng[i]] = tempDivs
    else:
        for i in range(int(year)):
            tempDivs = []
            for j in range(int(div)):
                tempDivs.append(secs[j])
            classes[others[i]] = tempDivs

    hodDetails = DataClasses.HodDetails(hodDetails.name, hodDetails.dept, hodDetails.email, hodDetails.clg, classes)
    loginData['Classes'] = classes

    result1 = firebaseDb.put(f'/Hod\'s Data/{hodDetails.clg}/{hodDetails.dept}/{hodDetails.name}', 'Details',
                             {'E-mail': hodDetails.email, 'Classes': classes})
    result2 = firebaseDb.post('/HodLogin', loginData)
    if result1 and result2:
        print('Registration Successful.')
        messagebox.showinfo(title = 'Success', message = 'Registration Successful...')
        getClassesInfoRoot.destroy()
        hodLogin.loginScreen()
    else:
        messagebox.showinfo(title = 'Invalid Input', message = 'Please Input all Fields.')

    print(classes)


def getClassesInfo():
    global streams, divs, years, lvar, m, n, getClassesInfoRoot
    # registerHodRoot.destroy()
    getClassesInfoRoot = Tk()
    getClassesInfoRoot.minsize(width = 700, height = 670)
    getClassesInfoRoot.geometry('1000x600+150+10')
    CanvasClasses = Canvas(getClassesInfoRoot)
    CanvasClasses.config(bg = "#3498D0")
    CanvasClasses.pack(expand = True, fill = BOTH)
    getClassesInfoRoot.resizable(True, True)
    getClassesInfoRoot.state("zoomed")

    # Set Heading Frame
    headingFrame = Frame(getClassesInfoRoot, bg = "#FFBB00", bd = 5)

    headingFrame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)

    headingLabel = Label(headingFrame, text = "Classes Info", bg = 'black', fg = 'white',
                         font = ('Courier', 15))
    headingLabel.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Stream Info Start

    streamLabel = Label(getClassesInfoRoot, text = "Select Stream", fg = 'black', bg = '#3498DF',
                        font = ('Courier', 15))
    streamLabel.place(relx = 0.1, rely = 0.3, relwidth = 0.25, relheight = 0.05)

    # Combobox creation
    lvar = StringVar(getClassesInfoRoot)

    streams = ttk.Combobox(getClassesInfoRoot, width = 20, values = ('Engineering', 'Others'), textvariable = lvar)
    streams.pack()
    streams.place(relx = 0.4, rely = 0.3, relwidth = 0.2, relheight = 0.05)

    use = Label(getClassesInfoRoot, text = "(Note: Use Dropdown Options)", bg = 'black', fg = 'white',
                font = ('Courier', 11))
    use.place(relx = 0.7, rely = 0.3, relheight = 0.05)
    # Stream Info End

    # Years Info Start

    yearsLabel = Label(getClassesInfoRoot, text = "Select Number of Years", fg = 'black', bg = '#3498DF',
                       font = ('Courier', 15))
    yearsLabel.place(relx = 0.1, rely = 0.5, relwidth = 0.25, relheight = 0.05)

    # Department
    # Combobox creation
    m = StringVar(getClassesInfoRoot)
    years = ttk.Combobox(getClassesInfoRoot, width = 20, textvariable = m)

    # Department Options Data
    years['values'] = ('1', '2', '3', '4')
    years.pack()

    years.place(relx = 0.4, rely = 0.5, relwidth = 0.2, relheight = 0.05)

    use = Label(getClassesInfoRoot, text = "(Note: Use Dropdown Options)", bg = 'black', fg = 'white',
                font = ('Courier', 11))
    use.place(relx = 0.7, rely = 0.5, relheight = 0.05)
    # Years Info End

    # cbFEVar = IntVar()
    # cbSEVar = IntVar()
    # cbTEVar = IntVar()
    # cbBEVar = IntVar()
    # cbFE = Checkbutton(getClassesInfoRoot, text = 'FE', variable = cbFEVar, onvalue = 1, offvalue = 0, command = '')
    # cbFE.pack()
    # cbFE.place(relx = 0.4, rely = 0.51)
    # cbSE = Checkbutton(getClassesInfoRoot, text = 'SE', variable = cbSEVar, onvalue = 1, offvalue = 0, command = '')
    # cbSE.pack()
    # cbSE.place(relx = 0.45, rely = 0.51)
    # cbTE = Checkbutton(getClassesInfoRoot, text = 'TE', variable = cbTEVar, onvalue = 1, offvalue = 0, command = '')
    # cbTE.pack()
    # cbTE.place(relx = 0.5, rely = 0.51)
    # cbBE = Checkbutton(getClassesInfoRoot, text = 'BE', variable = cbBEVar, onvalue = 1, offvalue = 0, command = '')
    # cbBE.pack()
    # cbBE.place(relx = 0.55, rely = 0.51)

    # Divs Info Start

    divsLabel = Label(getClassesInfoRoot, text = "Select Number of Divisions", fg = 'black', bg = '#3498DF',
                      font = ('Courier', 15))
    divsLabel.place(relx = 0.1, rely = 0.7, relwidth = 0.25, relheight = 0.05)

    # Combobox creation
    n = StringVar(getClassesInfoRoot)
    divs = ttk.Combobox(getClassesInfoRoot, width = 20, textvariable = n)

    # Department Options Data
    divs['values'] = ('1', '2', '3', '4')

    divs.pack()
    divs.place(relx = 0.4, rely = 0.7, relwidth = 0.2, relheight = 0.05)

    use = Label(getClassesInfoRoot, text = "(Note: Use Dropdown Options)", bg = 'black', fg = 'white',
                font = ('Courier', 11))
    use.place(relx = 0.7, rely = 0.7, relheight = 0.05)

    # Div Info End

    # Submit Button
    btn = Button(getClassesInfoRoot, text = 'Submit', bg = 'black', fg = 'white', font = ('Courier', 15),
                 command = generateClasses)
    btn.place(relx = 0.4, rely = 0.85, relwidth = 0.2, relheight = 0.05)

    getClassesInfoRoot.bind('<Return>', generateClasses)

    getClassesInfoRoot.mainloop()


def validate(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)


def register():
    global hodDetails, loginData
    name = bookInfo7.get()
    dept = bookInfo6.get()
    email = bookInfo4.get()
    password = bookInfo5.get()
    clg = bookInfoClg.get()
    hodDetails = None
    loginData = None

    if name and dept and email and password and clg and validate(email):
        hodDetails = DataClasses.HodDetails(name, dept, email, clg)
        loginData = {
            'Email': email,
            'Password': password,
            'Name': name,
            'College': clg,
            'Department': dept

        }

        registerHodRoot.destroy()
        getClassesInfo()

    else:
        messagebox.showinfo(title = 'Invalid Input', message = 'Please Input all Fields.')


def registration():
    global registerHodRoot, bookInfo3, bookInfo4, bookInfo5, bookInfo6, bookInfo7, bookInfoClg

    registerHodRoot = Tk()
    registerHodRoot.title("Teacher Registration")

    registerHodRoot.minsize(width = 700, height = 670)
    registerHodRoot.geometry('1000x600+150+10')
    Canvas5 = Canvas(registerHodRoot)
    Canvas5.config(bg = "#3498DB")
    Canvas5.pack(expand = True, fill = BOTH)

    # Set Heading Frame
    headingFrame5 = Frame(registerHodRoot, bg = "#FFBB00", bd = 5)

    headingFrame5.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)

    headingLabel5 = Label(headingFrame5, text = "Teacher Registration", bg = 'black', fg = 'white',
                          font = ('Courier', 15))
    headingLabel5.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Frame for Login Area
    labelFrame5 = Frame(registerHodRoot, bg = 'black')
    labelFrame5.place(relx = 0.040, rely = 0.25, relwidth = 0.92, relheight = 0.5)

    # Name
    lb7 = Label(labelFrame5, text = "Name : ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 1, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo7 = Entry(labelFrame5)
    bookInfo7.place(relx = 0.30, rely = 0.07, relwidth = 0.30, relheight = 0.09)

    # College
    lbclg = Label(labelFrame5, text = "College : ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 2, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfoClg = Entry(labelFrame5)
    bookInfoClg.place(relx = 0.30, rely = 0.25, relwidth = 0.30, relheight = 0.09)

    # Branch
    lb6 = Label(labelFrame5, text = "Department: ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 3, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo6 = Entry(labelFrame5)
    bookInfo6.place(relx = 0.30, rely = 0.42, relwidth = 0.30, relheight = 0.09)

    # Email
    lb4 = Label(labelFrame5, text = "Email-Id: ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 4, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo4 = Entry(labelFrame5)
    bookInfo4.place(relx = 0.30, rely = 0.59, relwidth = 0.30, relheight = 0.09)
    lbnote = Label(labelFrame5, text = "Eg: someone@domain.com ", bg = 'black', fg = 'yellow', font = ('Courier', 15))
    lbnote.place(relx = 0.65, rely = 0.59)

    # Password
    lb5 = Label(labelFrame5, text = "Password: ", bg = 'black', fg = 'white', font = ('Courier', 18))\
        .grid(row = 5, column = 0, sticky = E, padx = (10, 0), pady = (30, 0))
    bookInfo5 = Entry(labelFrame5)
    bookInfo5.place(relx = 0.30, rely = 0.77, relwidth = 0.30, relheight = 0.09)


    # Button to REGISTER
    btn7 = Button(registerHodRoot, text = "Register", bg = 'black', fg = 'white', font = ('Courier', 15),
                  command = register)
    btn7.place(relx = 0.25, rely = 0.80, relwidth = 0.5, relheight = 0.1)

    btn8 = Button(registerHodRoot, text = "Back To Login", bg = 'black', fg = 'white', font = ('Courier', 15),
                  command = login)
    btn8.place(relx = 0.35, rely = 0.94, relwidth = 0.3, relheight = 0.04)

    registerHodRoot.resizable(True, True)
    registerHodRoot.state("zoomed")
    registerHodRoot.mainloop()


global registerHodRoot, bookInfo3, bookInfo4, bookInfo5, bookInfo6, bookInfo7, bookInfoClg
global hodDetails, streams, divs, years, lvar, m, n, loginData, getClassesInfoRoot

if __name__ == '__main__':
    getClassesInfo()
