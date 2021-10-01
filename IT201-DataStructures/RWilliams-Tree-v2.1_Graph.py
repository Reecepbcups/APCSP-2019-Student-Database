#!/usr/bin/python3
"""
    Course: IT 201-01 SP21

    Program: RWilliams-Tree-v2.1_Graph.py 
    Author: Reece W
    Date: 2021-Feb-2, Version 2
    Description: Given N, use dict to create a full binary tree up to N levels (input).
                and traverse all nodes in fewest number of steps.
                myTree = {1:[2,3], ...}
                # create the tree
                # traverse the tree 

    OS, IDLE and Python Versions:
       Windows 10
       Python 3.6.5

    *Usage: 
     - python3 RWilliams-Tree-v2_Graph.py < N(Integer) >

    # Version 1.00+: Creating Tree
    # Version 1.30: Tree traversal
    # Version 2.00: Graphing the tree


    *Output: 
    My Tree: {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9], 5: [10, 11], 6: [12, 13], 7: [14, 15]}
    Traversed: [1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, 13, 7, 14, 15]

"""

#____________________________________________________________________________80

import sys # Argssssss 

from graphviz import Digraph # http://www.graphviz.org/download/ 
# https://graphviz.readthedocs.io/en/stable/manual.html

import math # used for logarithmic function in PDF graph output

#____________________________________________________________________________80

def parseArgs():
    # Remove initial program name@idx 0
    argList = sys.argv[1:]
    
    # save cmd args to correct variables
    if(len(argList) >= 1): return int(argList[0])


def main():

    # Number of levels we want to use. Where node 0 = top parent
    levels = parseArgs()

    # Default if no arg is supplied
    if(levels==None):
        levels = 3

    # if you want level 0, show simple node
    if(levels==0):
        print("My Tree: {1}" )
        exit(1)

    # Creates a binary tree using dictionary comprehension. 
    # binary tree patern key=idx values = [that idx*2 and (idx*2)+1 always]
    # Then the range of which this is done is always a power of 2.
    # This use to be its own dictionary as:
    # # NodesPerLevel = {1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128, ...}
    # But it was redundet after realising that I could just 2^3=8 for the same
    tree = {idx:[idx*2,(idx*2)+1] for idx in range(1, 2**levels)}

    print(f"\nMy Tree: {tree}\n")
    treeTraversal(tree)

    graphOutput(2**levels)
    

def graphOutput(nodes):

    # https://h1ros.github.io/posts/introduction-to-graphviz-in-jupyter-notebook/
    # Set the dot variable as an instance of the Digraph graph
    dot = Digraph(comment='Full Binary Tree')

    # Creates all nodes for the number of nodes needed using
    # 2**levels. So dot.node("1") -> dot.node("31") for levels=(2**5)-1
    for node in range(1, nodes):
        dot.node(str(node)) 

    
    # Add edges for each key [value1,value2] pair
    # ex. dot.edge("1", "2") && dot.edge("1", "3") 
    # Just like creating the binary tree in main algorithm
    for value in range(1, nodes):
        dot.edge(str(value), str(value*2) )      # dot.edge("1", "2")
        dot.edge(str(value), str((value*2)+1) )  # dot.edge("1", "3")
    
    # Render BinaryTree(level).pdf, and do not automatically show it to a user
    dot.render('reece-output/Reece-BinaryTree'+str(int(math.log(int(nodes), 2))), view=False) 


def treeTraversal(myTree):
    # ex. {1: [2, 3], 2: [4, 5], 3: [6, 7]}
    # to [1,2,4,5,3,6,7]

    current = 1
    doRightSide = False
    queue = [] 
    result = [1]

    while current != None:
        for child in myTree[current]: # [2,3]
            current = child

            # if child is a parent ( meaning its not a final node )
            if child in myTree.keys():

                # if child was already checked, test next value in the list
                if child in result:                    
                    continue 

                # Add value to queue and result output
                queue.append(child)
                result.append(child)

                # start back again in the while loop
                break

            else:            
                result.append(child)                

                if queue != []:
                    # get the last value from queue and now try that one
                    current = queue.pop()   
                else:
                    # if the queue is empty and we aready tested the Right
                    # stop
                    if doRightSide:
                        current = None 
                    else:
                        # start back at the top root, and do the right
                        current = 1 
                        doRightSide = True
                             
            

    print(f"Traversed: {result}")
    print("")

#____________________________________________________________________________80
main()




    # Bad code
    # Version 1.0 - stupidly overly complex 
    # level = 1 # 1 is really level 0. Easier for initial value
    # tempList = []
    # finalList = []    
    # # Loop through 1 to N values, where 1 will be the begining root node
    # for i in range(1,N+1):
    #     # add this item (ex. 1) to the tempList
    #     tempList.append(i)
    #     # if the tempList holding is the same number as the level,
    #     if(len(tempList) == level):
    #         # print(tempList)
    #         # not sure why I cant use just tempList, very weird
    #         # add the tempList variables into the final list as shown here:
    #         # [[1], [2, 3], [4, 5, 6, 7]]
    #         finalList.append([item for item in tempList])
    #         tempList.clear()
    #         # Level = Level*2 since each level in the tree needs to be 2 times as long
    #         #ex. 1, then 2 & 3 
    #         level*=2
    # [1]
    # [2, 3]
    # [4, 5, 6, 7]
    # [8, 9, 10, 11, 12, 13, 14, 15]
    # [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


    # Version 1.1 - Setting Tree
    # loop through all of the list in the final list which we will look through
    # for level in range(0, len(finalList)-1):
    #     # For each number in that level... ex [2, 3] would be level "2" (( which is really level 1 ))
    #     for number in finalList[level]:   
    #         # Get which index that number is in the list.   
    #         # This is so we can match it up with the right group of items in the next child group
    #         idx = finalList[level].index(number)*2
    #         # Save the number as a key to the dict and grab the next child level
    #         # in the correct subsections as provided by us obtaining the index
    #         tree[number] = finalList[level+1][idx:idx+2] # finalList[level+1][0:2]


    # Version 1.2 - Nodes Per Level
    # NodesPerLevel Example: {level:total_nodes_in_that_level}
    # NodesPerLevel = {1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128, ...}
    # NodesPerLevel={level:2**level for level in range(1,levels+1)}

    # Version 1.3
    # _temp = 1 
    # for level in range(1,levels+1):
    #     # gets the number of total_nodes for this level
    #     # {1: 2, 2: 4, 3: 8...}
    #     _temp*=2 
    #     # sets this level = that many nodes, with the last node being N
    #     NodesPerLevel[level] = _temp

    #Version 1.3 - Creating Tree. (overly complex)
    # for index in range(1, 2**levels):
        # Simularity of index*2 as the first value in the list when creating a tree
        # ex.   1 = [2,3]      =====>    1 = [(1*2),(1*2)+1]
        # tree[index] = [index*2,(index*2)+1]


    # V1.4: after about a day it just hit me this was just 2**INDEX, and so its not even needed.