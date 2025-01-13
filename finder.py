# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:35:07 2025

@author: Just_
"""

from typing import *
import math
import heapq
from collections import deque

class Finder:
    def __init__(self, origin:Tuple[int,int], destiny:Tuple[int, int], gridProportion=30) -> None:
        #atributes for the coordinates
        self.origin = origin
        self.destiny = destiny
        self.currentPosition:Node = origin
        #atributes for statistics
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
        #cost related atributes
        self.totalCost = 0
        #auxiliary atributs
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesVisited: List[Tuple[int,int]] = []
        self.__gridProportion = gridProportion
    #algorithms self, costFun:Callable[None], is2print=True) -> Tuple[int,List[Tuple[str,int,str]]]

    def greedy(self, costFun:None, heuristic:Callable):
        """
        A função de custo não será utilizada, será apenas para manter a uniformidade
        entre as assinaturas das funções
        """
        heuristicValueOrigin = heuristic(self.origin)
        queue = [(heuristicValueOrigin,self.origin,0)]
        visited = {self.origin:(heuristicValueOrigin,str(self.origin)+"'",0)}

        while queue:
            currentCost, currentNode, currentSteps = heapq.heappop(queue)
            if(currentNode == self.destiny):
                return (currentCost, self.__pathTaken(visited,self.destiny))
            self.__nodesVisited.append(currentNode)
            for neighbour in self.__getNeighbours(currentNode):
                totalCost =  currentCost + heuristic(neighbour) #tem que somar com `currentCost`, se não o valor total será apresentado como "0" pq o custo heurístico do destino para o destino é zero
                heapq.heappush(queue, (totalCost,neighbour,currentSteps+1))
                visited[neighbour] = (totalCost,currentNode,currentSteps+1)
                
    def runPathFiding(self, pathFidingAlgo:str, costFun:str, heuristicFun:str="None", is2print=True):
        pathFidingAlgo:Callable = getattr(self,pathFidingAlgo)
        totalCost, path =  pathFidingAlgo(getattr(self,costFun,None), getattr(self,heuristicFun,None))
        if is2print:
            self.__showResult(totalCost,path)
        return (totalCost,path)
        
    def BFS(self,costFun:Callable,heuristicFun=None) -> Tuple[int,List[Tuple[str,int,str]]]:
        """
        É necessário guardar o pai do nó `current` para fazer o `traceback`,
        a posição de cada nó gerado (obviamente) e o custo dele até o seu pai,
        além da quantidade de passos que se leva do filho ao pai para que os 
        custos C3 e C4 possam ser calculados.
        
        Portanto, é possível salvar essas informações em um dicionário com a 
        estrutura:
            
        (x_{filho}, y_{filho}) : (custo, (x_{pai}, y_{pai}}), passos).
        
        Uma fila será usada para selecionar os nós que irão ser gerados, enquan-
        to o dicionário guardará as informações necessárias para fazer o `trace
        back`. Quanto a fila, era guardará elementos do tipo:
            
        (custo, (x_{filho, y_{filho}}), passos)
        """
        queue = deque()
        queue.append((0,self.origin,0))
                     
        travelled = {self.origin: (0,str(self.origin)+"'",0)}
        
        while queue:
            currentCost, currentNode, currentSteps = queue.popleft()
            self.__nodesVisited.append(currentNode)
            if currentNode == self.destiny:
                return (currentCost, self.__pathTaken(travelled,self.destiny))
            #It adds the generated nodes into the queue
            neighbours = self.__getNeighbours(currentNode)
            for neighbour in neighbours:
                newCost = currentCost + costFun(self.__isItVertical(currentNode,neighbour), currentSteps+1)
                queue.append((newCost,neighbour,currentSteps+1))
                travelled[neighbour] = (newCost, currentNode, currentSteps+1)


    def DFS(self, costFunction:str, is2print=True):
        totalCost, path = None, None

        if costFunction == 'C1':
            totalCost, path = self.__DFS(self.C1)
        elif costFunction == 'C2':
            totalCost, path = self.__DFS(self.C2)
        elif costFunction == 'C3':
            totalCost, path = self.__DFS(self.C3)
        else:
            totalCost, path = self.__DFS(self.C4)
        if is2print:
            self.__showResult(totalCost, path)
        return (totalCost, path)

    def __DFS(self, costFun: Callable) -> Tuple[int, List[Tuple[str, int, str]]]:

        stack = [(0, self.origin, 0)]  # Pilha
        travelled = {self.origin: (0, str(self.origin) + "'", 0)}
        visited = set()


        while stack:
            currentCost, currentNode, currentSteps = stack.pop()

            
            if currentNode in visited:
                continue
            visited.add(currentNode)
            self.__nodesVisited.append(currentNode)

            self.__nodesVisited.append(currentNode)
            
            if currentNode == self.destiny:
                print("destino encontrado")
                return (currentCost, self.__pathTaken(travelled, self.destiny))
            
            neighbours = self.__getNeighbours(currentNode)
            for neighbour in neighbours:
                if neighbour not in visited:
                    newCost = currentCost + costFun(
                        self.__isItVertical(currentNode, neighbour), currentSteps + 1
                    )
                    stack.append((newCost, neighbour, currentSteps + 1))
                    if neighbour not in travelled or newCost < travelled[neighbour][0]:
                        travelled[neighbour] = (newCost, currentNode, currentSteps + 1)
        
        raise ValueError("caminho não encontrado!")
    

                
    def UCS(self, costFunction:Callable,heuristicFun=None) -> Tuple[int,List[Tuple[str,int,str]]]:
        """
        In the way uniform cost search is implementend it depends upon a priority queue
        for choosing among the adjacents with the minimum path and a dictionary for repre-
        senting the map. 
        
        At the beggining, it may seem like they represent the exact same thing and that
        the only data structure needed is the dictionary that represent the map, but this
        is an erronous notion because the algorithm needs a way to be able to store the
        adjacents nodes of the current node.

        For this, the way found was storing them in the priority queue.

        If we were using the traditional Dijkstra, visited would be of the type
        dict[str,List[Tuple[int,str]]], but since this is the UCS the type is of 
        dict[str,Tuple[int,str]]. This happen because of two reasons:

        1. In this variation only the relaxed neighbours are appended into the priority
        Queue
        2. The cost between the `current` and `adj` is stored in the `adj`, not in the 
        `current`, so, when adding elements in the `visited`, this does not generates
        repeated keys.   
        """
        priorityQueue = [(0,self.origin,0)]#distance from parent, nextNode, steps taken to get from parent to nextNode
        visited = {self.origin:(0,str(self.origin)+"'",0)} #da fonte para a fonte, a distância é 0
        #stepsTaken = 0
        while priorityQueue:
            currentCost, currentNode, currentSteps = heapq.heappop(priorityQueue)
            if currentNode == self.destiny :
                #The total cost is returned along with the way from the source to the destination
                return (visited[self.destiny][0], self.__pathTaken(visited,self.destiny))
            self.__nodesVisited.append(currentNode)#acho que o certo era gerado, dps eu mudo. Tbm acho que poderia ser posto antes do if, dps vejo se dá certo
            #relaxamento
            neighbours = self.__getNeighbours(currentNode)
            for neighbour in neighbours:
                totalCost = currentCost + costFunction(self.__isItVertical(currentNode, neighbour),currentSteps+1)
                if ((neighbour not in visited) or (totalCost < visited[neighbour][0])):
                    heapq.heappush(priorityQueue, (totalCost,neighbour,currentSteps+1))
                    visited[neighbour] = (totalCost,currentNode,currentSteps+1)
                    
    def Astar(self, costFunction:Callable, heuristicFun:Callable) -> Tuple[int,List[Tuple[str,int,str]]]:
        heuristicValueOrigin = heuristicFun(self.origin)

        priorityQueue = [(heuristicValueOrigin,self.origin,0)]#distance from parent, nextNode, steps taken to get from parent to nextNode
        visited = {self.origin:(heuristicValueOrigin,str(self.origin)+"'",0)} #da fonte para a fonte, a distância é 0
        #stepsTaken = 0
        while priorityQueue:
            currentCost, currentNode, currentSteps = heapq.heappop(priorityQueue)
            if currentNode == self.destiny :
                #The total cost is returned along with the way from the source to the destination
                return (visited[self.destiny][0], self.__pathTaken(visited,self.destiny))
            self.__nodesVisited.append(currentNode)#acho que o certo era gerado, dps eu mudo. Tbm acho que poderia ser posto antes do if, dps vejo se dá certo
            #relaxamento
            neighbours = self.__getNeighbours(currentNode)
            for neighbour in neighbours:
                totalCost = currentCost + costFunction(self.__isItVertical(currentNode, neighbour),currentSteps+1) + heuristicFun(neighbour)
                if ((neighbour not in visited) or (totalCost < visited[neighbour][0])):
                    heapq.heappush(priorityQueue, (totalCost,neighbour,currentSteps+1))
                    visited[neighbour] = (totalCost,currentNode,currentSteps+1)
                
    #methods related to moviment
    def __goDown(self, position:Tuple[int,int]) -> Tuple[int,int]:
        return (position[0], position[1]-1)
    def __goUp(self, position) -> Tuple[int,int]:
            return (position[0], position[1]+1)
    def __goRight(self, position) -> Tuple[int,int]:
            return (position[0]+1, position[1])
    def __goLeft(self, position) -> Tuple[int,int]:
            return (position[0]-1, position[1])

    #methods related to cost calculations
    def C1(self, nothingImportant, nothingImportant2) -> None:
        return 10
    def C2(self, isVertical:bool, nothingImportant) -> None:
        if isVertical :
            return  10
        return 15
    #nas funções de custo C3 e C4 eu subtraio 1 pois a lista já começa com a origem
    def C3(self, isVertical:bool, amountSteps) -> None:
        if isVertical:
            return 10
        return 10 + (abs((5-amountSteps%6)))
    def C4(self, isVertical:bool, amountSteps) -> None:
        if isVertical:
            return 10
        return 5 + (abs((10-amountSteps%11)))

    #methods related to heuristics
    def euclidianHeuristic(self, neighbour:Tuple[int,int]) -> int:
        return 10 * (self.__euc(neighbour, self.destiny))
    def __euc(self,neighbour:Tuple[int,int], destiny:Tuple[int,int]):
        x1,y1 = neighbour
        x2,y2 = destiny
        return math.floor(math.sqrt(pow(abs(x1-x2),2) + pow(abs(y1-y2),2)))
    def manhatamHeuristic(self, neighbour:Tuple[int,int]):
        return 10 * (self.__man(neighbour, self.destiny))
    def __man(self,neighbour:Tuple[int,int], destiny:Tuple[int,int]):
        x1,y1 = neighbour
        x2,y2 = destiny
        return abs(x1-x2) + abs(y1-y2)
    
    #auxiliary methods
    def __showResult(self,totalCost:int,path:List[Tuple[str,int,str]]) -> None:
        print(f"Cost from {path[0][0]} to {self.destiny} : {totalCost}")
        print(f"steps from {path[0][0]} to {self.destiny} : {len(path)}")

        for i in range(len(path)):
            print(f"{path[i][0]}--({path[i][1]})-->{path[i][2]}",end="")
            if i != len(path)-1:
                print(" --> ",end="")

    def __pathTaken(self, minSpanningTree:Dict[str,Tuple[int,str]], definitiveDestiny:str):
        pathTaken:List[Tuple[str,int,str]] = []
        
        parent:str = minSpanningTree[definitiveDestiny][1]
        changingDestiny:str = definitiveDestiny

        while True:
            pathTaken.append((minSpanningTree[changingDestiny][1],minSpanningTree[changingDestiny][0],changingDestiny))
            changingDestiny = parent
            parent = minSpanningTree[parent][1]
            if parent == str(self.origin)+"'":
                break
        
        pathTaken.reverse()
        return pathTaken

    def __getNeighbours(self,coord:Tuple[int,int]) -> List[Tuple[int,int]]:
        neighboursBeta = [self.__goDown(coord), self.__goUp(coord), self.__goRight(coord), self.__goLeft(coord)]
        #filter the invalid
        for i in range(len(neighboursBeta)):
            if (neighboursBeta[i][0] < 0 or neighboursBeta[i][0] > self.__gridProportion) or ((neighboursBeta[i][1] < 0 or neighboursBeta[i][1] > self.__gridProportion)):
                neighboursBeta[i] = None
        return [node for node in neighboursBeta if ((node != None) and (not self.__wasItVisited(node)))] # existe a possibilidade da lista retornada estar vazia

    def __wasItVisited(self, coord:Tuple[int,int]):
        return coord in self.__nodesVisited

    def __isItVertical(self, currentNode:Tuple[int,int], neighbour:Tuple[int,int]):
        return abs(currentNode[1] - neighbour[1]) > 0

    def __reset(self):
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
        #cost related atributes
        self.totalCost = 0
        self.totalSteps = 0

def main():
    a = Finder((0,0),(3,3),gridProportion=4)
    x = Finder((0,0),(3,3),gridProportion=4)
    try:

        b,c = a.runPathFiding("greedy","C","manhatamHeuristic")
        print(" ")


        print("===================")
        b, c = x.DFS("C1")
        print(b)
        print(c)
        print("===================")
        
    except TypeError:
        print("deu ruim")
    #a.tester()
if __name__ == "__main__":
    main()

"""
casos de testes
(0,0) -> (3,3) qProportion=3
    Esse caso deu errado, pois existiam 1 caminho não adjacente com o mesmo peso
    de um caminho adjacente, então, aconteceu de o caminho não adjacente ser es-
    colhido.
    
    Portanto, antes de fazer o pop do dicionário, é necessário observar se o nódulo
    que no qual o pop foi feito é adjacente ao currentNode.
"""
