import csv
import json
import shutil
from datetime import datetime
from tkinter import Tk, Canvas, BOTH, Button, Frame, Label, StringVar, VERTICAL, HORIZONTAL, NS, EW, messagebox,\
    filedialog
from tkinter.ttk import Combobox, Treeview, Scrollbar

from firebase import firebase

import AttendanceProjectMain
from Attendance import takeAttendance
from studentRegistration import upload_student
import ConnectionManager

connectionManager = ConnectionManager


def logout():
    with open('metadata.json', 'w+') as metadataFile:
        json.dump({}, metadataFile)
        metadataFile.close()
    rootTeacherHome.destroy()
    AttendanceProjectMain.fun()


def regStudent():
    pass


def regStud():
    upload_student(loggedInUser)
    rootTeacherHome.update_idletasks()


def viewAttendance():
    global classCb, subCb, finalData

    def showAttendance():
        global finalData

        startDate, endDate = '', ''

        def downloadAttendance():
            print(finalData)
            fileName = f'Attendance {selClass} {subject} {startDate}--{endDate}.csv'
            with open(fileName, 'w', encoding = 'UTF8', newline = '') as fp:
                writer = csv.writer(fp)
                for dt in finalData:
                    writer.writerow(dt)
                fp.close()

            files = [('All Files', '*.*'),
                     ('Excel Files', '*.csv'),
                     ('Text Document', '*.txt')]

            root.saveLocation = filedialog.asksaveasfile(initialfile = fileName, filetypes = files,
                                                         defaultextension = '*.csv')
            print(root.saveLocation)
            result = shutil.copy(fileName, root.saveLocation.name)
            print(result)
            if result:
                messagebox.showinfo(title = 'Success', message = 'Attendance Saved Successfully.',
                                    parent = root)

        dispData = {}
        dates = []
        selClass = classCb.get()
        year, div = selClass.split(' ')
        subject = subCb.get()
        if connectionManager.isConnected():
            firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
            data = firebaseDb.get(f'Attendance/{loggedInUser.clg}/{loggedInUser.dept}/{year}/{div}/{subject}', None)
            if data:
                studentData = firebaseDb.get(f'Student Details/{loggedInUser.clg}/{loggedInUser.dept}/{year}/{div}'
                                             , None)
                print(studentData)
                for student, value in studentData.items():
                    print(student)
                    dispData[student] = [value['Roll Number']]
                for date in data.keys():
                    dates.append(date)

                dates.sort(key = lambda dat: datetime.strptime(dat, '%a_%H-%M-%S_%d-%m-%y'))

                for date in dates:
                    for student, status in data[date].items():
                        dispData[student].append(status)
                print(dispData)
                tempdispData = dispData
                dispData = []

                for key, value in tempdispData.items():
                    temp = [value[0], key]
                    for i in range(1, len(value)):
                        temp.append(value[i])
                    dispData.append(temp)
                dispData.sort()

                tempdispData = dispData
                dispData = []
                for da in tempdispData:
                    pre = 0
                    total = 0
                    le = len(da)
                    for i in range(2, le):
                        total += 1
                        if da[i] == 'Present':
                            pre += 1
                    da.append(pre)
                    da.append(total)
                    da.append(f'{round(pre / total * 100, 2)} %')
                    dispData.append(da)

                for da in dispData:
                    print(da)

                cols = ['Roll No.', 'Student Name']

                for date in dates:
                    cols.append(date)
                startDate = dates[0].split('_')[2]
                endDate = dates[-1].split('_')[2]

                cols.append('Attendance')
                cols.append('Total')
                cols.append('Percentage')

                finalData = [cols]
                for ds in dispData:
                    finalData.append(ds)

                # Result Frame
                root = Tk()  # Create window
                root.title("Attendance")
                root.resizable(True, True)
                root.state("zoomed")
                root.columnconfigure(0, weight = 1)
                frame = Frame(root, bd = 5, height = 100)
                frame.grid(row = 0, column = 0, columnspan = len(cols) + 1)
                heading = Label(frame, text = 'Attendance ', bg = 'black', fg = 'white', font = ('Courier', 30))
                heading.grid(row = 0, column = 0)
                listBox = Treeview(root, show = "headings",
                                   columns = cols, height = 25)  # The first column of the table is not displayed
                listBox.grid(row = 1, columnspan = 1)
                # set column headings
                for col in cols:
                    listBox.heading(col, text = col)
                listBox.grid(row = 1, column = 0, columnspan = len(cols))
                listBox.column(cols[0], width = 100)
                listBox.column(cols[len(cols) - 1], width = 100)
                listBox.column(cols[len(cols) - 2], width = 100)
                listBox.column(cols[len(cols) - 3], width = 100)

                for index in range(len(dispData)):
                    listBox.insert("", "end", values = (dispData[index]))

                vbar = Scrollbar(root, orient = VERTICAL, command = listBox.yview)
                listBox.configure(yscrollcommand = vbar.set)
                # tree.grid(row=0, column=0, sticky=NSEW)
                vbar.grid(row = 1, column = len(cols), sticky = NS)

                # ----horizontal scrollbar----------
                hbar = Scrollbar(root, orient = HORIZONTAL, command = listBox.xview)
                listBox.configure(xscrollcommand = hbar.set)
                hbar.grid(row = 3, column = 0, sticky = EW)

                frame = Frame(root, bd = 5, height = 100)
                frame.grid(row = 4, column = 0, columnspan = len(cols) + 1)
                button = Button(frame, text = "Download Attendance", bg = 'black', fg = 'white', font = ('Courier', 15),
                                command = downloadAttendance)
                button.grid(row = 0, column = 0)

                root.mainloop()
            else:
                messagebox.showerror(parent = rootSA, title = 'Error',
                                     message = 'No Data Found.\n Please take Attendance First')
        else:
            messagebox.showerror(parent = rootSA, title = 'Error',
                                 message = 'Not connected to Internet. \n Connect to Network First.')

    rootSA = Tk()
    rootSA.title('Take Attendance ')
    rootSA.resizable(True, True)
    rootSA.state("zoomed")
    rootSA.minsize(width = 700, height = 670)
    rootSA.geometry('1000x600+150+10')
    CanvasSA = Canvas(rootSA)
    CanvasSA.config(bg = "#3498DB")
    CanvasSA.pack(expand = True, fill = BOTH)

    # Set Heading Frame
    headingFrame5 = Frame(rootSA, bg = "#FFBB00", bd = 5)

    headingFrame5.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)

    headingLabel5 = Label(headingFrame5, text = "Welcome", bg = 'black', fg = 'white',
                          font = ('Courier', 15))
    headingLabel5.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Class and Subject

    lbcls = Label(rootSA, text = "Class : ", bg = 'black', fg = 'white', font = ('Courier', 18))
    lbcls.place(relx = 0.1, rely = 0.25, relheight = 0.06)

    # Subject Combobox
    def OptionCallBack1(arg = None, arg1 = None, arg2 = None):
        print(variable1.get())
        year1, div1 = variable1.get().split(' ')
        print('in options callback')

    variable2 = StringVar(rootSA)
    variable2.set("Select Subject")
    variable2.trace('w', OptionCallBack1)

    subCb = Combobox(rootSA, textvariable = variable2)
    subCb.pack()
    subCb.place(relx = 0.5, rely = 0.25, relwidth = 0.1, relheight = 0.06)

    # Class Combobox
    def OptionCallBack(arg = None, arg1 = None, arg2 = None):
        print(variable1.get())
        year1, div1 = variable1.get().split(' ')
        print('in options callback')
        subCb.config(values = loggedInUser.subjects[year1][div1])
        variable2.set("Select Subject")

    variable1 = StringVar(rootSA)
    variable1.set("Select Class")
    variable1.trace('w', OptionCallBack)

    subs = loggedInUser.subjects
    clsDict = subs.keys()
    cls = []
    for cl in clsDict:
        abc = subs[cl].keys()
        for divs in abc:
            classes.append(cl + ' ' + divs)
        cls.append(cl)

    classCb = Combobox(rootSA, textvariable = variable1)
    classCb.config(values = classes)
    classCb.pack()
    classCb.place(relx = 0.35, rely = 0.25, relwidth = 0.1, relheight = 0.06)

    use = Label(rootSA, text = "(Note: Use Dropdown Options)", bg = 'black', fg = 'white',
                font = ('Courier', 11))
    use.place(relx = 0.7, rely = 0.25, relheight = 0.06)

    # Button to save student data
    btn7 = Button(rootSA, text = "Show Attendance", bg = 'black', fg = 'white', font = ('Courier', 15),
                  command = showAttendance)
    btn7.place(relx = 0.4, rely = 0.35, relwidth = 0.2, relheight = 0.070)

    rootSA.mainloop()


