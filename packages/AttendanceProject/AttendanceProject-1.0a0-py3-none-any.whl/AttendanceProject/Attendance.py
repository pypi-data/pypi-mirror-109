import csv
import json
import shutil
from datetime import datetime
from tkinter import Tk, Canvas, BOTH, Frame, Label, StringVar, Button, filedialog, messagebox
from tkinter.ttk import Treeview, Combobox

from cv2 import cvtColor, COLOR_BGR2RGB, rectangle, putText, FONT_HERSHEY_COMPLEX, imshow, waitKey, resize
from face_recognition import face_encodings, face_locations, compare_faces, face_distance, load_image_file
from firebase import firebase
from numpy import argmin

import ConnectionManager
from HelperClasses import NumpyArrayEncoder
import teacherHome


def showGeneratedAttendance(AttendanceList, presentEncodings):
    def editAttendance():
        editWindow = Tk()
        editWindow.resizable(True, True)
        label1 = Label(editWindow, text="Generated Attendance", font=("Arial", 30)).grid(row=0, columnspan=7)

        rollLabel = Label(editWindow, text="Roll Number", font=("Arial", 15)).grid(row=4, column=1)
        nameLabel = Label(editWindow, text="Name", font=("Arial", 15)).grid(row=4, column=3)
        statusLabel = Label(editWindow, text="Status", font=("Arial", 15)).grid(row=4, column=5)

        # Combobox Callback Methods

        def OptionCallBack1(arg=None, arg1=None, arg2=None):
            print(f'In Callback 1 : {arg, arg1, arg2}')
            roll = variable1.get()
            name = ''
            status = ''
            for rns in temp_roll_name_atte:
                if rns[0] == int(roll):
                    name, status = rns[1], rns[2]
            print(roll, name, status)
            # variable1.set(roll)
            # variable2.set(name)
            # variable3.set(status)
            rollCb.set(roll)
            nameCb.set(name)
            statusCb.set(status)

        def OptionCallBack2(arg=None, arg1=None, arg2=None):
            print(f'In Callback 2 : {arg, arg1, arg2}')
            name = variable2.get()
            roll = 0
            status = ''
            for rns in temp_roll_name_atte:
                if rns[1] == name:
                    roll, status = rns[0], rns[2]
            print(roll, name, status)
            # variable2.set(name)
            # variable1.set(roll)
            # variable3.set(status)
            rollCb.set(roll)
            nameCb.set(name)
            statusCb.set(status)

        def OptionCallBack3(arg=None, arg1=None, arg2=None):
            print(f'In Callback 3 : {arg, arg1, arg2}')
            status = statusCb.get()
            roll = rollCb.get()
            for ind in range(len(temp_roll_name_atte)):
                if temp_roll_name_atte[ind][0] == int(roll):
                    temp_roll_name_atte[ind][2] = status
                editWindow.update_idletasks()
            print(temp_roll_name_atte)
            editWindow.mainloop()

        def confirmAttendance():
            global roll_name_atte
            roll_name_atte = temp_roll_name_atte
            editWindow.destroy()
            update()
            root.update_idletasks()
            root.mainloop()

        # rollLabel Combobox

        variable1 = StringVar(editWindow)
        variable1.set("select")
        # variable1.trace('w', OptionCallBack1)

        rollCb = Combobox(editWindow, textvariable=variable1)

        rollCb.grid(row=7, column=1)
        rollCb.config(values=[rns[0] for rns in temp_roll_name_atte])
        rollCb.bind("<<ComboboxSelected>>", OptionCallBack1)

        # NameLabel Combobox

        variable2 = StringVar(editWindow)
        variable2.set("Select")
        # variable2.trace('w', OptionCallBack2)

        nameCb = Combobox(editWindow, textvariable=variable2)

        nameCb.grid(row=7, column=3)
        nameCb.config(values=[rns[1] for rns in temp_roll_name_atte])
        nameCb.bind("<<ComboboxSelected>>", OptionCallBack2)

        # StatusLabel Combobox

        variable3 = StringVar(editWindow)
        variable3.set("Select")
        # variable3.trace('w', OptionCallBack3)

        statusCb = Combobox(editWindow, textvariable=variable3)

        statusCb.grid(row=7, column=5)
        statusCb.config(values=['Present', 'Absent'])
        statusCb.bind("<<ComboboxSelected>>", OptionCallBack3)

        confirm = Button(editWindow, text="Confirm", width=15,
                         command=confirmAttendance).grid(row=10, column=3)

        Label(editWindow, text='', width=10).grid(row=7, column=0)
        Label(editWindow, text='', width=10).grid(row=7, column=2)
        Label(editWindow, text='', width=10).grid(row=7, column=4)
        Label(editWindow, text='', width=10).grid(row=7, column=6)

        Label(editWindow, text='', height=4).grid(row=2, column=0)

        Label(editWindow, text='', height=2).grid(row=6, column=0)

        Label(editWindow, text='', height=2).grid(row=9, column=0)

        Label(editWindow, text='', height=2).grid(row=11, column=0)

        editWindow.mainloop()

    def save_attendance():
        def downloadAttendance():
            finalData = [['Roll No.', 'Name', 'Attendance']]
            for r, n, s in roll_name_atte:
                finalData.append([r, n, s])
            print(finalData)
            date = now.strftime('%d-%m-%y')
            fileName = f'Attendance {year} {div} {subject} {date}.csv'
            with open(fileName, 'w', encoding='UTF8', newline='') as fp:
                writer = csv.writer(fp)
                for dt in finalData:
                    writer.writerow(dt)
                fp.close()

            files = [('All Files', '*.*'),
                     ('Excel Files', '*.csv'),
                     ('Text Document', '*.txt')]

            rootTA.saveLocation = filedialog.asksaveasfile(initialfile=fileName, filetypes=files,
                                                           defaultextension='*.csv')
            print(rootTA.saveLocation)
            result1 = shutil.copy(fileName, rootTA.saveLocation.name)
            if result:
                messagebox.showinfo(title='Success', message='Attendance Saved Successfully.',
                                    parent=root)

        attendance = {}
        for rns in roll_name_atte:
            attendance[rns[1]] = rns[2]
        presEnc = {}
        for stud_enc in presentEncodings.keys():
            if attendance[stud_enc] == 'Present':
                presEnc[stud_enc] = presentEncodings[stud_enc]

        now = datetime.now()
        dtString = now.strftime('%a_%H-%M-%S_%d-%m-%y')
        firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
        result = firebaseDb.put(f'Attendance/{loggedInUser.clg}/{loggedInUser.dept}/{year}/{div}/{subject}', dtString,
                                attendance)
        result2 = firebaseDb.put(f'Attendance-Encodings/{loggedInUser.clg}/{loggedInUser.dept}/{year}/{div}/{subject}',
                                 dtString, presEnc)
        if result:
            downloadAttendance()
            root.destroy()
            rootTA.destroy()
            teacherHome.rootTeacherHome.mainloop()
        else:
            messagebox.showerror(title='Failed', message='Attendance Failed to save .',
                                 parent=root)
            return

    temp_roll_name_atte = []

    for i in range(len(list(set(studentsNameList)))):
        temp_roll_name_atte.append([studentsData[studentsNameList[i]]['Roll Number'], studentsNameList[i],
                                    AttendanceList[studentsNameList[i]]])
    print(temp_roll_name_atte)

    roll_name_atte = temp_roll_name_atte

    def show():

        roll_name_atte.sort()

        for index in range(len(temp_roll_name_atte)):
            listBox.insert("", "end", values=(roll_name_atte[index]))

    def update():
        for item in listBox.get_children():
            listBox.delete(item)
        roll_name_atte.sort()

        for index in range(len(temp_roll_name_atte)):
            listBox.insert("", "end", values=(roll_name_atte[index]))

    root = Tk()
    root.title("Attendance")
    root.resizable(True, True)
    root.geometry('500x500+150+10')
    root.minsize(width=500, height=500)
    root.columnconfigure(0, weight=1)
    label = Label(root, text="Generated Attendance", font=("Arial", 30)).grid(row=0, columnspan=3)
    # create Treeview with 3 columns
    cols = ('Roll No.', 'Name', 'Status')
    listBox = Treeview(root, columns=cols, show='headings', height=15)

    # set column headings
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.column(cols[0], width=100)
    listBox.column(cols[2], width=100)
    frame = Frame(root, bg="#FFBB00", bd=5)
    frame.grid(row=4, columnspan=3)

    showScores = Button(frame, text="Save Attendance", width=15,
                        command=save_attendance)
    showScores.grid(row=0, column=1)
    closeButton = Button(frame, text="Edit List", width=15,
                         command=editAttendance)
    closeButton.grid(row=0, column=0)

    show()

    root.mainloop()


