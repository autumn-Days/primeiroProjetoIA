# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:35:07 2025

@author: Just_
"""

from typing import *
import math
import heapq
from collections import deque
from random import randint
import contextlib #serve para redirecionar o output do terminal para um arquivo
import os #biblioteca usada para verificar se um arquivo já está no diretório do projeto

class Finder:
    def __init__(self, origin:Tuple[int,int]=None, destiny:Tuple[int, int]=None, gridProportion=30) -> None:
        #atributes for the coordinates
        self.origin = origin
        self.destiny = destiny
        #atributes for statistics
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
        #cost related atributes
        self.totalCost = 0
        #auxiliary atributs
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesVisited: List[Tuple[int,int]] = []
        self.__gridProportion = gridProportion
    #return (currentCost, self.__pathTaken(visited,self.destiny),pathCost,currentCost)
    def runPathFiding(self, pathFidingAlgo:str, costFun:str,heuristicFun:Callable=None,popingMethod=None, is2print=True):
        pathFidingAlgo:Callable = getattr(self,pathFidingAlgo)
        if pathFidingAlgo.__name__ == "D_BFS":
            totalCost,path,pathCost,heuristicCost,isItHeuristic =  pathFidingAlgo(getattr(self,costFun,None), popingMethod)
        else:
            totalCost,path,pathCost,heuristicCost,isItHeuristic =  pathFidingAlgo(getattr(self,costFun,None), getattr(self,heuristicFun,None))
        if is2print:
            if not isItHeuristic:
                self.__showResult(totalCost,path)
            else:
                self.__showResult(totalCost,path,isItHeuristic,pathCost,heuristicCost)
        return (totalCost,path)
    
    def __showResult(self,totalCost:int,path:List[Tuple[str,int,str]],isItHeuristic:str=None,pathCost:int=None,heuristicCost:int=None,is2printCost=False) -> None:
        if isItHeuristic :
            print(f"Path cost from {path[0][0]} to {self.destiny}: {pathCost}")
            #print(f"Heuristic cost from {path[0][0]} to {self.destiny}: {heuristicCost}")
        print(f"Total cost from {path[0][0]} to {self.destiny} : {totalCost}")
        print(f"Visited from {path[0][0]} to {self.destiny} : {len(path)+1}") #"Um" é subtraido já que dá origem para ela própria se leva 0 passos
        print(f"Generated from {path[0][0]} to {self.destiny} : {self.amountNodesGenerated}")

        if (is2printCost):
            for i in range(len(path)):
                print(f"{path[i][0]}--({path[i][1]})-->{path[i][2]}")
                
        else:
            for i in range(len(path)):
                print(f"{path[i][0]}-->{path[i][2]}")
    """
    Os próximos dois métodos dizem respeito aos algoritmos de busca heurísticos.
    
    A*:
        
    Cada nódulo (x,y) é representado pela estrutura: 
                            `(f(n),(x,y),passos,g(n),h(n))`
    É útil guardar os valores de g(n) pois, desta forma, é possível comparar o
    custo total do caminho trilhado com os algoritmos de busca não informada.
    
    De forma semelhante, também é útil guardar h(n), pois desta forma é possível
    obter o custo heurístico total ao final, o que útil para comparar o A* com 
    o guloso posteriormente.
    
    Por último, é essencial guardar o f(n) pois ele é o elemento que será usado
    pela heap mínima para selecionar o nódulo com o menor caminho entre o pai
    e o filho.
    
    Greedy:
        
    A estrutura do nódulo (x,y) do guloso é basicamente a mesma que a do A*, mas,
    como f(n) = h(n), omitisse o útlimo elemento da tupla. Assim, a sua estrutura
    é:
                            `(f(n),(x,y),passos,g(n))`
                            `(h(n),(x,y),passos,g(n),f(n))`
    """

    def greedy(self, costFun:Callable, heuristic:Callable):
        """
        Mesmo que o algoritmo guloso não utilize o custo do caminho, `costFun`
        é passado como parâmetro para facilitar a comparação entre ele e os
        algoritmos de busca não informados.
        """
        IT_IS_HEURISTIC = True
        
        queue = [(0,self.origin,0,0,0)]
        visited = {self.origin:(0,str(self.origin)+"'",0,0,0)}

        while queue:
            currentCost, currentNode, currentSteps,pathCost,totalCost = heapq.heappop(queue)
            self.__nodesVisited.append(currentNode) #depois eu tenho que me lembrar de pôr isso antes da condição. Isso daqui explica pq eu não tive que subtrair 1 da quantidade de passos na função `pathTaken` para excluir a origem 
            if(currentNode == self.destiny):
                #totalCost,path,pathCost,heuristicCost,isItHeuristic
                return (totalCost, self.__pathTaken(visited,self.destiny),pathCost,currentCost,IT_IS_HEURISTIC)#f(n) = g(n), por isso currentCost é passado 2 vezes
            for neighbour in self.__getNeighbours(currentNode,"greedy"):
                self.amountNodesGenerated += 1
               
                heuristicNeighbour = heuristic(neighbour)
                costNeighbour = costFun(self.__isItVertical(currentNode, neighbour),currentSteps+1)
                
                neighbourTotalCost = totalCost + costNeighbour + heuristicNeighbour #só serve para comparar com o A*   
                pathCostNeighbour = pathCost + costNeighbour# O custo do path em sí, sem comtar a heurítics    
                
                heapq.heappush(queue,(heuristicNeighbour,neighbour,currentSteps+1,pathCostNeighbour,neighbourTotalCost))
                visited[neighbour] = (heuristicNeighbour,currentNode,currentSteps+1,pathCostNeighbour,neighbourTotalCost)
                
                #self.__nodesGenerated.append(neighbour) #comentei essa linha, dps vejo se era importante
    def Astar(self, costFunction:Callable, heuristicFun:Callable) -> Tuple[int,List[Tuple[str,int,str]]]:
        IT_IS_HEURISTIC = True
        

        priorityQueue = [(0,self.origin,0,0,0)]#distance from parent, nextNode, steps taken to get from parent to nextNode
        visited = {self.origin:(0,str(self.origin)+"'",0,0,0)} #da fonte para a fonte, a distância é 0
        #stepsTaken = 0
        while priorityQueue:
            currentCost, currentNode, currentSteps,pathCost,heuristicCost = heapq.heappop(priorityQueue)
            self.__nodesVisited.append(currentNode)#acho que o certo era gerado, dps eu mudo. Tbm acho que poderia ser posto antes do if, dps vejo se dá certo
            if currentNode == self.destiny :
                #The total cost is returned along with the way from the source to the destination
                #totalCost,path,pathCost,heuristicCost,isItHeuristic
                return (visited[self.destiny][0], self.__pathTaken(visited,self.destiny),pathCost,heuristicCost,IT_IS_HEURISTIC)
            #relaxamento
            neighbours = self.__getNeighbours(currentNode)
            for neighbour in neighbours:
                self.amountNodesGenerated += 1
                
                pathValue2neighbour = costFunction(self.__isItVertical(currentNode, neighbour),currentSteps+1)
                heuristicValue2neighbour = heuristicFun(neighbour)
                
                totalCost = currentCost + pathValue2neighbour + heuristicValue2neighbour
                newPathCost = pathCost + pathValue2neighbour
                newHeuristicCost = heuristicCost + heuristicValue2neighbour
                
                if ((neighbour not in visited) or (totalCost < visited[neighbour][0])):
                    heapq.heappush(priorityQueue, (totalCost,neighbour,currentSteps+1,newPathCost,newHeuristicCost))
                    visited[neighbour] = (totalCost,currentNode,currentSteps+1,newPathCost,newHeuristicCost)

    def D_BFS(self,costFun:Callable,popingMethod:str,heuristicFun=None) -> Tuple[int,List[Tuple[str,int,str]]]:
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
        
        i = 0
        
        queue = deque()
        queue.append((0,self.origin,0))
                     
        travelled = {self.origin: (0,str(self.origin)+"'",0)}       
        while queue:
            currentCost, currentNode, currentSteps = getattr(queue,popingMethod)() #usa `pop` para pilha e `popleft` para fila
            
            self.__nodesVisited.append(currentNode)
            if currentNode == self.destiny:
                return (currentCost, self.__pathTaken(travelled,self.destiny),currentCost,None,None)
            #It adds the generated nodes into the queue
            neighbours = self.__getNeighbours(currentNode,"DBFS")
            for neighbour in neighbours:
                self.amountNodesGenerated += 1
                #para que o DFS não entre em loop infinito e para que o BFS poupe tempo de processamento
                if ((popingMethod == "popleft") and (neighbour in self.__nodesGenerated)):
                    continue
                newCost = currentCost + costFun(self.__isItVertical(currentNode,neighbour), currentSteps+1)
                queue.append((newCost,neighbour,currentSteps+1))
                travelled[neighbour] = (newCost, currentNode, currentSteps+1)
                self.__nodesGenerated.append(neighbour)
            i +=1


                
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
            self.__nodesVisited.append(currentNode)#acho que o certo era gerado, dps eu mudo. Tbm acho que poderia ser posto antes do if, dps vejo se dá certo
            if currentNode == self.destiny :
                #The total cost is returned along with the way from the source to the destination
                return (visited[self.destiny][0], self.__pathTaken(visited,self.destiny),None,None,None)
            #relaxamento
            neighbours = self.__getNeighbours(currentNode)
            for neighbour in neighbours:
                self.amountNodesGenerated += 1
                totalCost = currentCost + costFunction(self.__isItVertical(currentNode, neighbour),currentSteps+1)
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
        return 10 + (abs(5-amountSteps)%6)
    def C4(self, isVertical:bool, amountSteps) -> None:
        if isVertical:
            return 10
        return 5 + (abs(10-amountSteps)%11)

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
#
    def __getNeighbours(self,coord:Tuple[int,int],isItDBFS_or_greedy=None) -> List[Tuple[int,int]]:
        neighboursBeta = [self.__goLeft(coord), self.__goRight(coord), self.__goDown(coord), self.__goUp(coord)]
        #filter the invalid
        for i in range(len(neighboursBeta)):
            if (neighboursBeta[i][0] < 0 or neighboursBeta[i][0] > self.__gridProportion) or ((neighboursBeta[i][1] < 0 or neighboursBeta[i][1] > self.__gridProportion)):
                neighboursBeta[i] = None
        if isItDBFS_or_greedy:
            return [node for node in neighboursBeta if ((node != None) and (not self.__wasItVisited(node)))] # existe a possibilidade da lista retornada estar vazia
        else:
            return [node for node in neighboursBeta if (node != None)] # existe a possibilidade da lista retornada estar vazia


    def __wasItVisited(self, coord:Tuple[int,int]):
        return coord in self.__nodesVisited

    def __isItVertical(self, currentNode:Tuple[int,int], neighbour:Tuple[int,int]):
        return abs(currentNode[1] - neighbour[1]) > 0

    """
        #atributes for the coordinates
        self.origin = origin
        self.destiny = destiny
        #atributes for statistics
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
        #cost related atributes
        self.totalCost = 0
        #auxiliary atributs
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesVisited: List[Tuple[int,int]] = []
        self.__gridProportion = gridProportion
    """

    def resetAll(self):
        self.origin = None
        self.destiny = None
        self.resetSome()
        
    def resetSome(self):
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesVisited: List[Tuple[int,int]] = []        
        self.totalCost = 0
        self.totalSteps = 0
        self.amountNodesGenerated:int = 0
        self.amountNodesVisited:int = 0
    
class Test():
    def generateData(self, is2GenerateNewCoordinates:bool, fileCoordinates=None):
        randomCoordinates = []
        if is2GenerateNewCoordinates:
            randomCoordinates = self.__generateRandomCoordinates()
        else:
            randomCoordinates = self.__readCoordinatesFromFile(fileCoordinates)
        finder = Finder()
        
        i = 0
        
        for coord in randomCoordinates:
            x1,y1,x2,y2 = coord
            finder.origin = (x1,y1)
            finder.destiny = (x2,y2)
            self.BFS_DFS_Data(finder,i)
            self.UCSData(finder,i)
            self.AstarData(finder,i)
            self.greedyData(finder,i) #tô resolvendo umas coisas com esse ainda
            i += 1
            
    def AstarData(self, finder:Finder, timesRunned):
        heuristics = ["euclidianHeuristic","manhatamHeuristic"]
        costs = ["C1","C2","C3","C4"]

        for heuristic in heuristics:
            for cost in costs:
                openingType = self.__selectOpeningType2(timesRunned)
                with open(f"Astar_{cost}_{heuristic}.txt",openingType) as file:    
                    with contextlib.redirect_stdout(file):
                        print(f"-=-=-=-=-=-=-={timesRunned+1}°-=-=-=-=-=-=-=")
                        finder.runPathFiding("Astar",cost,heuristic)
                        finder.resetSome()
        print("ok")
            
    def BFS_DFS_Data(self,finder:Finder,timesRunned):
        dataStrucutureMethods = ["popleft","pop"]
        costs = ["C1","C2","C3","C4"]

        for dataStructureMethod in dataStrucutureMethods:
            for cost in costs:
                openingType = self.__selectOpeningType2(timesRunned)
                
                fileName = ""
                if dataStructureMethod == "pop":
                    fileName = f"DFS_{cost}.txt"
                elif dataStructureMethod == "popleft":
                    fileName = f"BFS_{cost}.txt"
                
                with open(fileName,openingType) as file:
                    with contextlib.redirect_stdout(file):
                            print(f"-=-=-=-=-=-=-={timesRunned+1}°-=-=-=-=-=-=-=")
                            finder.runPathFiding("D_BFS",cost,popingMethod=dataStructureMethod)
                            finder.resetSome()
        print("ufa")
                
    def UCSData(self, finder:Finder,timesRunned):
        costs = ["C1","C2","C3","C4"]
        for cost in costs:
            openingType = self.__selectOpeningType2(timesRunned)
            with open(f"UCS_{cost}.txt", openingType) as file:
                with contextlib.redirect_stdout(file):
                    print(f"-=-=-=-=-=-=-={timesRunned+1}°-=-=-=-=-=-=-=")
                    finder.runPathFiding("UCS",cost,"None")#None é o valor da heurística
                    finder.resetSome()
        print("aff")
                
    def greedyData(self, finder:Finder,timesRunned):
        heuristics = ["euclidianHeuristic","manhatamHeuristic"]
        costs = ["C1","C2","C3","C4"]

        for heuristic in heuristics:
            for cost in costs:
                openingType = self.__selectOpeningType2(timesRunned)
                with open(f"greedy_{heuristic}_{cost}.txt",openingType) as file:
                    with contextlib.redirect_stdout(file):
                        print(f"-=-=-=-=-=-=-={timesRunned+1}°-=-=-=-=-=-=-=")
                        finder.runPathFiding("greedy",cost,heuristic)
                        finder.resetSome()
        print("oi")
                        
    def __generateRandomCoordinates(self):
        coordinates = []
        for i in range(50):
            
            while True:
                x1,y1,x2,y2 = (randint(0,30),randint(0,30),randint(0,30),randint(0,30))
                if ((x1,y1) == (x2,y2) or (x1,y1,x2,y2) in coordinates):               
                    continue
                coordinates.append((x1,y1,x2,y2))
                break
        
        with open("randomCoordinates.txt","w") as file:
            for coord in coordinates:
                file.write(f"{coord[0]} {coord[1]} {coord[2]} {coord[3]}\n")
        return coordinates


    def __readCoordinatesFromFile(self, file):
        allCoordinates = []
        with open(file,"r") as file:
            for line in file:
                if line != "\n":
                    coordinates = tuple(map(int,line.strip().split())) #coordinates = (x1,y1,x2,y2)
                    allCoordinates.append(coordinates)
        return allCoordinates

    def __selectOpeningType(self,fileName):
        if (os.path.isfile(fileName)):
            return "w"
        else:
            return "a"

    def __selectOpeningType2(self,timesRunned:int):
        if (timesRunned == 0):
            return "w"
        else:
            return "a"

def main():
    
    #b = Finder((0,0),(30,30),gridProportion=30)
    
    #b.runPathFiding("D_BFS", "C1", popingMethod="pop")
    #b.runPathFiding("Astar", "C1", "euclidianHeuristic")
    #b.runPathFiding("UCS", "C1")
    
    c = Test()
    c.generateData(is2GenerateNewCoordinates=False,fileCoordinates = "coordinates.txt")
    
    
    #finder.runPathFiding("D_BFS",cost,popingMethod=dataStructure)

    #a,c = b.runPathFiding("D_BFS", "C1",popingMethod="popleft")
    #a,c = b.runPathFid
    #b.runPathFiding(pathFidingAlgo, costFun)
    
    
    #a.generateData(is2GenerateNewCoordinates=False,fileCoordinates="coordinates.txt")
    #try:
    #    a = Finder((8,7),(30,30), gridProportion=30)
    #   a.runPathFiding("D_BFS", "C2", popingMethod="popleft")
    #except:
    #    print("oi")
    
    #a = Finder((21,12),(2,7),gridProportion=30)
    #try:
    #    b,c = a.runPathFiding("UCS","C1","manhatamHeuristic")
    #    #b,c = a.BFS("C1")
        #print(" ")
    #except TypeError:
    #    print("deu ruim")
    #a.tester()
if __name__ == "__main__":
    main()

"""
O código tá praticamente pronto. Só falta fazer os seguintes testes/revisões e ajustes antes de fazer o relatório