def takeAtte():
    takeAttendance(loggedInUser)
    rootTeacherHome.update()


def main(argLoggedInUser):
    global rootTeacherHome, classes, loggedInUser, Canvas5
    loggedInUser = argLoggedInUser
    print(loggedInUser)
    rootTeacherHome = Tk()
    rootTeacherHome.title('Welcome to Attendance Management System')
    rootTeacherHome.resizable(True, True)
    rootTeacherHome.state("zoomed")

    rootTeacherHome.minsize(width = 700, height = 670)
    rootTeacherHome.geometry('1000x600+150+10')
    Canvas5 = Canvas(rootTeacherHome)
    Canvas5.config(bg = "#3498DB")
    Canvas5.pack(expand = True, fill = BOTH)

    # Logout Button
    logoutBtn = Button(rootTeacherHome, text = "Logout", font = ('Sylfaen', 15), command = logout)
    logoutBtn.place(relx = 0.9, rely = 0.03, relwidth = 0.07, relheight = 0.04)

    # Set Heading Frame
    headingFrame5 = Frame(rootTeacherHome, bg = "#FFBB00", bd = 5)

    headingFrame5.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)

    headingLabel5 = Label(headingFrame5, text = f"Welcome {loggedInUser.name}", bg = 'black', fg = 'white',
                          font = ('Courier', 15))
    headingLabel5.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    regStudBtn = Button(rootTeacherHome, text = "Register Student", font = ('Sylfaen', 15),
                        command = regStud)
    regStudBtn.place(relx = 0.3, rely = 0.3, relwidth = 0.4, relheight = 0.1)

    takeAttnBtn = Button(rootTeacherHome, text = "Take Attendance", font = ('Sylfaen', 15),
                         command = takeAtte)
    takeAttnBtn.place(relx = 0.3, rely = 0.5, relwidth = 0.4, relheight = 0.1)

    viewAttendancebtn = Button(rootTeacherHome, text = "View Attendance", font = ('Sylfaen', 15),
                               command = viewAttendance)
    viewAttendancebtn.place(relx = 0.3, rely = 0.7, relwidth = 0.4, relheight = 0.1)

    rootTeacherHome.update_idletasks()
    rootTeacherHome.mainloop()


global rootTeacherHome, loggedInUser, Canvas5, subjectName, classCb, subCb, finalData

classes = []
classesList = []
