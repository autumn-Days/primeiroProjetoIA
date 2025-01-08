from typing import *
import math
import heapq

class Finder:
    def __init__(self, nodeCollection:Set[Node], origin:Tuple[int,int], destiny:Tuple[int, int]) -> None:
        #atributes for the coordinates
        self.origin = origin
        self.destiny = destiny
        self.currentPosition:Node = origin
        #atributes for statistics
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
        #cost related atributes
        self.totalCost = 0
        self.totalSteps = 0
    #algorithms
    def uniformCost(self, costFun:function) -> List[Tuple[int,int]]: #aka Dijkstra
        if costFun.__name__ == 'self.C1':
            return self.__uniformCostC1()

    def __uniformCostC1(self) -> Tuple[int,str]:
        priorityQueue = [(self.origin,0)]
        visited = {self.origin:(self.origin+"'"), 0} #da fonte para a fonte, a distância é 0

        while priorityQueue:
            currentNode:str, currentCost:int = heapq.heappop(priorityQueue)
            if currentNode == destiny :
                #The total cost is returned along with the way from the source to the destination
                return (self.totalSteps*10, self.pathTaken())
            #relaxamento
            for neighbour in self.__getNeighbours(origin):
        
    def __getNeighbours(self,coordinate:Tuple[int,int]):
        a = [self.__goDown(coordinate), self.__]

    def greedySearch(sefl, costFun:function, heuristicFun:function):
        #somente se costFun.__name__ == C3 || == C4 então self.totalSteps setá incrementado
        pass
    #methods related to moviment
    def __goDown(self) -> Tuple[int,int]:
        return (self.currentPosition, self.currentPosition-1)
    def __goUp(self) -> Tuple[int,int]:
            return (self.currentPosition, self.currentPosition+1)
    def __goRight(self) -> Tuple[int,int]:
            return (self.currentPosition+1, self.currentPosition)
    def __goLeft(self) -> Tuple[int,int]:
            return (self.currentPosition-1, self.currentPosition-1)

    #methods related to heuristics
    def euclidianHeuristic(self, neighbour:Tuple[int,int]) -> Tuple[int,int]:
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
    #methods related to cost calculations
    def C1(self) -> None:
        return 10
    def C2(self, isVertical:bool) -> None:
        if isVertical :
            return  10
        return 15
    def C3(self, isVertical:bool) -> None:
        if isVertical:
            return 10
        return 10 + (abs((5-self.totalSteps))%6)
    def C4(self, isVertical:bool) -> None:
        if isVertical:
            return 10
        return 5 + (abs((10-self.totalSteps))%11)
    #other methods
    def reset(self):
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
        #cost related atributes
        self.totalCost = 0
        self.totalSteps = 0
    #auxiliary methods

def main():
    """
    input:

    x1 y1 [local]
    x2 y2 [local]
    x3 y3 [local]
    ...
    xn yn [local]
    !END
    origem destino

    output:

    (x_{a},y_{b}) -> (x_{c},y_{d}) -> (x_{e},y_{f}) -> ... -> (x_{y},y_{z}) 
    """
    coordinatesCollections:Set[Node] = set()
    #asking for coordinates
    askIpunt:str = ""
    while True:
        askInput = input("")
        if askInput == "!END":
            break
        askInput = askInput.split()
        try:
            coordinatesCollections.add(Node(int(askInput[0]),int(askInput[1]), askInput[2]))
        except IndexError:
            coordinatesCollections.add(Node(int(askInput[0]),int(askInput[1])))
    #asking for initial and final
    origin:str = input("")
    destiny:str = input("")
    #showing results
    print(Finder(coordinatesCollections:Set, origin, destiny).relatory())
    




