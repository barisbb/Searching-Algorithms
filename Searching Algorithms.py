#Barış Büyüktaş - Cmpe 540

import numpy as np
import sys

class Node: #holds the puzzle values and previous movements
    def __init__(self, value, movements): 
        self.value = value
        self.movements = movements
     
def find_successors(nodeList): #finds successor positions
    successorList = []
    movements=[]
    for i in range(nodeList.shape[0]):
        for j in range(nodeList.shape[1]):
            tmp = np.copy(nodeList)
           
            if(tmp[i,j-1]==None and j-1>=0 and tmp[i,j]!=None and tmp[i,j]!="x"):
                movements.append(str(tmp[i,j])+"l")
                tmp[i,j-1]=nodeList[i,j]
                tmp[i,j]=nodeList[i,j-1]
                successorList.append(tmp)
                
              
            tmp = np.copy(nodeList) 
            if(j+1<goal.shape[0] and tmp[i,j+1]==None and tmp[i,j]!=None and tmp[i,j]!="x"):
                movements.append(str(tmp[i,j])+"r")
                tmp[i,j+1]=nodeList[i,j]
                tmp[i,j]=nodeList[i,j+1]
                successorList.append(tmp)
                
               
               
            tmp = np.copy(nodeList)
            if(tmp[i-1,j]==None and i-1>=0 and tmp[i,j]!=None and tmp[i,j]!="x"):
                movements.append(str(tmp[i,j])+"u")
                tmp[i-1,j]=nodeList[i,j]
                tmp[i,j]=nodeList[i-1,j]
                successorList.append(tmp)
                
               
            tmp = np.copy(nodeList) 
            if(i+1<goal.shape[0] and tmp[i+1,j]==None and tmp[i,j]!=None and tmp[i,j]!="x"):
                movements.append(str(tmp[i,j])+"d")
                tmp[i+1,j]=nodeList[i,j]
                tmp[i,j]=nodeList[i+1,j]
                successorList.append(tmp)                            
               
    return successorList,movements

def insert(node):
    
    succesors,movements=find_successors(node.value)
    for i in range(len(succesors)):

        if(notSame(succesors[i],fringe_before)):
            allMovements=node.movements.copy()
            allMovements.append(movements[i])
            global nInsertedNodes
            nInsertedNodes=nInsertedNodes+1
            succ=Node(succesors[i],allMovements)
            fringe.append(succ)

            
def notSame(a,b):
    ult=True
    for i in range(len(b)):
        if((a==b[i]).all()):
            ult= False
    return ult


def sumMovements(movements):
    count=0
    for i in range(len(movements)):
        count=count+int(movements[i][0:len(movements[i])-1])
    return count

def findIndexforFringe(fringe):
    sum=10000000
    index=0
    for i in range(len(fringe)):
        if(sumMovements(fringe[i].movements)<sum):
            sum=sumMovements(fringe[i].movements)
            index=i
    return index
        

def findIndexforMisplacedTiles(fringe):
     sum=1000
     index=0
     for i in range(len(fringe)):
            count=0
            for j in range(fringe[i].value.shape[0]):
                for z in range(fringe[i].value.shape[0]):
                    if(fringe[i].value[j][z]!=goal[j][z] and fringe[i].value[j][z]!=None):
                        count=count+1
             
            g_n=sumMovements(fringe[i].movements)
            count=count+g_n
            if(count<sum):
                    sum=count
                    index=i
     return index


def manhattanDistanceforMisplacedTiles(fringe):
     sum=1000
     index=0
     for i in range(len(fringe)):
            count=0
            for j in range(fringe[i].value.shape[0]):
                for z in range(fringe[i].value.shape[0]):
                  if(goal[j][z]!=None and goal[j][z]!=0):  
                      pos1,pos2=findIndexinArray(fringe[i].value,goal[j][z])
                      count=count+abs(pos1-j)+abs(z-pos2) 
                    
             
            g_n=sumMovements(fringe[i].movements)
            count=count+g_n
            if(count<sum):
                    sum=count
                    index=i
     return index

def findIndexinArray(array,value):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if(array[i][j]==value):
                return i,j
    
