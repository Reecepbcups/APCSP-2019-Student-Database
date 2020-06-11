from tkinter import messagebox
import os
import hashlib

class functions:
    
    # Create default database if not in Current Working Directory (Folder)
    def __init__(self):
        # Sets so no user is logged in 
        currentLoggedInUser = None 

        # Set databsae, username, and password variables
        global database
        database, adminUsername , adminPassword= 'Database.csv', 'admin', 'admin'
        self.database = database
        
        # Encypt admin password with username salt        
        adminPassword = hashlib.sha256(str.encode(adminUsername + adminPassword)).hexdigest() 

        # If the database.csv is not in current directory
        if os.path.exists(database) == False:
            
            # Open the database file, and write default admin login credentials
            with open(database,'a') as adminAccount:
                adminAccount.write(f'{adminUsername},{adminPassword},admin\n')
                adminAccount.close()
            print(f" [!] Couldn't find Database File In Current Working Directory.\n [!] Creating file with admin credentials from DatabaseFunctions.py\n [!] {database}")
            
 
    # Checks to see if a username has been used or not
    def checkUsedUsernames(self, username=""):
        '''
        This function reads the database, and saves all usernames to a list. This is then compared to the username being
        the user is trying to make for a new account, and will Allow or Deny the account to be made. (returns True or False)
        (returning True means: True that the username has been taken.)
        ** Be sure to set this to a variable when called apon inside a function too allow if statement checking **
        '''

        # Makes sure the username feild is not empty
        if username == "":
            print('You did not specify a username')

        # Gets a list of all lines in the Database, loop through those lines, Split it to only get the first part (username)
        # If username has been used, return TRUE
        else:
            takenUsernames = [checkUsedNames for checkUsedNames in open(database, 'r').readlines()]
            for accounts in takenUsernames: 
                if username in accounts.split(',')[0]: 
                    return True

                
    # Abstract function
    def getLine(self, database, line_num): 
        '''
        Reads the database, and returns just the line with the username the user is checking
        '''
        lines = open(database, 'r').readlines()
        return lines[line_num]


    def register(self, newUser, password):
        '''
        Allows new students to make an account.
        This Checks already used account names, and double checks password are typed right.
        Uses checkUsedUsernames() function
        '''
        
        # returns True if username has already been used
        usedUsername = functions().checkUsedUsernames(newUser) 

        # If username has not been used
        if usedUsername != True:
            
            # Encrypt password (username is used as a cryptographic salt)
            passwordHash = hashlib.sha256(str.encode(newUser + password)).hexdigest() 

            # write username, passwordHASH, permissionLevel to the database
            with open(database, 'a') as f:
                f.write(f'{newUser},{passwordHash},student\n') 
                f.close()
                return True
            
        else:
            # Return false if the username has been used
            return False


    def login(self, username, password):
        '''
        Basic login with logical operators to check for correct info
         - http://book.pythontips.com/en/latest/enumerate.html
        '''
        
        global currentLoggedInUser
        password = hashlib.sha256(str.encode(username + password)).hexdigest()

        # Open database
        with open(database) as f:
            # Get LineNumber, the that line in the database.
            for lineNumber, line in enumerate(f, 1):
                # If their username is in any of those lines
                if username in line:
                    # Get the line number - 1 (This is the index)
                    # Then search this line with the getLine function
                    lineIndex = lineNumber - 1
                    theirInfo = functions().getLine(database, lineIndex)

                    # If the given username & password is correct
                    if username == theirInfo.split(',')[0] and password == theirInfo.split(',')[1]:
                        # Sets current user to logged in account, and group to their group
                        self.currentLoggedInUser = username 
                        self.currentLoggedInUserGroup = theirInfo.split(',')[2].replace('\n','')
                        # return TRUE that the login was successful
                        return True
                        break
                    
                    elif username != theirInfo.split(',')[0] and password != theirInfo.split(',')[1]:
                        # Failed login
                        return False

                    
    # Used to replace the exact line in a file
    def replaceLine(self, database, line_num, text):
        '''
        Reads the database, finds the line you want to change, and rewrites just that 1 line.
        Used in ChangeAccountDetails() Function
        - https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python
        '''
        lines = open(database, 'r').readlines()
        lines[line_num] = text
        out = open(database, 'w')
        out.writelines(lines)
        out.close()                    
                    
       
    def newStudent(self, username='', password='', permissionLevel='student'):
        '''
                                 [!] ADMIN ONLY [!]
        allows an admin to force create a username and password for a new student.
        Auto checks username incase it is already used by another user.
        Uses checkUsedUsernames() function
        '''
        
        hasBeenUsed = functions().checkUsedUsernames(username)
        # if username not been used
        if hasBeenUsed != True: 
            
            if password == '':
                messagebox.showinfo("Error", f"Password field is blank")
                
            else:
                # Add new username & password to the database of users
                with open(database, 'a') as f:
                    passwordHash = hashlib.sha256(str.encode(username + password)).hexdigest()
                    f.write(f'{username},{passwordHash},{permissionLevel}\n')
                    f.close()
                    messagebox.showinfo("Success", f"Account created for: {username}")
                    return True
        else:
            messagebox.showinfo("Error", f"Account '{username}' is already in use")
    
    
    def changeUserInfo(self, accountLookup="", newPass=""):
        '''
                     [!] ADMIN ONLY [!]
        Allows an admin to change another users password
        Uses replaceLine() function.
        '''
        
        if accountLookup=="":
            return False
        
        if newPass != "":
            newPasswordHash = hashlib.sha256(str.encode(accountLookup + newPass)).hexdigest()
        else:
            return False
            
        with open(database) as f:
            # Gets the line number, and line content
            for lineNumber, content in enumerate(f, 1):
                # Compares the account you want against the usernames in the Database
                if accountLookup in content.split(',')[0]:
                    # Replaces the lines content to new username
                    functions().replaceLine(database, lineNumber-1, f"{content.split(',')[0]},{newPasswordHash},{content.split(',')[2]}")



# Create a functions object, easier for debugging this class file
f = functions()