OK
1. Se o loop está salvando os outputs dentro dos arquivos certos

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
ok
2. Testar se a sobreescrição dos arquivos está funcionando, ou seja, se quando "i" == 0 o programa usa o método
de overwrite ao invés do append (que é usado quando i != 0)

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
ok
3. Fazer com que o get neighbours só verifique se o nódulo está na lista de visitados quando o BFS/DFS for chamado

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
ok
4. Analisar o porquê do DFS estar com esse comportamento estranho
    - Acho que é pq o DFS precisa que eu tire aquela condição do "se o nó já tiver sido gerado, pule"
        -Não era isso não, tá certo assim msm
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Ok
5. Analisar porque o guloso tá com aqueles custos heurísticos estranhos entre de um nó para outro

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    OK
6. Gerar as funções de movimento na ordem que o Samy quer de acordo com o documento dele
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    OK
7. verificar se o cálculo das heurísticas está certa
    -Calcula na mão cada uma dessas coordenadas e depois confere:
        (21,6) (7,4)
            -Euclidiana:
                -meu: 140
                -retornado: 140
            -Manhatam:
                -meu:160
                -retornado:160
                    
        (12,15) (19,9)
            -Euclidiana:
                -meu: 90
                -ret: 90
            -Manhatam:
                -meu:130        
                -retornado:130
                
        (11,17) (27,27)
            -Euclidiana:
                -meu: 180
                -ret: 180
            -Manhatam:
                -meu: 260
                -retornado: 260
                    
        (5,11) (4,23):            
            -Euclidiana:
                -meu:120
                -ret:120
            -Manhatam:
                -meu: 130
                -retornado:130

        (13,22) (7,21):
            -Euclidiana:
                -meu:60
                -ret:60
            -Manhatam:
                -meu: 70
                -retornado: 70
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
OK
- 8. Testar as funções de custo  
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=            
OK
8. Revisar e analisar melhor se as coordenadas aleatórias estão sendo postas no x1,y1 e no x2,y2 como o esperado.

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Já revisei demais, deve tá certo

9. Revisar cada algoritmo principalmente para ver se os argumentos que eles estão passando para os métodos auxiliares
está certo mesmo.
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Coisas bobas a implementar:  
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
OK
1. Salvar nos arquivos tbm a quantidade de nós gerados
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
OK
2. Também por no arquivo quais os nódulos que foram visitados (pra isso é só mudar `steps` para `visitados` e tirar aquele -1)
    ATENÇÃO: DEPOIS QUE VOCÊ IMPLEMENTAR O 1&2 NÃO SE ESQUEÇA DE ATUALIZAR O RESET E O RESETSOME 
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

3. Implementar a randomização da vizinhaça
4. Implementar as bobagens do teste 5
"""
