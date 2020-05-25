# -*- coding: utf-8 -*-
"""
Created on Mon Apr 6 20:16:36 2020

@author: Raúl
"""

import copy
from Sudoku import sudoku
import time


sudokuForTest = "..7.....1.58......6.197...2...48.29.......3.6...3.7..............5.46..8.6..1..5."

#function to extract a cube in arrays from the string that represents the sudoku
def get_sudokus():
    listOfCells = split_in_chars(sudokuForTest)
    finalSudoku = []
    for i in range(len(listOfCells)):
        if listOfCells[i] == ".":
            listOfCells[i] = 0
    for i in range(9):
        valuesForRow = listOfCells[slice(i*9,i*9+9)]
        listForCell = []
        rowForSudoku = []
        for value in valuesForRow:
            value = int(value)
            listForCell.append(value)
            startingDomain = []
            listForCell.append(startingDomain)
            rowForSudoku.append(listForCell)
            listForCell = []
        finalSudoku.append(rowForSudoku)
    return finalSudoku
    
#function that splits a string in its individual characters
#useful in get_sudokus() to split the original sudoku layout
def split_in_chars(word): 
    return [char for char in word]  


#class representing the CSP problem, in this case it has the backtrackingFC
#algorithm, as well as a constructor and the startSolving() method
#that starts the procedures
class csp:
    atLeastOneSolutionFound = False
    
    def __init__(self,model):
        self.sudo = sudoku(model=model)
        self.model=model
        #subgrid system for a 9x9 sudoku board
        #each row is formed by the cells that belong to the subgrid
        self.block={0:[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)],
            1:[(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)],
            2:[(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)],
            3:[(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)],
            4:[(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)],
            5:[(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)],
            6:[(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)],
            7:[(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)],
            8:[(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]
            }

    def backtrackingFC(self,pmodel):
        #we check for the minimum domain cell for the current state of the
        #sudoku board
        i,j=self.sudo.findMinimumDomainForModel(pmodel)
        #we have to check that the minimum found is a valid position
        #i.e. valid branch to continue
        if not i=='' and not j=='':
            #we go over that min. domain
            tempPosition=pmodel[i][j]
            for numInDomain in tempPosition[1]:
                #copy by content, not by reference of the sudoku model
                copyOfSudoku=copy.deepcopy(pmodel)
                #we extract the first possibility from the remaining domain
                item=copyOfSudoku[i][j][1].pop(copyOfSudoku[i][j][1].index(numInDomain))
                #we insert it in the copy of the board
                copyOfSudoku[i][j][0]=item
                #we continue computing the domain for the temporal board
                model_temp=self.sudo.computeAllDomains(blocks=self.block, model=copyOfSudoku)
                #if it is not an unsolvable state we continue with the forward
                #checking procedure
                if self.sudo.isSolvableState(model_temp):
                    self.backtrackingFC(model_temp)
                #print("fin")
                #clself.sudo.printState(model_temp)
                #if the sudoku is finished we print its final solved state
                if self.sudo.isGameFinished(model_temp):
                    self.atLeastOneSolutionFound = True
                    print("Game is finished")
                    self.sudo.printState(model_temp)

    def startSolving(self):
        #compute domains for all the 0 cells of the board
        self.sudo.computeAllDomains(blocks=self.block, model=self.model)
        #do actual work on the sudoku
        self.backtrackingFC(self.model)
        if not self.atLeastOneSolutionFound:
            print("No solutions found for this setup")
               
    
modelForTest=[
    [[8,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]]],
    [[0,[]],[0,[]],[3,[]],[6,[]],[0,[]],[0,[]],[0,[]],[0,[]],[0,[]]],
    [[0,[]],[7,[]],[0,[]],[0,[]],[9,[]],[0,[]],[2,[]],[0,[]],[0,[]]],
    [[0,[]],[5,[]],[0,[]],[0,[]],[0,[]],[7,[]],[0,[]],[0,[]],[0,[]]],
    [[0,[]],[0,[]],[0,[]],[0,[]],[4,[]],[5,[]],[7,[]],[0,[]],[0,[]]],
    [[0,[]],[0,[]],[0,[]],[1,[]],[0,[]],[0,[]],[0,[]],[3,[]],[0,[]]],
    [[0,[]],[0,[]],[1,[]],[0,[]],[0,[]],[0,[]],[0,[]],[6,[]],[8,[]]],
    [[0,[]],[0,[]],[8,[]],[5,[]],[0,[]],[0,[]],[0,[]],[1,[]],[0,[]]],
    [[0,[]],[9,[]],[0,[]],[0,[]],[0,[]],[0,[]],[4,[]],[0,[]],[0,[]]]
]

initialBoard = get_sudokus()
start_time = time.time()
csp=csp(initialBoard)
csp.startSolving()
print("--- %s seconds ---" % (time.time() - start_time))
