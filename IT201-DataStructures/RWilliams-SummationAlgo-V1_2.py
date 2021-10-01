#!/usr/bin/python3
"""
    Course: IT 201-01 SP21

    Program: RWilliams-SummationAlgo-V1_2.py 
    Author: Reece W
    Date: 2021-Feb-2, Version 1.2
    Description: Sum 1st 'N' numbers with a Loop, Math, or recursion
                 + Timer in seconds

    OS, IDLE and Python Versions:
       Windows 10
       Python 3.6.5

    *Usage: 
     - python3 RWilliams-SummationAlgo-V1_1.py <N> <loop|math|recursion> [i]
        
    Command Line & Output:
    ~$ python3 Summation.py 100000000 Loop
        Summation (N=100000000 & i=1):  5000000050000000
        Using algorithm: For Loop
        Took 4.279836416244507 seconds

    ~$ python3 Summation.py 3222 Recursion
        Summation (N=3222 & i=1):  5192253
        Using algorithm: recursion 
        Took 0.0029926300048828125 seconds

    ~$ python3 Summation.py 9999999999999999999999999999999999999999999 Math
        Summation (N=9's' & i=1): 
        5000000000000000073153476153374365154850214939323275296393.. cont (30)
        Using algorithm: Mathmatical Compute
        Took 0.0014727115631103516 seconds

    Summary:
      - Math works for all numbers up to 154 9's. (overflow error for float)
      - Recursion dies much sooner, even when bypassing Py's 1000 rec. limit
      - Loop would eventually get there, but waiting took a long time
            after around 1 billion numbers

"""

#____________________________________________________________________________80

import sys # Args
import time
sys.setrecursionlimit(10000)

# Default Variables
N = 5
i = 1

# Type of algorithm (( L, M or R))
Algorithm = "L"

#____________________________________________________________________________80

def parsePossibleArgs():
    global N, i, Algorithm

    # Remove init program name idx 0
    argList = sys.argv[1:]
    argsSize = len(argList)
    
    # save cmd args to correct variables
    if(argsSize >= 1):
        N = int(argList[0])

        if(argsSize >= 2): 
            # Get the type of algorithm as 
            #   L: Loop, R: Recursion, M: Math
            Algorithm = argList[1].title()[0]

        if(argsSize >= 3):
            # optional i argument from index to start 
            i = int(argList[2])


# Done In class (2/2/21)
def recursion(n): 
    if n <= 1: 
        return n
    else:
        return recursion(n-1) + n


def main():
    global N, i

    # The 2 strings used to print to the user
    OutputStr_Sum = f"Summation (N={N} & i={i}):\t"
    OutputStr_Alg = "Using algorithm: "

    # Timer init
    start = time.time()

    # Math Algo.
    if(Algorithm == "M"):
        # O(1) - Constants -- Book, pg26. 1.21 arithmetic series
        # Adds the mathmatical compute the the final String outputs
        Output = int(N*(N+1)/2)

        OutputStr_Sum += str(Output)
        OutputStr_Alg += "Mathmatical Compute"


    # Loop Algo.
    elif(Algorithm == "L"):
        # O(N) - loops through list one time
        _output = 0
        for _iteration in range(i, N+1):
            _output += _iteration

        OutputStr_Sum += str(_output)
        OutputStr_Alg += "For Loop"
        

    # Recursion Algo
    elif(Algorithm == "R"):
        OutputStr_Sum += str(recursion(N))
        OutputStr_Alg += "recursion"


    else:
        print("Incorrect Usage: ")
        print("python3 Summation.py <N> <loop|math|recursion> [i]")


    # Output information to the user
    print(OutputStr_Sum)
    print(OutputStr_Alg)
    print(f"Took {time.time() - start} seconds")


#____________________________________________________________________________80

parsePossibleArgs()
main()