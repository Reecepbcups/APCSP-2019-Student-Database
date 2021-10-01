#!/usr/bin/python3
"""
    Course: IT 201-01 SP21

    Program: RWilliams-RandomList-V1_1.py 
    Author: Reece W
    Date: 2021-Feb-11, Version 1.0
    Description: Timing my function vs python's insert

    OS, IDLE and Python Versions:
       Ubuntu 18 && Python 3.6.5

    Problem:
    - Time how fast/slow my insert is vs py insert (10,100,1000,10000)
    - Is it good compared to python? (What algo / O())
    (( http://www.laurentluce.com/posts/python-list-implementation/ ))

    *Usage: 
     - python3 RWilliams-RandomList-V1_1 [N]

    Command Line & Output:
    ~$ python3 RWilliams-RandomList-V1_1
        My Insert:      10 inserts time: 0.0
        Python Insert:  10 inserts time: 0.0
        My Insert:      100 inserts time: 0.0
        Python Insert:  100 inserts time: 0.0

        My Insert:      1000 inserts time: 0.0029914379119873047
        Python Insert:  1000 inserts time: 0.0009987354278564453

        My Insert:      10000 inserts time: 0.2786598205566406
        Python Insert:  10000 inserts time: 0.04727292060852051

    Summary:
    - Provided this output with the same algo's, just different functions
    shows that pythons insert() method is quicker. This is due to python
    being writen in C.
        
"""

#____________________________________________________________________________80
'''

'''
import random as r  # (( https://docs.python.org/3/library/random.html ))
import time         # (( https://docs.python.org/3/library/time.html   ))
import sys          # (( https://docs.python.org/3/library/sys.html    ))

ourList = []        # Init our global list
#____________________________________________________________________________80

def main():
    global ourList

    # Get CLI arg, else 10 is default
    NInput = int(sys.argv[1]) if(len(sys.argv)>=2) else 10

    # Get list of unique random generated ints.
    ourList = r.sample(range(0, 1000), NInput)

    # Time my code vs Pythons
    runs = 10000
    myMethodTime(runs)

    # Reset list, then try it with python's insert()
    ourList = r.sample(range(0, 1000), NInput)
    pythonInsertTime(runs)


# MY METHODS
def myMethodTime(numOfIterations):
    '''Times code looped through numOfIters, then output to user'''
    global ourList

    start = time.time()
    for i in range(numOfIterations): 
        insertElement(2, 3)

    print(f"\nMy Insert:\t{numOfIterations} inserts time: {time.time()-start}")


def pythonInsertTime(numOfIterations):
    '''Times code looped through numOfIters, then python's speed to user'''
    global ourList

    start = time.time()    
    for i in range(numOfIterations):
        ourList.insert(2, 40)

    print(f"Python Insert:\t{numOfIterations} inserts time: {time.time()-start}")


# [!] Future Update - replace @ idx
# def replaceElement(num, idx):
#     if(len(ourList) >= idx):
#         ourList[idx] = num


def showList():
    # Output to user and Manipulate List
    print(f"\n(( List Size: {len(ourList)} ))")
    print(ourList)

def deleteElement(idx):
    '''
    Remove an elemet from a List via the index.
    Saves the list without the index we wanted to remove
    by just skipping that element
    '''

    global ourList
    ourList = ourList[0:idx] + ourList[idx+1:]


def insertElement(num, idx):
    '''
    Insert a number at an index between all values.
    [list 1st half] + [insert] + [list 2nd half]
    '''

    global ourList
    if(len(ourList) >= idx):
        ourList = ourList[0:idx] + [num] +  ourList[idx:]
    else:
        print(f"Not Eough Slots for {idx} in ourList")


#____________________________________________________________________________80
main()

