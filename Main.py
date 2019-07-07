## Reece W.
## AP Computer Science Principles
## 2/18/2019

from tkinter import * 
from tkinter import messagebox
# Imports 'functions' class from DatabaseFunctions.py file.
# Creates functions() object

from DatabaseFunctions import functions  
f = functions()


################################################
#                   GUI
################################################


# Student Calculator (+ Security)
def studentCalculator():

    calculatorWindow = Tk() # Creates calculatorWindow area
    calculatorWindow.title(f"{f.currentLoggedInUser.capitalize()}\'s Calculator")
    calculatorWindow.geometry('300x100')

    def showCalulationAnswer():
        
        # Checks to make sure the user does not enter like: " 4/ "
        try:
            # !! SECURITY !! The eval function is able to run functions, this check to disable basic functions.
            # Without, would result in possible Admin priv. escalation (running functions in the other class)
            if "()" in str(cEntry.get()):
                messagebox.showinfo("No! : )", "You are not allowed to run functions inside of this box.")
            else:
                messagebox.showinfo("Answer", str(eval(cEntry.get())))
                
        except:
            messagebox.showinfo("ERROR", "The Expression you entered is not supported")

        # ReFocuses the calculator windows to the user
        calculatorWindow.focus_force()
    
    
    # Calculator window panel layout
    Label(calculatorWindow, text="Expression:", font=("Arial", 15)).grid(column=0, row=0)
    cEntry = Entry(calculatorWindow,width=30)
    cEntry.grid(column=1, row=0)

    # Call the showCalulationAnswer function using lambda
    calcButton = Button(calculatorWindow, text="Calculate", command=lambda: showCalulationAnswer())
    calcButton.grid(column=0, row=1, pady=5, sticky=W+E, columnspan=2)

    # Close currnet window instance on click
    quitButton = Button(calculatorWindow, text="Quit", command=lambda: calculatorWindow.destroy())
    quitButton.grid(column=0, row=2, sticky=W+E, columnspan=2)
    
    calculatorWindow.mainloop()


# MAIN panel window - Main parent algo with 2 childs       
def create_window():
    
    mainWindow = Tk() # Create bsaic area
    mainWindow.title(f"Logged in as user: {f.currentLoggedInUser.capitalize()}")
    mainWindow.geometry('475x250')

    # Student panel menu
    if f.currentLoggedInUserGroup == 'student':
        calc = Button(mainWindow, text="Calculator", command=studentCalculator)
        calc.grid(column=0, row=0)

    # Admin panel menu
    if f.currentLoggedInUserGroup == 'admin':
        # Get the number of lines in the database, and show to the admin - Math
        usersCount = 0
        with open(f.database, 'r') as db:
            for user in db:
                usersCount += 1 

        Label(mainWindow, text=f"Welcome {f.currentLoggedInUser.capitalize()} <>", font=("Arial", 15)).grid(column=0, row=0)
        Label(mainWindow, text=f"Users In Database: {usersCount}", font=("Arial", 15)).grid(column=1, row=0)
              
        def newStudents():
            newStudent = Tk() # New Student window
            newStudent.title(f"Create new students")
            newStudent.geometry('350x200')
            
            newUsername = Entry(newStudent,width=25)
            newUsername.insert(END, 'New_Username')
            newUsername.grid(column=0, row=3, sticky=W)

            newPass = Entry(newStudent,width=25)
            newPass.insert(END, 'Password')
            newPass.grid(column=0, row=4, sticky=W)

            # https://stackoverflow.com/questions/45441885/python-tkinter-creating-a-dropdown-select-bar-from-a-list
            variable = StringVar(newStudent) 
            variable.set("student")
            dropdown = OptionMenu(newStudent, variable, "student","admin")
            dropdown.grid(column=1, row=4,sticky=W)

            # Get the from this window, and pass it through the database file, then destroy window 
            newStudentBtn = Button(newStudent, text="Create", command=lambda: [f.newStudent(newUsername.get(), newPass.get(), variable.get()), newStudent.destroy()])
            newStudentBtn.grid(column=0, row=5,sticky=W)
            
        def changeAccountPassword():
            accPass = Tk() # New changePassword window
            accPass.title(f"Change Accounts password")
            accPass.geometry('350x200')
                
            username = Entry(accPass,width=25)
            username.insert(END, 'Username')
            username.grid(column=0, row=3, sticky=W)

            newPass = Entry(accPass,width=25)
            newPass.insert(END, 'New Password')
            newPass.grid(column=0, row=4, sticky=W)
            
            def createNewAccount():
                if newPass.get() == "" or newPass.get() == "New Password":
                     messagebox.showinfo("Error", "That Password is not usable (\"\" or \"New Password\")")
                else:
                    f.changeUserInfo(username.get(), newPass.get())
                    accPass.destroy()

            # Change password submit button, and run some checks in the createNewAccount nested child Function        
            changePasswordBtn = Button(accPass, text="Change", command=createNewAccount)
            changePasswordBtn.grid(column=0, row=5,sticky=W)
            accPass.mainloop()

        
        newStudentBtn = Button(mainWindow, text="New Student", command=newStudents)
        newStudentBtn.grid(column=0, row=1,sticky=E+W, pady=(10, 25))
        changeBtn = Button(mainWindow, text="Change Accounts Password", command=changeAccountPassword)
        changeBtn.grid(column=1, row=1,sticky=W, pady=(10, 25)) 
        
        mainWindow.mainloop()


