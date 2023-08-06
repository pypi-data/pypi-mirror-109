import csv
import json
import shutil
from tkinter import Tk, Canvas, BOTH, Frame, Label, Button, StringVar, ttk, messagebox, filedialog, Scrollbar, VERTICAL, \
    NS, HORIZONTAL, EW
from tkinter.ttk import Treeview, Combobox

from firebase import firebase

import hodLogin as hodLogin
import teacherRegistration as teacherRegistration
import AttendanceProjectMain
import ConnectionManager

connectionManager = ConnectionManager


class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder

        self.field_style = kwargs.pop("style", "TEntry")
        self.placeholder_style = kwargs.pop("placeholder_style", self.field_style)
        self["style"] = self.placeholder_style

        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, e):
        if self["style"] == self.placeholder_style:
            self.delete("0", "end")
            self["style"] = self.field_style

    def _add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = self.placeholder_style


def registerTeacher():
    if connectionManager.isConnected():
        teacherRegistration.registration()
    else:
        messagebox.showwarning("Network Error", "Please check your Internet Connection")
        return


def logout():
    with open('metadata.json', 'w+') as metadataFile:
        json.dump({}, metadataFile)
        metadataFile.close()
    rootHodHome.destroy()
    AttendanceProjectMain.fun()


def assignClasses():
    global rootAssignClasses
    print(f'Selected Entries : {classcb.get()},{teachercb.get()},{subjectName.get()}')
    selectedClass = classcb.get()
    selectedTeacher = teachercb.get()
    selectedSubject = subjectName.get()

    if (selectedTeacher not in teachersOptions) or (selectedClass not in classOptions):
        messagebox.showwarning("Invalid Option", "Please select options from list.")
        return
    if selectedSubject == '':
        messagebox.showwarning("Empty Subject", "Please Enter Subject.")
        return

    if not ConnectionManager.isConnected():
        messagebox.showwarning("Network Error", "Please check your Internet Connection")
        return

    selClass, div = selectedClass.split('_')

    firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
    appointedClasses = firebaseDb.get(
        f'/Teacher\'s Data/{loggedInUser.clg}/{loggedInUser.dept}/{selectedTeacher}/Subjects', '')

    subs = [selectedSubject]
    classesToBeAppointed = {selectedClass: selectedSubject}
    print(appointedClasses)
    if appointedClasses:
        if selClass in appointedClasses.keys():
            if div in appointedClasses[selClass].keys():
                sub = appointedClasses[selClass][div]
                if sub:
                    for su in sub:
                        subs.append(su)

    print(classesToBeAppointed)
    result1 = firebaseDb.put(
        f'/Teacher\'s Data/{loggedInUser.clg}/{loggedInUser.dept}/{selectedTeacher}/Subjects/{selClass}',
        div,
        subs)

    keys = firebaseDb.get('/TeacherLogin', None)
    print(keys)
    result2 = False
    for key, data in keys.items():
        if data['College'] == loggedInUser.clg and data['Department'] == loggedInUser.dept and \
                data['Name'] == selectedTeacher:
            result2 = firebaseDb.put(f'/TeacherLogin/{key}/Subjects/{selClass}', div, subs)

    result3 = firebaseDb.put(f'/Subjects_Teachers/{loggedInUser.clg}/{loggedInUser.dept}/{selClass}/{div}',
                             selectedSubject,
                             selectedTeacher)

    if result1 and result2 and result3:
        ret = messagebox.showinfo("Success", "Class Assigned Successfully.", parent=rootAssignClasses)
        rootAssignClasses.destroy()

    else:
        messagebox.showerror("Error", "Some Error Occurred Please try Again")


