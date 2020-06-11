#!/usr/bin/python3
"""
    Course: IT 101-01 Spring 2020

    Program: DatabaseFunctions.py 
    Author: Reece Williams (rwilliams82 [at] students.cumberland.edu)
    Date: 2020-Feb-25, Version 9.0
    Honor Code: Reece D. Williams
    Description: All backend Database functions are done here.
                 Used to create, change, and check users info

    TODO:
        + Change DBFunctions class to be more classlike for multiple instances
         - in another instance, could have classes and features based on account names.
         - would need to add int ID per user to have linked to both DB's
         - rename functions to addRecord, deleteRecord (treat like an API)
        
        + Salting is not the best
          - add random salt into Credentials.db (Epoch Unix Time Stamp)

        + clean up the use temp variables
        + Add decorators for debugging messages insead of if statements (include function.__qualname__)
        + Make en-us.lang file for debbug messages
        + Make getuserinfo func -> getUserInfo(self, _user, *, showDebug=True) to force use of showDebug in code args

    OS, IDLE and Python Versions:
       Ubuntu Linux 18.04.1 LTS
       IDLE (Thonny) 3.7.4
       Python 3.6.8
"""


from os import path
import hashlib
import sqlite3

# Global Variables
DEBUGGING = 1
DEFAULT_ADMIN_PASSWORD = 'pa'
DATABASE = 'Credentials.db' #":memory:" # if debuggin
CURRENT_LOGGED_IN_USER = ''

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

class DBFunctions:

    def __init__(self):
        self.initDBCheck()
    
    def encryptPass(self, _user, _pass):
        '''Returns salted (username+password) encyrpted hash
           Used when writing a new Password to the DB'''
        salt = _user.lower() + _pass  
        encodedString = str.encode(salt)
        return hashlib.sha1(encodedString).hexdigest()


    def initDBCheck(self):
        '''Creates empty table if it is not in the DB'''
        c.execute("""CREATE TABLE IF NOT EXISTS information (
                    username text,
                    password text,
                    permission text
                )""")

        # If there is no admin account, add it (typically due to a fresh DB)
        if self.getUserInfo('admin', False) == None:
            self.newUser('admin', DEFAULT_ADMIN_PASSWORD, 'admin')

            print("\n[!] NEW ADMIN ACCOUNT WITH DEFAULT PASSWORD CREATED")
            print("\n[!]"*2 + " Make sure to change the default password!\n[!]\n")


    def newUser(self, _user, _pass, _perm='student'):

        _user = _user.lower()
        _pass = self.encryptPass(_user, _pass)

        # If the user does not already exist
        if self.getUserInfo(_user, False) == None:

            # Add the user to the Database
            with conn:
                c.execute("INSERT INTO information VALUES (?,?,?)", (_user, _pass, _perm))

            if DEBUGGING:
                print(f"[+] User: {_user} created")

            return True


    def removeUser(self, _user):

        _user = _user.lower()

        with conn:
            c.execute("DELETE FROM information WHERE username=:user", {'user': _user})

        if DEBUGGING:
            print(f"[-] {_user} removed")

        # If there is no user, it worked successfully
        if self.getUserInfo(_user) == None: 
            return True
        else: 
            return False


    def changeUserInfo(self, _user, _pass="", _perm=""):
        '''changes a users password and/or permission.'''
        _user = _user.lower()

        # If user exsist, continue on
        if self.getUserInfo(_user, False) != None:
            pass
        else:
            print(f"[!] USER: {_user} does not exsist")
            return False

        # Change the password if they exsist AND they want to change the password
        if _pass != "":

            # New password put through encrptPass function
            updatedPassword = self.encryptPass(_user, _pass)

            with conn: # Change the password for the user given their username
                c.execute("UPDATE information SET password=? WHERE username=?", (updatedPassword, _user))

            if DEBUGGING:
                print(f"[+] Password changed for {_user}\n")

        # If you specified to change the permission level,
        # and the perm has an 'a'dmin or 's'tudent in it.
        if _perm != "": 

            with conn:
                c.execute("UPDATE information SET permission=? WHERE username=?", (_perm, _user))

            if DEBUGGING:
                print(f"[!] USER: {_user} permission changed to {newPermission}\n")
                
        else:
            if DEBUGGING:
                print(f"[!] User: {_user} permission is not correct ({newPermission})\n")
            return False

        return True
                

    def getUserInfo(self, _user, showDebug=True):
        '''Grabs all of a users info. (username, passwordhash, permission)'''
        _user = _user.lower()

        with conn:
            c.execute("SELECT * FROM information WHERE username=:user", {"user": _user})

        user = c.fetchone()

        if DEBUGGING and showDebug == True:
            print(f"Got userInfo {user}")
        
        return user


    def checkLogin(self, _user, _pass):        
        '''
        Checks if the input password = username's password hash in the database.
        returns the username if it works. False if it not.
        '''

        global CURRENT_LOGGED_IN_USER

        _user = _user.lower()

        # If the user exsist
        if self.getUserInfo(_user,False) != None:
            # get the DB password hash & current inputed (supplied) hash
            userInformation = self.getUserInfo(_user, False)
            suppliedPassword = self.encryptPass(_user, _pass)

            # if db hash = theirs, set the user to currently logged in
            if userInformation[1] == suppliedPassword:
                if DEBUGGING:
                    print(f"[!] Login for {_user} successful")

                CURRENT_LOGGED_IN_USER = _user
                return _user

            else:
                if DEBUGGING:
                    print("Incorrect Password")
                return False

        else:
            if DEBUGGING:
                print("No account found")
            return False

    def getCurrentUser(self):
        '''
        Returns who is currently logged in after
        checkLogin has been called 1 time successfully
        '''
        return CURRENT_LOGGED_IN_USER


    def numberOfUsers(self):
        '''Admin only function. Returns the number of users in the database'''
        with conn:
            c.execute("SELECT COUNT(*) FROM information")

        return c.fetchall()[0][0]


if __name__ == "__main__":
    # this = DBFunctions()
    # this.initDBCheck()
    # this.newUser('reece','pa')
    pass