def writeResults(path,movements,cost,nInsertedNodes):
    directions = {"l": "left","r": "right","u": "up","d":"down"}
    f = open(path, "w")
    for i in movements:
         element="move "+i[0:len(i)-1]+" "+directions[i[-1]]+"\n"
         f.write(element)
    f.write("nInsertedNodes: "+str(nInsertedNodes)+"\n")
    f.write("cost: "+str(cost)+"\n")
    f.close()
    
def callFunction(init,method):
    if(method=="bfs"):
        movements,cost=bfs_search(init)
    elif(method=="dfs"):
        movements,cost=dfs_search(init)
    elif(method=="ucs"):
        movements,cost=ucs_search(init)
    elif(method=="astar0"):
        movements,cost=astar0(init)
    elif(method=="astar1"):
        movements,cost=astar1(init)
    elif(method=="my-astar-positive"):
        movements,cost=astarPositive(init)
    return movements,cost


def open_files(init):
  with open(init) as f:
      lines = f.readlines()
  init_array=np.zeros((len(lines),len(lines)), dtype=object)
  for i in range(len(lines)):
        values=lines[i]
        values.replace("\n","")
        eachValue=values.split("\t")
        for j in range(len(lines)):
            
            if(eachValue[j]=="." or eachValue[j]==".\n"):
                init_array[i][j]=None
            elif(eachValue[j]=="x" or eachValue[j]=="x\n"):
                 init_array[i][j]="x"
            elif(eachValue[j]!="x" and eachValue[j]!="x\n"):
               init_array[i][j]=int(eachValue[j])
  return init_array

def bfs_search(init):
    
    while(True):
      if(len(fringe)==0):
         print("No solution")
         break
      node=fringe.pop(0)

      fringe_before.append(node.value)
      if((node.value==goal).all()):
       
         movements,cost= node.movements,sumMovements(node.movements)
         return movements,cost
     
      insert(node)    
    
def dfs_search(init):
    
    while(True):
      if(len(fringe)==0):
         print("No solution")
         break
      node=fringe.pop()
      fringe_before.append(node.value)
      if((node.value==goal).all()):
        
         movements,cost= node.movements,sumMovements(node.movements)
         return movements,cost
      
      insert(node)
      
def ucs_search(init):
    
    while(True):
      if(len(fringe)==0):
         print("No solution")
         break
      node=fringe.pop(findIndexforFringe(fringe))
      fringe_before.append(node.value)
      if((node.value==goal).all()):
        
         movements,cost= node.movements,sumMovements(node.movements)
         return movements,cost
      
      insert(node)

        
def astar0(init):
    
    while(True):
      if(len(fringe)==0):
         print("No solution")
         break
      node=fringe.pop(findIndexforMisplacedTiles(fringe))
      fringe_before.append(node.value)
      if((node.value==goal).all()):
       
         movements,cost= node.movements,sumMovements(node.movements)
         return movements,cost
      
      insert(node)
        
        
def astar1(init):
    
    while(True):
      if(len(fringe)==0):
         print("No solution")
         break
      node=fringe.pop(manhattanDistanceforMisplacedTiles(fringe))
      fringe_before.append(node.value)
      if((node.value==goal).all()):
        

         movements,cost= node.movements,sumMovements(node.movements)
         return movements,cost
         
      
      insert(node)

def astarPositive(init):
    
    while(True):
      if(len(fringe)==0):
         print("No solution")
         break
      node=fringe.pop(manhattanDistanceforMisplacedTiles(fringe))
      fringe_before.append(node.value)
      if((node.value==goal).all()):
        

         movements,cost= node.movements,sumMovements(node.movements)
         return movements,cost
         
      
      insert(node)


init=open_files(sys.argv[2])
goal=open_files(sys.argv[3])
path=sys.argv[4]
methodName=sys.argv[1]

nInsertedNodes = 1
cost=0    
    
fringe=[]
fringe.append(Node(init,[]))

fringe_before=[]  


movements,cost=callFunction(init,methodName)
writeResults(path,movements,cost,nInsertedNodes)