# Login Panel
def login():
    global currentLoggedInUser
    
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showinfo("Failed", "Username or password feild is empty")
        
    else:
        # If username & password is correct
        try: 
            returnValue = f.login(usernameEntry.get(), passwordEntry.get())
            if returnValue == True:
                usernameEntry.delete(0, END) # clears boxes after login to remove from RAM
                passwordEntry.delete(0, END)
                LoginPanel.destroy() # Close LoginPanel Window
                create_window()
                
            else:
                messagebox.showinfo("Failed Login", "Incorrect username or password")
        except: 
            print() # Just a nothing incase of failed login error

# Register panel       
def register():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showinfo("Error", "Username or password feild is empty")
    else:
        isUsed = f.checkUsedUsernames(usernameEntry.get())
        if isUsed != True:
            f.register(usernameEntry.get(),passwordEntry.get())
            messagebox.showinfo("Success", f"Account created for {usernameEntry.get()}")
        if isUsed == True:
            messagebox.showinfo("Error", "Username is already taken")
            usernameEntry.delete(0, END)
            passwordEntry.delete(0, END)
  


# Intial Window
LoginPanel = Tk()
LoginPanel.title("Login panel")
LoginPanel.geometry('275x125')

user = Label(LoginPanel, text="Username:", font=("Arial", 15))
user.grid(column=0, row=1)
usernameEntry = Entry(LoginPanel,width=25)
usernameEntry.grid(column=1, row=1)
usernameEntry.focus()

password = Label(LoginPanel, text="Password:", font=("Arial", 15))
password.grid(column=0, row=2)
passwordEntry = Entry(LoginPanel, show="*", width=25)
passwordEntry.grid(column=1, row=2)


def togglePasswordView():
    # https://stackoverflow.com/questions/48767399/python-how-to-show-password-when-user-clicked-a-button
    # https://www.python-course.eu/tkinter_checkboxes.php
    global entry, passwordEntry
    if var.get() == 0:
        passwordEntry = Entry(LoginPanel, show="*", width=25)
    if var.get() == 1:
        passwordEntry = Entry(LoginPanel, show="", width=25)
    passwordEntry.grid(column=1, row=2)
    
var = IntVar()
checkbutton = Checkbutton(LoginPanel,text="Show password", variable=var, command=togglePasswordView)
checkbutton.grid(column=0, row=3)


btn = Button(LoginPanel, text="Login", command=login)
btn.grid(column=1, row=3, sticky=W)

btn1 = Button(LoginPanel, text="Register", command=register)
btn1.grid(column=1, row=3)

LoginPanel.mainloop()
