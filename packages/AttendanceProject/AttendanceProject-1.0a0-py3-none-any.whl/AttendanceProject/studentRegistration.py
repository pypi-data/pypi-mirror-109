import json
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk

import cv2
import face_recognition
from firebase import firebase

import DataClasses
import ConnectionManager
import HelperClasses
import teacherHome


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


def open_img():
    global imgEncodings
    imgEncodings = []
    registerStudentRoot.filename = filedialog.askopenfile(initialdir = ":", title = "Select a File", filetypes = (
        ("Jpg files", "*.jpg"), ("Png files", "*.png"), ("All Files", "*.*")), parent = registerStudentRoot)
    registerStudentRoot.update()
    uploadedImage = registerStudentRoot.filename
    uploadedImage = open(uploadedImage.name, encoding = "utf8")
    print(uploadedImage)
    print(uploadedImage.name)

    registerStudentRoot.update()

    img = face_recognition.load_image_file(uploadedImage.name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if len(face_recognition.face_encodings(img)):
        imgEncodings = face_recognition.face_encodings(img)[0]
        messagebox.showinfo(title = 'Success', message = 'Image Uploaded Successfully.', parent = registerStudentRoot)
    else:
        imgEncodings = []
        messagebox.showinfo(parent = registerStudentRoot, title = 'Error',
                            message = 'No face Detected. Please upload another image with clear face.')
    registerStudentRoot.update()


def saveStudentsData():
    first_name = firstName.get()
    middle_name = middleName.get()
    last_name = lastName.get()
    stud_class = classCb.get()
    registerStudentRoot.update()

    if not (first_name and middle_name and last_name) or (
            first_name == 'First Name' or middle_name == 'Middle Name' or
            last_name == 'Last Name'
    ):
        messagebox.showinfo(title = 'Error', message = 'Please enter name correctly', parent = registerStudentRoot)
        return
    if (not stud_class) or (stud_class not in classes):
        messagebox.showinfo(title = 'Error', message = 'Please select class from list', parent = registerStudentRoot)
        return

    try:
        roll_no = int(rollNo.get())
    except ValueError:
        messagebox.showinfo(title = 'Error', message = 'Please enter a valid roll number', parent = registerStudentRoot)
        return

    if not len(imgEncodings):
        messagebox.showinfo(title = 'Error', message = 'Please upload a valid image.', parent = registerStudentRoot)
        return
    registerStudentRoot.update()

    studentName = DataClasses.StudentName(first_name, middle_name, last_name)
    stud_encodings = json.dumps(imgEncodings, cls = HelperClasses.NumpyArrayEncoder)

    studentDetails = DataClasses.StudentDetails(studentName, stud_class, roll_no, stud_encodings, loggedInUser.clg,
                                                loggedInUser.dept)

    print(studentDetails.getDetails())

    detailsToBeSaved = {
        'First Name': studentDetails.name.fName,
        'Middle Name': studentDetails.name.mName,
        'Last Name': studentDetails.name.lName,
        'Roll Number': studentDetails.rollNumber,
        'Encodings': studentDetails.encoding
    }

    registerStudentRoot.update()
    result = None

    if ConnectionManager.isConnected():
        firebaseDb = firebase.FirebaseApplication("https://attendanceproject1-default-rtdb.firebaseio.com/", None)
        result = firebaseDb.put(
            f'/Student Details/{studentDetails.clg}/{studentDetails.dept}/{studentDetails.year}/{studentDetails.sec}/',
            studentDetails.name.fullName, detailsToBeSaved)
        registerStudentRoot.update()

    if result:
        messagebox.showinfo(title = 'Success', message = 'Student Record Saved Successfully.',
                            parent = registerStudentRoot)
        registerStudentRoot.destroy()
        teacherHome.rootTeacherHome.mainloop()


def upload_student(args):
    global registerStudentRoot, canvas
    global labelFrame
    global firstName, middleName, lastName, rollNo, loggedInUser, classCb, classes
    loggedInUser = args
    print(loggedInUser.getDetails())
    registerStudentRoot = Tk()
    registerStudentRoot.title("Student Data")
    registerStudentRoot.resizable(True, True)

    registerStudentRoot.minsize(width = 700, height = 670)
    registerStudentRoot.geometry('1000x600+150+10')
    canvas = Canvas(registerStudentRoot)
    canvas.config(bg = "#3498DB")
    canvas.pack(expand = True, fill = BOTH)

    # Set Heading Frame
    headingFrame = Frame(registerStudentRoot, bg = "#FFBB00", bd = 5)
    headingFrame.place(relx = 0.2, rely = 0.01, relwidth = 0.6, relheight = 0.08)

    headingLabel = Label(headingFrame, text = "Manage Student Data", bg = 'black', fg = 'white',
                         font = ('Courier', 15))
    headingLabel.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Frame for Login Area
    labelFrame = Frame(registerStudentRoot, bg = 'black')
    labelFrame.place(relx = 0.040, rely = 0.14, relwidth = 0.92, relheight = 0.65)

    # Name
    lbName = Label(labelFrame, text = "Name : ", bg = 'black', fg = 'white', font = ('Courier', 18))
    lbName.place(relx = 0.08, rely = 0.2, relheight = 0.08)
    firstName = PlaceholderEntry(labelFrame,
                                 "First Name",
                                 style = "TEntry")
    firstName.place(relx = 0.30, rely = 0.19, relwidth = 0.18, relheight = 0.1)

    middleName = PlaceholderEntry(labelFrame,
                                  "Middle Name",
                                  style = "TEntry")
    middleName.place(relx = 0.52, rely = 0.19, relwidth = 0.18, relheight = 0.1)

    lastName = PlaceholderEntry(labelFrame,
                                "Last Name",
                                style = "TEntry")
    lastName.place(relx = 0.74, rely = 0.19, relwidth = 0.18, relheight = 0.1)

    # Class:

    # Combobox Creation 1
    def OptionCallBack():
        print(variable1.get())

    variable1 = StringVar(registerStudentRoot)
    variable1.set("Select Class From List")
    variable1.trace('w', OptionCallBack)

    subs = loggedInUser.subjects
    clsDict = subs.keys()
    cls = []
    divs = []
    classes = []
    for cl in clsDict:
        abc = subs[cl].keys()
        for div in abc:
            classes.append(cl + ' ' + div)

            divs.append(div)
        cls.append(cl)

    print(subs)
    print(cls)
    print(divs)

    print(classes)

    classOptions = classes
    # for item in classesList:
    #     classOptions.append(item)

    lbcls = Label(labelFrame, text = "Class : ", bg = 'black', fg = 'white', font = ('Courier', 18))
    lbcls.place(relx = 0.08, rely = 0.4, relheight = 0.08)

    classCb = ttk.Combobox(labelFrame, textvariable = variable1)

    # Department Options Data
    classCb.config(values = classOptions)
    classCb.pack()
    classCb.place(relx = 0.3, rely = 0.4, relwidth = 0.18, relheight = 0.09)

    use = Label(labelFrame, text = "(Note: Use Dropdown Options)", bg = 'black', fg = 'white',
                font = ('Courier', 11))
    use.place(relx = 0.53, rely = 0.4, relheight = 0.09)

    # Roll No:
    lbRoll = Label(labelFrame, text = "Roll No: ", bg = 'black', fg = 'white', font = ('Courier', 18))
    lbRoll.place(relx = 0.08, rely = 0.6, relheight = 0.08)
    rollNo = Entry(labelFrame)
    rollNo.place(relx = 0.3, rely = 0.6, relwidth = 0.18, relheight = 0.090)

    # Upload Image
    lb5 = Label(labelFrame, text = "Upload Image: ", bg = 'black', fg = 'white', font = ('Courier', 18))
    lb5.place(relx = 0.08, rely = 0.80, relheight = 0.08)

    # Button to upload student image
    std_image = Button(labelFrame, text = "Upload", bg = 'white', fg = 'black', font = ('Courier', 12),
                       command = open_img)
    std_image.place(relx = 0.3, rely = 0.80, relwidth = 0.18, relheight = 0.09)

    # Button to save student data
    btn7 = Button(registerStudentRoot, text = "Save", bg = 'black', fg = 'white', font = ('Courier', 15),
                  command = saveStudentsData)
    btn7.place(relx = 0.28, rely = 0.85, relwidth = 0.45, relheight = 0.070)

    registerStudentRoot.state("zoomed")
    registerStudentRoot.resizable(True, True)
    registerStudentRoot.mainloop()


global registerStudentRoot, canvas
global labelFrame
global firstName, middleName, lastName, rollNo, loggedInUser, classCb, classes
imgEncodings = []
