from typing import *
import math
import heapq

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
        self.totalSteps = 0
        #auxiliary atributs
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesVisited: List[Tuple[int,int]] = []
        self.__gridProportion = gridProportion
    #algorithms self, costFun:Callable[None], is2print=True) -> Tuple[int,List[Tuple[str,int,str]]]
    def uniformCost(self, costFun, is2print=True):
        try:
            if costFun.__name__ == 'self.C1':
                #totalCost,path:List[Tuple[int,int]] =  self.__uniformCostC1()
                a =  self.__uniformCostC1()
                if is2print:
                    self.__showResult(totalCost,path)
                return (totalCost,path)
            elif costFun.__name__ == 'self.C2':
                return self.__uniformCostC2()
            elif costFun.__name__ == 'self.C3':
                return self.__uniformCostC3()
            else:
                return self.__uniformCostC4()
        except:
            print("oi")
    def __showResult(self,totalCost:int,path:List[Tuple[str,int,str]]) -> None:
        print(f"{path[0][0]} -> {path[0][2]} : {totalCost}")

        for i in len(path):
            print(f"{path[i][0]}->{path[i][1]}->{path[i][2]}")
            if i != len(path)-1:
                print(" --> ")

    def uniformCostC1(self) -> Tuple[int,List[Tuple[str,int,str]]]:
#        In the way uniform cost search is implementend it depends upon a priority queue
#        for choosing among the adjacents with the minimum path and a dictionary for repre-
#        senting the map. 
        
#        At the beggining, it may seem like they represent the exact same thing and that
#        the only data structure needed is the dictionary that represent the map, but this
#        is an erronous notion because the algorithm needs a way to be able to store the
#        adjacents nodes of the current node.

#        For this, the way found was storing them in the priority queue.

#        If we were using the traditional Dijkstra, visited would be of the type
#        dict[str,List[Tuple[int,str]]], but since this is the UCS the type is of 
#        dict[str,Tuple[int,str]]. This happen because of two reasons:

#        1. In this variation only the relaxed neighbours are appended into the priority
#        Queue
#        2. The cost between the `current` and `adj` is stored in the `adj`, not in the 
#        `current`, so, when adding elements in the `visited`, this does not generates
#        repeated keys.   
        priorityQueue = [(0,self.origin)]
        visited = {self.origin:(0,str(self.origin)+"'")} #da fonte para a fonte, a distância é 0

        while priorityQueue:
            currentCost, currentNode = heapq.heappop(priorityQueue)
            if currentNode == self.destiny :
                #The total cost is returned along with the way from the source to the destination
                return (currentCost+self.C1(), self.__pathTaken(visited,self.destiny))
            self.__nodesVisited.append(currentNode)
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

    def greedySearch(self, costFun, heuristicFun):#self, costFun:Callable[None], heuristicFun:Callable[Tuple[int,int]]):
        #somente se costFun.__name__ == C3 || == C4 então self.totalSteps setá incrementado
        pass
    #methods related to moviment
    def __goDown(self, position:Tuple[int,int]) -> Tuple[int,int]:
        return (position[0], position[1]-1)
    def __goUp(self, position) -> Tuple[int,int]:
            return (position[0], position[1]+1)
    def __goRight(self, position) -> Tuple[int,int]:
            return (position[0]+1, position[1])
    def __goLeft(self, position) -> Tuple[int,int]:
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
    def __wasItVisited(self, coord:Tuple[int,int]):
        return coord in self.__nodesVisited

def main():
    a = Finder((2,1),(0,0),gridProportion=2)
    print((a.uniformCostC1())[1])
    
if __name__ == "__main__":
    main()

"""
casos de testes
(0,0) -> (3,3)
"""


