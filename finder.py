from typing import *
import math
import heapq

class Finder:
    def __init__(self, nodeCollection:Set[Node], origin:Tuple[int,int], destiny:Tuple[int, int], gridProportion=30) -> None:
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
        #auxiliary atributs
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__gridProportion = gridProportion
    #algorithms
    def uniformCost(self, costFun:function) -> List[Tuple[int,int]]: #aka Dijkstra
        if costFun.__name__ == 'self.C1':
            return self.__uniformCostC1()
        elif costFun.__name__ == 'self.C2':
            return self.__uniformCostC2()
        elif costFun.__name__ == 'self.C3':
            return self.__uniformCostC3()
        else:
            return self.__uniformCostC4()

    def __uniformCostC1(self) -> Tuple[int,List[Tuple[str,int,str]]]:
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
        priorityQueue = [(0,self.origin)]
        visited = {self.origin:(0,str(self.origin)+"'")} #da fonte para a fonte, a distância é 0

        while priorityQueue:
            currentCost:int, currentNode:str = heapq.heappop(priorityQueue)
            if currentNode == destiny :
                #The total cost is returned along with the way from the source to the destination
                return (currentCost+self.C1(), self.__pathTaken(visited,destiny))
            self.__nodesGenerated.append(currentNode)
            #relaxamento
            for neighbour in self.__getNeighbours(currentNode):
                totalCost = currentCost + self.C1()
                if ((neighbour not in visited) or (totalCost < visited[neighbour][0])):
                    heapq.heappush(priorityQueue, (totalCost,neighbour))
                    visited[neighbour] = (totalCost,currentNode)
                    self.totalSteps += 1

    def __pathTaken(self, minSpanningTree:Dict[str,Tuple[int,str]], definitiveDestiny:str):
        pathTaken:List[Tuple[str,int,str]] = []
        
        parent:str = minSpanningTree[definitiveDestiny][1]
        changningDestiny:str = definitiveDestiny

        while parent != str(self.origin)+"'":
            pathTaken.append((changingDestiny,minSpanningTree[changingDestiny][0]),minSpanningTree[changingDestiny][1])
            parent = minSpanningTree[changingDestiny][1]
            changiningDestiny = parent
        return pathTaken.reverse()
        
    def __getNeighbours(self,coord:Tuple[int,int]) -> List[Tuple[int,int]]:
        neighboursBeta = [self.__goDown(coord), self.__goUp(coord), self.__goRight(coord), self.__goLeft(coord)]
        #filter the invalid
        for i in range(len(neighboursBeta)):
            if (neighboursBeta[i][0] < 0 or neighboursBeta[i][0] > self.__gridProportion) or ((neighboursBeta[i][1] < 0 or neighboursBeta[i][1] > self.__gridProportion)):
                neighboursBeta[i] = None
        return [node for node in neighboursBeta ((node != None) and (not self.__wasItGenerated(node)))] # existe a possibilidade da lista retornada estar vazia

    def greedySearch(sefl, costFun:function, heuristicFun:function):
        #somente se costFun.__name__ == C3 || == C4 então self.totalSteps setá incrementado
        pass
    #methods related to moviment
    def __goDown(self, position:Tuple[int,int]) -> Tuple[int,int]:
        return (position[0], position[1]-1)
    def __goUp(self) -> Tuple[int,int]:
            return (position[0], position[1]+1)
    def __goRight(self) -> Tuple[int,int]:
            return (position[0]+1, position[1])
    def __goLeft(self) -> Tuple[int,int]:
            return (position[0]-1, position[0])

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
    def __wasItGenerated(self, coord:Tuple[int,int]):
        return coord in self.__nodesGenerated
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
    




