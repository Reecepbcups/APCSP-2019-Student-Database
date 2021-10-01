#!/usr/bin/python3
"""
    Course: IT 201-01 SP21

    Program: RWilliams-Sorting-v1.1.py 
    Author: Reece W
    Date: 2021-Feb-2, Version 2
    Description: Given a list of N unique numbers (N=10,100,1000)
                Time each for 1000 times
                - Python's list sort method
                - Insertion
                - Merge
                - Quick 
                Display results on a table = formating output to CLI

    OS, IDLE and Python Versions:
       Ubuntu 18
       Python 3.6.5 (Sublime3)

    *Usage & Output: 
     - python3 RWilliams-Sorting-v1.1.py 

        Reece Williams  :Ubuntu 18
        Alogirthm   :N  :M  :Mean Time (ms)

        PythonSort  :10     :5  :0.0017ms
        InsertSort  :10     :5  :0.0027ms
        mergeSort   :10     :5  :0.0825ms
        QuickSort   :10     :5  :0.1483ms

        PythonSort  :100    :5  :0.0156ms
        InsertSort  :100    :5  :0.0151ms
        mergeSort   :100    :5  :1.8548ms
        QuickSort   :100    :5  :38.9361ms

        PythonSort  :1000   :5  :0.2223ms
        InsertSort  :1000   :5  :0.1585ms
        mergeSort   :1000   :5  :31.7351ms
        QuickSort   :1000   :5  :24784.0161ms

"""

#____________________________________________________________________________80

from functools import wraps # https://docs.python.org/3/library/functools.html
import random as r
import time
import sys                  
sys.setrecursionlimit(2500)

#____________________________________________________________________________80

# Number of times to test each N
totalIters = 5

# Dict of total times per function algorithm 
# (( Adds all values for a given function before getting avg))
times = {}

# Decorator to tally time taken per function call
def timeit(myF):
    @wraps(myF)
    def timed(*args, **kw):
        timeStart = time.time()
        output = myF(*args, **kw)
        timeEnd = time.time()

        updateTimes(myF.__name__, timeStart, timeEnd)
        return output
    return timed


def main():
    print("Reece Williams\t:Ubuntu 18")
    print("Alogirthm\t:N\t:M\t:Mean Time (ms)\n") 

    for N in [10, 100, 1000]:
        for M in range(totalIters):

            # generate unique list
            myList = uniqueList(N)

            # Run sorting algorithms
            PythonSort(myList)
            InsertSort(myList)                             
            mergeSort(myList)
            QuickSort(myList, 0, len(myList)-1)

        # Output sorting algorithms
        for method in times: 
            #     Alogirthm    :N    :M       Mean Time
            print(f"{method}\t:{N}\t:{M+1}\t:{times[method]/(M+1):.4f}ms")
            times[method] = 0
        print()


def updateTimes(method, startTime, endTime):
    '''Update time for a given sort method'''

    if method not in times:
        times[method] = 0

    # add function run time to memory + current total run time for functions
    times[method] = times[method]+((endTime-startTime)*1000)

@timeit
def PythonSort(myList):
    return myList.sort()


@timeit
def InsertSort(myList): # Page 255 book
    for i in range(1, len(myList)):
        temp = myList[i]
        k = i
        while k > 0 and temp < myList[k-1]:
            myList[k] = myList[k-1]
            k-=1
        myList[k] = temp
    return myList


@timeit
def mergeSort(arr):
    # https://www.geeksforgeeks.org/merge-sort/
    if len(arr) > 1:
        # Finding the mid of the array
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        mergeSort(L)
        mergeSort(R)

        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1  
  


@timeit
def QuickSort(arr, low, high):
    if len(arr) == 1:
        return arr

    if low < high:
        pi = partition(arr, low, high)

        try:
            QuickSort(arr, low, pi-1)
            QuickSort(arr, pi+1, high)
        except:
            return "RecurrsionError"

def partition(arr, low, high):
    i = (low-1)          
    pivot = arr[high]     

    for j in range(low, high):
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def uniqueList(Size):
    '''Gives back an entirely unique list per instance for a given size'''
    return r.sample(range(0, 50000), Size)



#____________________________________________________________________________80
main()