def sveAttendance(preStuds, presentEncodings):
    AttendanceList = {}
    now = datetime.now()
    dtString = now.strftime('%a_%H-%M-%S_%d-%m-%y')
    date = now.strftime('%d/%m/%y')
    for name in list(set(studentsNameList)):
        if name in preStuds:
            AttendanceList[name] = 'Present'
        else:
            AttendanceList[name] = 'Absent'

    print(AttendanceList)

    showGeneratedAttendance(AttendanceList, presentEncodings)


def generateAttendance():
    threshold = 0.48
    originalImg = uploadedImage
    presentEncodings = {}

    imgS = cvtColor(originalImg, COLOR_BGR2RGB)
    facesCurFrame = face_locations(imgS)
    encodesCurrFrame = face_encodings(imgS, facesCurFrame)
    prestuds = []

    for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurFrame):
        rootTA.update()
        matches = compare_faces(studentsEncodingList, encodeFace, threshold)
        faceDis = face_distance(studentsEncodingList, encodeFace)
        print(f'Matches : {matches}')
        print(f'FaceDis : {faceDis}')

        if len(faceDis):
            matchIndex = argmin(faceDis)

            if matches[matchIndex]:
                student = studentsNameList[int(matchIndex)]
                print(student)
                presentEncodings[student] = json.dumps(encodeFace, cls=NumpyArrayEncoder)
                prestuds.append(student)

                y1, x2, y2, x1 = faceLoc
                rectangle(uploadedImage, (x1, y1), (x2, y2), (0, 255, 0), 1)
                putText(uploadedImage, student, (x1 + 6, y1 - 10), FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        rootTA.update()
    print(presentEncodings)

    shape = uploadedImage.shape

    imgToShow = uploadedImage

    if shape[0] > 480 or shape[1] > 640:
        imgToShow = resize(imgToShow, (640, 480))

    print(prestuds)
    imshow("output with names", imgToShow)  # Show image
    waitKey(0)
    sveAttendance(prestuds, presentEncodings)


def open_img():
    global uploadedImage
    rootTA.filename = filedialog.askopenfile(initialdir=":", title="Select a File", filetypes=(
        ("Jpg files", "*.jpg"), ("Jpeg files", "*.jpeg"), ("Png files", "*.png"), ("All Files", "*.*")), parent=rootTA)
    rootTA.update()
    uploadedImage = rootTA.filename
    uploadedImage = open(uploadedImage.name, encoding="utf8")
    print(uploadedImage)
    print(uploadedImage.name)
    uploadedImage = load_image_file(uploadedImage.name)

    rootTA.update()

    if len(uploadedImage):
        messagebox.showinfo(title='Success', message='Image Uploaded Successfully.', parent=rootTA)
    else:
        messagebox.showinfo(parent=rootTA, title='Error',
                            message='Some Error Occurred. Please Try Again ')
    rootTA.update()


def getStudents():
    global studentsData, studentsEncodingList, studentsNameList
    studentsEncodingList = []
    studentsNameList = []

    if ConnectionManager.isConnected():
        firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
        data = firebaseDb.get(f'Student Details/{loggedInUser.clg}/{loggedInUser.dept}/{year}/{div}', None)
        if data:
            studentsData = data
            for key in data.keys():
                studentsEncodingList.append(json.loads(data[key]['Encodings']))
                studentsNameList.append(key)
                rootTA.update()
        data2 = firebaseDb.get(f'Attendance-Encodings/{loggedInUser.clg}/{loggedInUser.dept}/{year}/{div}/{subject}',
                               None)

        if data2:
            dates = []
            for date in data2.keys():
                dates.append(date)
            dates.sort(key=lambda dat: datetime.strptime(dat, '%a_%H-%M-%S_%d-%m-%y'))
            lastDates = []
            if len(dates) >= 2:
                lastDates = dates[-2:]
            elif len(dates):
                lastDates = dates
            if lastDates:
                for date in lastDates:
                    for key, value in data2[date].items():
                        studentsEncodingList.append(json.loads(value))
                        studentsNameList.append(key)
                        rootTA.update()

        rootTA.update_idletasks()
        for name, enc in zip(studentsNameList, studentsEncodingList):
            print(name, enc)
            rootTA.update()
        generateAttendance()
    else:
        messagebox.showerror(title='Error', message='Network Connection Not Found please connect to Internet\n '
                                                    'and try Again', parent=rootTA)
        return


def check():
    global year, div, subject
    stud_class = classCb.get()
    subject = subCb.get()

    if not ConnectionManager.isConnected():
        messagebox.showerror(title='Error',
                             message='Internet Connection Not Found. Please connect to a network first.',
                             parent=rootTA)
        return

    if (not stud_class) or (stud_class not in classes):
        messagebox.showinfo(title='Error', message='Please select class from list', parent=rootTA)
        return

    if not len(uploadedImage):
        messagebox.showerror(title='Error', message='Image Not Found. Please upload Another Image', parent=rootTA)
        return

    year, div = stud_class.split(' ')
    getStudents()
    rootTA.update_idletasks()


def takeAttendance(args):
    global loggedInUser, rootTA, classes, classCb, subCb
    loggedInUser = args
    rootTA = Tk()
    rootTA.title('Take Attendance ')
    rootTA.resizable(True, True)
    rootTA.state("zoomed")
    rootTA.minsize(width=700, height=670)
    rootTA.geometry('1000x600+150+10')
    Canvas5 = Canvas(rootTA)
    Canvas5.config(bg="#3498DB")
    Canvas5.pack(expand=True, fill=BOTH)

    # Set Heading Frame
    headingFrame5 = Frame(rootTA, bg="#FFBB00", bd=5)

    headingFrame5.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

    headingLabel5 = Label(headingFrame5, text="Welcome", bg='black', fg='white',
                          font=('Courier', 15))
    headingLabel5.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Class and Subject

    lbcls = Label(rootTA, text="Class : ", bg='black', fg='white', font=('Courier', 18))
    lbcls.place(relx=0.1, rely=0.25, relheight=0.06)

    # Subject Combobox
    def OptionCallBack1(arg=None, arg1=None, arg2=None):
        print(variable1.get())
        year1, div1 = variable1.get().split(' ')
        print('in options callback')

    variable2 = StringVar(rootTA)
    variable2.set("Select Subject")
    variable2.trace('w', OptionCallBack1)

    subCb = Combobox(rootTA, textvariable=variable2)
    subCb.pack()
    subCb.place(relx=0.5, rely=0.25, relwidth=0.1, relheight=0.06)

    # Class Combobox
    def OptionCallBack(arg=None, arg1=None, arg2=None):
        print(variable1.get())
        year1, div1 = variable1.get().split(' ')
        print('in options callback')
        subCb.config(values=loggedInUser.subjects[year1][div1])
        variable2.set("Select Subject")

    variable1 = StringVar(rootTA)
    variable1.set("Select Class")
    variable1.trace('w', OptionCallBack)

    subs = loggedInUser.subjects
    clsDict = subs.keys()
    cls = []
    classes = []
    for cl in clsDict:
        abc = subs[cl].keys()
        for divs in abc:
            classes.append(cl + ' ' + divs)
        cls.append(cl)

    classCb = Combobox(rootTA, textvariable=variable1)
    classCb.config(values=classes)
    classCb.pack()
    classCb.place(relx=0.35, rely=0.25, relwidth=0.1, relheight=0.06)

    use = Label(rootTA, text="(Note: Use Dropdown Options)", bg='black', fg='white',
                font=('Courier', 11))
    use.place(relx=0.7, rely=0.25, relheight=0.06)

    # Upload Image
    lb5 = Label(rootTA, text="Upload Image: ", bg='black', fg='white', font=('Courier', 18))
    lb5.place(relx=0.1, rely=0.37, relheight=0.06)

    # Button to upload student image
    std_image = Button(rootTA, text="Upload", bg='white', fg='black', font=('Courier', 12),
                       command=open_img)
    std_image.place(relx=0.35, rely=0.37, relwidth=0.18, relheight=0.06)

    # Button to save student data
    btn7 = Button(rootTA, text="Generate Attendance", bg='black', fg='white', font=('Courier', 15),
                  command=check)
    btn7.place(relx=0.4, rely=0.48, relwidth=0.2, relheight=0.070)

    rootTA.mainloop()


global loggedInUser, rootTA, uploadedImage, classes, studentsData, studentsEncodingList, studentsNameList, year, div
global classCb, subCb, subject, roll_name_atte