def funAssignClasses():
    global classcb, teachercb, subjectName, classOptions, teachersOptions, rootAssignClasses
    rootAssignClasses = Tk()
    rootAssignClasses.title(f'Assign Classes to Teachers')
    rootAssignClasses.resizable(True, True)
    rootAssignClasses.state("zoomed")

    rootAssignClasses.minsize(width=700, height=670)
    rootAssignClasses.geometry('1000x600+150+10')

    CanvasAssignClasses = Canvas(rootAssignClasses)
    CanvasAssignClasses.config(bg="#3498DB")
    CanvasAssignClasses.pack(expand=True, fill=BOTH)

    # Set Heading Frame
    headingFrame = Frame(CanvasAssignClasses, bg="#FFBB00", bd=5)

    headingFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

    headingLabel = Label(headingFrame, text=f"Welcome ", bg='black', fg='white',
                         font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Combobox Creation 1
    def OptionCallBack():
        print(variable1.get())

    variable1 = StringVar(rootAssignClasses)
    variable1.set("Select Class From List")
    variable1.trace('w', OptionCallBack)

    classOptions = []
    for item in classesList:
        classOptions.append(item)

    classcb = ttk.Combobox(rootAssignClasses, width=20, textvariable=variable1)

    # Department Options Data
    classcb.config(values=classOptions)
    classcb.pack()
    classcb.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.05)

    # Combobox Creation 2

    def OptionCallBack():
        print(variable2.get())

    variable2 = StringVar(rootAssignClasses)
    variable2.set("Select Teacher From List")
    variable2.trace('w', OptionCallBack)

    if connectionManager.isConnected():
        firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
        result1 = firebaseDb.get(f'/Teacher\'s Data/{loggedInUser.clg}/{loggedInUser.dept}/', '')
        print(f'result : {result1}')
        if result1:
            print(result1.keys())
    else:
        messagebox.showerror("Network Error", "Please check your Internet Connection")
        rootAssignClasses.destroy()
        rootHodHome.update_idletasks()
        return

    teachersOptions = []
    for item in result1.keys():
        teachersOptions.append(item)

    teachercb = ttk.Combobox(rootAssignClasses, width=20, textvariable=variable2)

    # Department Options Data
    teachercb.config(values=teachersOptions)
    teachercb.pack()
    teachercb.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.05)

    # Entry Box to enter Teacher's Name
    subjectName = PlaceholderEntry(rootAssignClasses, "Enter Subject Name", style="TEntry")
    subjectName.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.05)

    # Submit Button
    submitBtn = Button(rootAssignClasses, text="Submit", font=('Sylfaen', 15), command=assignClasses)
    submitBtn.place(relx=0.45, rely=0.4, relwidth=0.1, relheight=0.05)

    rootAssignClasses.mainloop()


def viewAttendance():
    def showAttendance():

        startDate, endDate = '', ''

        def downloadAttendance():
            print(finalData)
            fileName = f'Attendance {selClass} {subject} {startDate}--{endDate}.csv'
            with open(fileName, 'w', encoding='UTF8', newline='') as fp:
                writer = csv.writer(fp)
                for dt in finalData:
                    writer.writerow(dt)
                fp.close()

            files = [('All Files', '*.*'),
                     ('Excel Files', '*.csv'),
                     ('Text Document', '*.txt')]

            root.saveLocation = filedialog.asksaveasfile(initialfile=fileName, filetypes=files,
                                                         defaultextension='*.csv')
            print(root.saveLocation)
            result = shutil.copy(fileName, root.saveLocation.name)
            print(result)
            if result:
                messagebox.showinfo(title='Success', message='Attendance Saved Successfully.',
                                    parent=root)

        dispData = {}
        dates = []
        selClass = classCb.get()
        year, div = selClass.split('_')
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
                root.columnconfigure(0, weight=1)
                frame = Frame(root, bd=5, height=100)
                frame.grid(row=0, column=0, columnspan=len(cols) + 1)
                heading = Label(frame, text='Attendance ', bg='black', fg='white', font=('Courier', 30))
                heading.grid(row=0, column=0)
                listBox = Treeview(root, show="headings",
                                   columns=cols, height=25)  # The first column of the table is not displayed
                listBox.grid(row=1, columnspan=1)
                # set column headings
                for col in cols:
                    listBox.heading(col, text=col)
                listBox.grid(row=1, column=0, columnspan=len(cols))
                listBox.column(cols[0], width=100)
                listBox.column(cols[len(cols) - 1], width=100)
                listBox.column(cols[len(cols) - 2], width=100)
                listBox.column(cols[len(cols) - 3], width=100)

                for index in range(len(dispData)):
                    listBox.insert("", "end", values=(dispData[index]))

                vbar = Scrollbar(root, orient=VERTICAL, command=listBox.yview)
                listBox.configure(yscrollcommand=vbar.set)
                # tree.grid(row=0, column=0, sticky=NSEW)
                vbar.grid(row=1, column=len(cols), sticky=NS)

                # ----horizontal scrollbar----------
                hbar = Scrollbar(root, orient=HORIZONTAL, command=listBox.xview)
                listBox.configure(xscrollcommand=hbar.set)
                hbar.grid(row=3, column=0, sticky=EW)

                frame = Frame(root, bd=5, height=100)
                frame.grid(row=4, column=0, columnspan=len(cols) + 1)
                button = Button(frame, text="Download Attendance", bg='black', fg='white', font=('Courier', 15),
                                command=downloadAttendance)
                button.grid(row=0, column=0)

                root.mainloop()
            else:
                messagebox.showerror(parent=rootSA, title='Error',
                                     message='No Data Found.\n Please take Attendance First')
        else:
            messagebox.showerror(parent=rootSA, title='Error',
                                 message='Not connected to Internet. \n Connect to Network First.')

    rootSA = Tk()
    rootSA.title('Attendance ')
    rootSA.resizable(True, True)
    rootSA.state("zoomed")
    rootSA.minsize(width=700, height=670)
    rootSA.geometry('1000x600+150+10')
    CanvasSA = Canvas(rootSA)
    CanvasSA.config(bg="#3498DB")
    CanvasSA.pack(expand=True, fill=BOTH)

    # Set Heading Frame
    headingFrame5 = Frame(rootSA, bg="#FFBB00", bd=5)

    headingFrame5.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

    headingLabel5 = Label(headingFrame5, text="Welcome", bg='black', fg='white',
                          font=('Courier', 15))
    headingLabel5.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Class and Subject

    lbcls = Label(rootSA, text="Class : ", bg='black', fg='white', font=('Courier', 18))
    lbcls.place(relx=0.1, rely=0.25, relheight=0.06)

    # Subject Combobox
    def OptionCallBack1(arg=None, arg1=None, arg2=None):
        pass

    variable2 = StringVar(rootSA)
    variable2.set("Select Subject")
    variable2.trace('w', OptionCallBack1)

    subCb = Combobox(rootSA, textvariable=variable2)
    subCb.pack()
    subCb.place(relx=0.5, rely=0.25, relwidth=0.1, relheight=0.06)

    firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
    print(firebaseDb)
    subjects = firebaseDb.get(f'Subjects_Teachers/{loggedInUser.clg}/{loggedInUser.dept}', None)
    print(f'subjects : {subjects}')
    print(subjects)

    # Class Combobox
    def OptionCallBack(arg=None, arg1=None, arg2=None):
        print(variable1.get())
        year1, div1 = variable1.get().split('_')
        print('in options callback')
        subs = []
        if year1 in subjects.keys():
            if div1 in subjects[year1].keys():

                for sub in subjects[year1][div1].keys():
                    subs.append(sub)

        subCb.config(values=subs)
        variable2.set("Select Subject")

    variable1 = StringVar(rootSA)
    variable1.set("Select Class")
    variable1.trace('w', OptionCallBack)

    classCb = Combobox(rootSA, textvariable=variable1)
    classCb.config(values=classesList)
    classCb.pack()
    classCb.place(relx=0.35, rely=0.25, relwidth=0.1, relheight=0.06)

    use = Label(rootSA, text="(Note: Use Dropdown Options)", bg='black', fg='white',
                font=('Courier', 11))
    use.place(relx=0.7, rely=0.25, relheight=0.06)

    # Button to save student data
    btn7 = Button(rootSA, text="Show Attendance", bg='black', fg='white', font=('Courier', 15),
                  command=showAttendance)
    btn7.place(relx=0.4, rely=0.35, relwidth=0.2, relheight=0.070)

    rootSA.mainloop()


