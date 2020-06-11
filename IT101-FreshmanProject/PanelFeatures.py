#!/usr/bin/python3
"""
    Course: IT 101-01 Spring 2020

    Program: PanelFeatures.py 
    Author: Reece Williams (rwilliams82 [at] students.cumberland.edu)
    Date: 2020-Feb-25, Version 11.0
    Honor Code: Reece D. Williams
    Description: The main core of features for administrator,
                 and students. 

    TODO:
        - its messy, clean it up and add grid entry to the inserted objects
        - regex for newFile find and replace, might be quicker
        - Change any concatination from += to ''.join() as its faster
        - usernameInput.get() should be saved to a local scope variable then passed through the functions

    OS, IDLE and Python Versions:
       Ubuntu Linux 18.04.1 LTS
       IDLE (Thonny) 3.7.4
       Python 3.6.8
    
"""

from tkinter import *
from tkinter import messagebox
from datetime import date
import webbrowser
import pyperclip
import platform
import sys
import os


from DatabaseFunctions import DBFunctions
db = DBFunctions()


TEMPLATE_FILENAME = 'Python.tmpl'
CLASS = "IT101"
CURRENT_USER = ''

class studentPanel:

    def main(self, _currentUser):
        '''
        Creates Front-end panel to place all inputs and buttons
        '''

        global CURRENT_USER
        CURRENT_USER = _currentUser

        mainWindow = Tk() 
        mainWindow.title(f"Logged in as user: {CURRENT_USER.capitalize()}")
        mainWindow.geometry('550x250')

        # Input field for assignments
        fInput = Entry(mainWindow, width=25)
        fInput.insert(END, 'Assigment')
        fInput.grid(column=0, row=0, sticky=W)

        # Creates the assignment based on the input field
        fInputBtn = Button(mainWindow, text="New File", command=lambda: \
            [self.newFile(fInput.get(), CURRENT_USER)])
        fInputBtn.grid(column=1, row=0, sticky=W)

        # Opens GMAIL and copies default text format. Fills in fInput field if the user has something there.
        emailBtn = Button(mainWindow, text="Send as Email", command=lambda: \
            [self.newEmail(CURRENT_USER, fInput.get())])
        emailBtn.grid(column=2, row=0, sticky=W)

        # Characters to ascii number, number to ascii char
        asciiCharCode = Entry(mainWindow, width=25)
        asciiCharCode.insert(END, 'Ascii Values')
        asciiCharCode.grid(column=0, row=3, sticky=W)
        asciiBtn = Button(mainWindow, text="Convert", command=lambda: \
            [self.asciiVal(asciiCharCode.get())])
        asciiBtn.grid(column=1, row=3, sticky=W)

        # Decimal to binary input & button
        decInput = Entry(mainWindow, width=25)
        decInput.insert(END, 'Decimal -> Binary')
        decInput.grid(column=0, row=4, sticky=W)
        emailBtn = Button(mainWindow, text="Dec > Bin", command=lambda: \
            [self.decToBin(decInput.get())])
        emailBtn.grid(column=1, row=4, sticky=W)

        # Googles your issues for you. "Google It"!
        googleInput = Entry(mainWindow, width=25)
        googleInput.insert(END, 'Type issue here.')
        googleInput.grid(column=0, row=5, sticky=W)
        googleBtn = Button(mainWindow, text="Google It", command=lambda: \
            [self.googleIt(googleInput.get())])
        googleBtn.grid(column=1, row=5, sticky=W)


    def newFile(self, _assigment, _currentUser):
        ''' 
        Creates a file with correct filename formating & correct commented code.
        '''

        # 123199 (MMDDYY)
        todayFormated = date.today().strftime("%m%d%y")

        # Makes sure filename has no spaces
        assignment = _assigment.replace(' ','_')

        # Creats filename (CURRENT_USER-HW_ASSIGNMENT_1-IT101-022120-V1.py)
        filenameFormated = f"{_currentUser}-{assignment}-IT101-{todayFormated}-V1.py"

        # Make the file if it does not exist yet.
        if os.path.exists(filenameFormated) == False:

            template = open(TEMPLATE_FILENAME).read()
            f = open(filenameFormated,'a')

            # Variables within the comments file (python.tmpl) to replace with the correct values
            # via a for loop
            strToReplace = [
                ('{{class}}', CLASS),
                ('{{author}}', _currentUser.capitalize()),
                ('{{file_name_with_extension}}', filenameFormated),
                ('{{create_time}}', date.today().strftime("%b-%d-%Y")),
                ('{{python_version}}', sys.version.split(' ')[0]),
                ('{{system_version}}', f"{platform.system()} {platform.release()} ({platform.version()})")
             ]

            for _str in strToReplace:
                template = template.replace(_str[0], _str[1])

            f.write(template)
            f.close()

            openEditor = messagebox.askquestion("File", f"File {assignment} created!\nOpen in editor?")
            # The webbrowser module opens with default editor.
            if openEditor == 'yes':
                webbrowser.open(filenameFormated)

        else:
            messagebox.showinfo("Error", "Filename already exists")


    def newEmail(self, _currentUser, _file=""):
        '''
        Correctly makes email body and copies the contents, opens gmail and composes a fresh email.
        '''

        ASSIGNMENT = "ASSIGNMENT_INFO_HERE"   
        if _file != '' and _file != "Assigment":
                ASSIGNMENT  = _file    

        email = f'''Dr. Nichols,\n\nAssignment: {ASSIGNMENT} attached.\n\nSincerely,\n{_currentUser.capitalize()}'''

        try: # Fix for linux machines do not have the correct module
            pyperclip.copy(email)
        except:
            print("If you are on linux: ' sudo apt-get install xclip '")

        webbrowser.open('https://mail.google.com/mail#inbox?compose=new')
        messagebox.showinfo("Success", "Copy and paste in GMAIL")

    def decToBin(self, _number, _optionalAscii=''):
        '''
        Turns a decimal number to binary representation if its a number.
        '''

        if _number.isdigit():
            _number = int(_number)
            messagebox.showinfo("Dec>Bin", f"{_number} in binary is: {bin(_number)[2:]}")

        else:
            messagebox.showinfo("Error", f"{_number} does not seem to be a number.")

    def asciiVal(self, _value):
        '''
        If the user enters a number: outputs ascii character (ex. 65 -> A)
                           a letter: outputs ascii value     (ex. A -> 65)
        '''
        # Removes un-needed extra space and splits char's.
        _value = _value.strip().split(' ')
        output = ''

        for val in _value:
            # is a number (ex. 65)
            if val.isdigit():
                output += f"{chr(int(val))} "

            # Single char String split at space ' '
            elif type(val) == str and len(val) == 1:
                output += f"{str(ord(val))} "

            else:
                output += "\nMake sure to add spaces between characters"
                break

        # Shows the output for both numbers and ascii chars.
        messagebox.showinfo("ASCII", f"{' '.join(_value)}\n{output}")

    def googleIt(self, _phrase):
        '''
        Googles their question and adds python3 OS to the end of the search phrase
        '''

        system = platform.system()
        version = platform.release()

        _phrase = _phrase.replace(' ', '+')
        webbrowser.open(f'https://www.google.com/search?q={_phrase}+python3+{system}+{version[0:6]}')

