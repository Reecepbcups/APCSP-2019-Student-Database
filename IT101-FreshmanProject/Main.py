#!/usr/bin/python3
"""
    Course: IT 101-01 Spring 2020

    Program: Main.py 
    Author: Reece Williams (rwilliams82 [at] students.cumberland.edu)
    Date: 2020-Feb-25, Version 7.0
    Honor Code: Reece D. Williams
    Description: The initial window which allows login,
                 and registration.

    TODO
         - Find a cleaner way to prettify code (maybe classes with tkinker)
         - allow user to press enter to login, rather than having to click with a button
         - Move userPanels code intot the getAccess login function. Much simpler, and still
               makes it easy to add a teacher panel if needed

    OS, IDLE and Python Versions:
       Ubuntu Linux 18.04.1 LTS
       IDLE (Thonny) 3.7.4
       Python 3.6.8
"""

from tkinter import messagebox 
from tkinter import *

# imported CWD files
from PanelFeatures import studentPanel, adminPanel
from DatabaseFunctions import DBFunctions

db = DBFunctions()

st = studentPanel()
ap = adminPanel()


def main():
    '''
    Initial Login Panel
    '''
    
    global LoginPanel, usernameEntry, passwordEntry

    # initial Login panel specs
    LoginPanel = Tk()
    LoginPanel.title("Login panel")
    LoginPanel.geometry('350x125')
    
    # username label and entry on initial window
    userlbl = Label(LoginPanel, text="Username:", font=("Arial", 15))
    usernameEntry = Entry(LoginPanel,width=25)
    userlbl.grid(column=0, row=1)
    usernameEntry.grid(column=1, row=1)

    usernameEntry.focus()

    # Password label and entry on initial window
    passwordlbl = Label(LoginPanel, text="Password:", font=("Arial", 15))
    passwordEntry = Entry(LoginPanel, show="*", width=25)
    passwordlbl.grid(column=0, row=2)
    passwordEntry.grid(column=1, row=2)

    # login and register buttons. Calls getAccess below.
    loginBtn = Button(LoginPanel, text="Login", command=lambda: [getAccess('Login')])
    registerBtn = Button(LoginPanel, text="Register", command=lambda: [getAccess('Register')])
    loginBtn.grid(column=1, row=3, sticky=W)
    registerBtn.grid(column=1, row=3)

    LoginPanel.mainloop()


def getAccess(func="Login"):
    '''
    login/register functions
    '''

    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == '' or password == '':
        messagebox.showinfo("Error", "Username or password feild is empty")
        return False

    # If user presses the login button
    if func=='Login':
        if db.checkLogin(username, password) != False:
            CURRENT_LOGGED_IN_USER = username
            # Remove window from view, and call the correct panel type
            LoginPanel.destroy()
            userPanels(username)
        else:
            messagebox.showinfo("Error", f"No username found for {username}")

    # If user presses the register button
    if func=='Register':
        if db.getUserInfo(username) == None:
            db.newUser(username, password, "student")
            messagebox.showinfo("Success", f"Account created for {username}")
            getAccess("Login")

        else:
            messagebox.showinfo("Error", "Username is already taken")    


def userPanels(_user):
    '''
    Gets users permissions level and gives the corrosponding panel
    '''

    # returns 's' for student, and 'a' for admin (0th index)
    current_group = db.getUserInfo(_user)[2][0]

    # Admin panel functions
    if current_group == 'a':
        ap.main(_user)

    # Student Panel (all other users)
    else:
        st.main(_user)


   

# Calls initial main window
main()