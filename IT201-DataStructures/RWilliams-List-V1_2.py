#!/usr/bin/python3
"""
    Course: IT 201-01 SP21

    Program: RWilliams-List-V1_2.py 
    Author: Reece W
    Date: 2021-Feb-11, Version 1.0
    Description: Timing my function vs python's insert

    OS, IDLE and Python Versions:
       Ubuntu 18 && Python 3.6.5

    Problem:
    - Time how fast/slow my insert is vs py insert (10,100,1000,10000)
    - Is it good compared to python? (What algo / O())
    (( http://www.laurentluce.com/posts/python-list-implementation/ ))

    Command Line & Output:
    ~$ python3 RWilliams-CustomList-V1_2.py
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
    being writen in C. Even removing global did not speed up my program
        
"""

#____________________________________________________________________________80
'''

'''
import random as r  # (( https://docs.python.org/3/library/random.html ))
import time         # (( https://docs.python.org/3/library/time.html   ))
import sys          # (( https://docs.python.org/3/library/sys.html    ))

#____________________________________________________________________________80

def main():
    # Get CLI arg, else 10 is default
    NInput = int(sys.argv[1]) if(len(sys.argv)>=2) else 10

    # Timing my code vs python
    iterations = 10000

    # Initiate list from class method
    myList = MyList(NInput)
    myMethodTime(myList, iterations)

    # Initiate new list, then try it with python's insert()
    pyList = r.sample(range(0, 1000), NInput)
    pythonInsertTime(pyList, iterations)


# MY METHODS
def myMethodTime(myList, iterations):
    '''Times code looped through numOfIters, then output to user'''
    start = time.time()

    for i in range(iterations): 
        myList.insertElement(2, 3)

    print(f"\nMy Insert:\t{iterations} inserts time: {time.time()-start}")


def pythonInsertTime(pythonsList, iterations):
    '''Times code looped through numOfIters, then python's speed to user'''
    start = time.time()  

    for i in range(iterations):
        pythonsList.insert(2, 40)

    print(f"Python Insert:\t{iterations} inserts time: {time.time()-start}")



# MY CLASS FOR INSERT / DELETE + formating output
class MyList():
    # https://docs.python.org/3/reference/datamodel.html init,str

    def __init__(self, size): # dunder init the instance
        self.L = r.sample(range(0, 1000), size)

    def __str__(self): # dunder format output:   (size) [list]
        return f'({len(self.L)}) {self.L}'


    def insertElement(self, num, idx):
        '''
        Insert a number at an index between all values.
        [list 1st half] + [insert] + [list 2nd half]
        '''
        if(len(self.L) >= idx):
            self.L = self.L[0:idx] + [num] +  self.L[idx:]
        else:
            _e = f"Not Eough Slots for {idx} in list ("+str(len(self.L))+")"
            raise Exception(_e)


    def deleteIndex(self, idx):
        '''
        Remove an elemet from a List via the index.
        Saves the list without the index we wanted to remove
        by just skipping that element
        '''
        self.L = self.L[0:idx] + self.L[idx+1:]

    def replaceElement(self, num, idx):
        if(len(self.L) >= idx):
            self.L[idx] = num

#____________________________________________________________________________80
main()

