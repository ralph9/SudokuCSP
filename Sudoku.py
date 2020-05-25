# -*- coding: utf-8 -*-
"""
Created on Tue Apr 7 16:33:06 2020

@author: Raúl
"""

#class representing the sudoku and the methods to retrieve information from
#it, it will be used by the CSP class to proceed with the forward checking
class sudoku:
    
    #constructor function that assigns the sudoku its model
    def __init__(self,model):
        self.model=model

    #basic function to check if the sudoku is completed or not
    def isGameFinished(self,model):
        gameIsFinished=True
        if model:
            for row in model:
                for col in row:
                    #when we find a 0 on any position of the board
                    #we know the game isn't over yet
                    if col[0]==0:
                        gameIsFinished=False
                        break
        else:
            gameIsFinished=False
        #if the board is fully complete it's game over
        return gameIsFinished

    #function to find the available domain of a subgrid (3x3) 
    #of the board based on the numbers already present on it
    def computeSubgridDomain(self, block):
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #we iterate over the subgrid
        for cellInSubgrid in block:
            #if we find a number we delete if from the domain for 
            #the given subgrid
            if cellInSubgrid[0] in domain:
                domain.remove(cellInSubgrid[0])
        for cellInSubgrid in block:
            #buscamos ceros en el subbloque
            if cellInSubgrid[0]==0:
                #when we find one we attach to it the subgrid domain
                #(on the second slot of the tuple)
                for n in domain:
                    if domain:
                        cellInSubgrid[1].append(n)
        #we return the domain for a specific subgrid of the board
        return domain


    #function to find the domain for a row
    def computeRowDomain(self,model):
        numbersAlreadyInRow=[]
        for row in model:
            #first we loop over the row to see which values are
            #not 0 and we record them
            for item1 in row:
                if not item1[0]==0:
                    #añadir no 0 a la lista
                    numbersAlreadyInRow.append(item1[0])
            #then we loop again and delete from the domain
            #of the cells of the row the values already present
            #in the row
            for item2 in row:
                for number in numbersAlreadyInRow:
                    if number in item2[1]:
                        if item2[1]:
                            #borrar del dominio
                            item2[1].remove(number)
            #empty variable for the next row
            numbersAlreadyInRow=[]

    #function to find the domain for a column
    def computeColumnDomain(self,model):
        numbersAlreadyInColumn=[]
        #we loop the board by columns
        for i in range(9):
            #same as in rows, we record the non-zero values 
            #already in the column
            for j in range(9):
                #valor fila
                item=model[j][i]
                if not item[0]==0:
                    numbersAlreadyInColumn.append(item[0])
            #then we delete the values from the domain of the column
            #if they're already present in the column itself
            for j in range(9):
                #valor columna
                item = model[j][i]
                for number in numbersAlreadyInColumn:
                    if number in item[1]:
                        item[1].remove(number)
            #empty variable for a new column
            numbersAlreadyInColumn=[]


    #function to return the model with the correct domain included
    #(taking into account the row, column and block constraints)
    def computeAllDomains(self,blocks,model):
        subgrid=[]
        for num in blocks:
            iblock=blocks[num]
            for j in iblock:
                #retrieve the number from the subgrid in the model
                item=model[j[0]][j[1]]
                item[1]=[]
                #add the number to the subgrid variable
                subgrid.append(item)
            self.computeSubgridDomain(subgrid)
            #empty subgrid for another iteration
            subgrid=[]
        #calls to row and column domain functions
        self.computeRowDomain(model)
        self.computeColumnDomain(model)
        return model

    def findMinimumDomainForModel(self,model):
        #we find the minimum domain for all the squares that are available 
        #in the sudoku that is the possibility that offers the less branches
        min=9
        minDomainRow=''
        minDomainCol=''
        #we iterate over the model and calculate the domain
        for row in model:
            for item in row:
                #we only stop to calculate in cells that have a domain (zeroes)
                if item[0]==0:
                    #if we found a new minimum domain we store it, as well 
                    #as the position in the board
                    if len(item[1])<min:
                        min=len(item[1])
                        minDomainRow=model.index(row)
                        minDomainCol=row.index(item)
        #we return the desired position
        return minDomainRow,minDomainCol

    #function to check if the current sudoku position is possible to solve
    def isSolvableState(self,model):
        #we traverse the whole board
        for row in model:
            for item in row:
                #it checks whether the value is 0, and if the domain for that 
                #position is empty then we found an unsolvable state
                if item[0]==0 and len(item[1])==0:
                    return False
        return True

    #function for printing the state of the sudoku board at a given point
    def printState(self,model):
        m=0
        #we print by rows
        for i in model:
            #divider for subgrid (3x3 block)
            if not m % 3:
                print('----------------------------')
            print(str(i[0][0])+'  '+str(i[1][0])+'  '+str(i[2][0])+' | '+str(i[3][0])+'  '+str(i[4][0])+'  '+str(i[5][0])
                  +' | '+str(i[6][0])+'  '+str(i[7][0])+'  '+str(i[8][0]))
            m+=1
        print('----------------------------')