class HodDetails:
    name = ''
    dept = ''
    email = ''
    clg = ''
    classes = {}

    def __init__(self, name, dept, email, clg, classes = None):
        if classes is None:
            classes = {}
        self.name = name
        self.email = email
        self.dept = dept
        self.clg = clg
        self.classes = classes

    def getDetails(self):
        return {'Name': self.name, 'College': self.clg, 'Department': self.dept, 'Email': self.email,
                'Classes': self.classes}


class TeacherDetails:
    name = ''
    dept = ''
    email = ''
    clg = ''
    subjects = {}

    def __init__(self, name, dept, email, clg, subjects = None):
        if subjects is None:
            subjects = {}
        self.name = name
        self.email = email
        self.dept = dept
        self.clg = clg
        self.subjects = subjects

    def getDetails(self):
        return {'Name': self.name, 'College': self.clg, 'Department': self.dept, 'Email': self.email,
                'Subjects': self.subjects}


class StudentName:
    fName = ''
    mName = ''
    lName = ''
    fullName = ''

    def __init__(self, fn, mn, ln):
        self.fName = fn
        self.mName = mn
        self.lName = ln
        self.fullName = ' '.join([fn, mn, ln])

    def getName(self):
        return {'First Name': self.fName, 'Middle Name': self.mName, 'Last Name': self.lName,
                'Full Name': self.fullName,
                'Name': self.fullName}


class StudentDetails:
    name = ''
    cls = ''
    rollNumber = 0
    encoding = []
    year = ''
    sec = ''
    clg = ''
    dept = ''

    def __init__(self, name, cls, roll, encoding, clg, dept):
        self.name = name
        self.cls = cls
        self.year, self.sec = self.cls.split(' ')
        self.rollNumber = roll
        self.encoding = encoding
        self.clg = clg
        self.dept = dept

    def getDetails(self):
        return {'Name': self.name.getName(), 'Class': self.cls, 'Academic Year': self.year, 'Division': self.sec,
                'Roll Number': self.rollNumber, 'Encodings': self.encoding, 'Department': self.dept,
                'College': self.clg}