class adminPanel:

    def main(self, CURRENT_USER):
        mainWindow = Tk() # Create basic panel
        mainWindow.title(f"Logged in as user: {CURRENT_USER.capitalize()}")
        mainWindow.geometry('475x250')

        # Num of users in db button
        label1 = Label(mainWindow, text=f"Database Users: {db.numberOfUsers()}", font=("Arial", 11))
        label1.grid(column=0, row=0)

        # -= Remove user entry and button
        usernameInput = Entry(mainWindow, width=20)
        usernameInput.insert(END, 'Username')
        usernameInput.grid(column=0, row=1, sticky=W)
        

        passwordInput = Entry(mainWindow, width=20)
        passwordInput.insert(END, 'New Password')
        passwordInput.grid(column=1, row=1, sticky=W)
        

        permissionInput = Entry(mainWindow, width=20)
        permissionInput.insert(END, 'New Permission')
        permissionInput.grid(column=2, row=1, sticky=W)
        

        makeNewUser = Button(mainWindow, text="Create User", command=lambda: \
            [db.newUser(usernameInput.get(), passwordInput.get(), permissionInput.get())])
        makeNewUser.grid(column=0, row=2, sticky=W)

        remUserBtn = Button(mainWindow, text="Remove User", command=lambda: \
            [db.removeUser(usernameInput.get())])
        remUserBtn.grid(column=0, row=3, sticky=W)

        chgPassBtn = Button(mainWindow, text="Change Password", command=lambda: \
            [db.changeUserInfo(usernameInput.get(), passwordInput.get())])
        chgPassBtn.grid(column=0, row=4, sticky=W)

        chgPermBtn = Button(mainWindow, text="Change Perm", command=lambda: \
            [db.changeUserInfo(usernameInput.get(), '', permissionInput.get())])
        chgPermBtn.grid(column=0, row=5, sticky=W)


    def removeUser(self, _username):
        if db.removeUser(_username) == True:
            messagebox.showinfo('Success!', f'User {_username} has been removed!')
        else:
            messagebox.showinfo('Error!', f'User "{_username}" is not in the database!')


    def changeUserInformation(self, _username, _pass='', _perm=''):
        value = db.changeUserInfo()

    def newUser():
        pass
        
if __name__ == "__main__":
    pass