def main():
    global rootHodHome, classes, loggedInUser, Canvas5
    loggedInUser = hodLogin.loggedInUser
    classes = loggedInUser.getDetails()['Classes']
    print(classes)
    for key, value in classes.items():
        for div in value:
            classesList.append(f'{key}_{div}')
    print(classesList)

    rootHodHome = Tk()
    rootHodHome.title(f'Welcome to Attendance Management System')
    rootHodHome.resizable(True, True)
    rootHodHome.state("zoomed")

    rootHodHome.minsize(width=700, height=670)
    rootHodHome.geometry('1000x600+150+10')
    Canvas5 = Canvas(rootHodHome)
    Canvas5.config(bg="#3498DB")
    Canvas5.pack(expand=True, fill=BOTH)

    # Logout Button
    logoutBtn = Button(rootHodHome, text="Logout", font=('Sylfaen', 15), command=logout)
    logoutBtn.place(relx=0.9, rely=0.03, relwidth=0.07, relheight=0.04)

    # Set Heading Frame
    headingFrame5 = Frame(rootHodHome, bg="#FFBB00", bd=5)

    headingFrame5.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

    headingLabel5 = Label(headingFrame5, text=f"Welcome {loggedInUser.name}", bg='black', fg='white',
                          font=('Courier', 15))
    headingLabel5.place(relx=0, rely=0, relwidth=1, relheight=1)

    regTeacher = Button(rootHodHome, text="Register Teacher", font=('Sylfaen', 15),
                        command=registerTeacher)
    regTeacher.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)

    assignClass = Button(rootHodHome, text="Assign Classes", font=('Sylfaen', 15),
                         command=funAssignClasses)
    assignClass.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)

    viewAttendancebtn = Button(rootHodHome, text="View Attendance", font=('Sylfaen', 15),
                               command=viewAttendance)
    viewAttendancebtn.place(relx=0.3, rely=0.7, relwidth=0.4, relheight=0.1)
    rootHodHome.update_idletasks()

    rootHodHome.mainloop()


global rootHodHome, loggedInUser, Canvas5, classcb, teachercb, subjectName
global classOptions, teachersOptions, rootAssignClasses
classes = []
classesList = []
