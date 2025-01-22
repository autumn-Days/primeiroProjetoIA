# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:35:07 2025

@author: Just_
"""

from typing import *
import math
import heapq
from collections import deque
import random
import contextlib #serve para redirecionar o output do terminal para um arquivo 

class Finder:
    def __init__(self, origin:Tuple[int,int]=None, destiny:Tuple[int, int]=None, gridProportion=30) -> None:
        #atributos relacionados às coordenadas
        self.origin = origin
        self.destiny = destiny
        #atributos relacionados às estatísticas
        self.amountNodesGenerated:int = 0
        #auxiliary atributs
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesExplored: List[Tuple[int,int]] = []
        self.__gridProportion = gridProportion

    def runPathFiding(self, pathFidingAlgo:str, costFun:str,heuristicFun:Callable=None,popingMethod=None, is2print=True,is2shuffle=False):
        """
        Este método é um wrapper para selecionar os algoritmos de busca. Ele recebe strings do mesmo nome dos métodos de busca e os invoca
        dinamicamente, juntamente como todos os parâmetros necessários. Esta estratégia foi adotada para facilitar a criação dos arquivos
        para a análise, pois basta que sejam criadas listas de strings relacionando os algoritmos, funções de custo, heurísticas, etc e 
        realizar todas as combinações possíveis em um 'for-ninhado'.

        Para utilizá-la, espera-se que seja passado o algoritmo de busca (Astar,greedy,D_BFS ou UCS), a função de custo (C1,C2,C3 ou C4) a heurística,
        caso seja aplicável, o método de remoção de elementos da fronteira dos algoritmos DFS ou BFS (caso aplicável) e se é desejado aplicar a randomização
        da vizinhança, caso seja desejado, basta especificar pondo "is2shuffle=True", caso não seja desejado, basta ignorar.

        Como o BFS e o DFS possuem praticamente o mesmo código, sendo que a única mudança de um para outro é que o primeiro implementa um fila
        e o segundo uma pilha, foi decidido que seria implementado apenas um código e o que iria definir se o código rodaria o BFS ou o DFS seria o
        método de remoção, ou seja, "popleft" para a fila e "pop" para pilha. Desta forma, para usar o DFS ou o BFS, basta especificar o parâmetro
        'popingMethod=<"popleft"|"pop">'. Além disso, o método responsável por implementar esses algoritmos se chama "D_BFS", justamente por causa
        da similaridade da implementação desess algoritmos.

        A main contêm exemplos de utilização desse método
        """
        pathFidingAlgo:Callable = getattr(self,pathFidingAlgo)
        if pathFidingAlgo.__name__ == "D_BFS":
            totalCost,path,pathCost,heuristicCost,isItHeuristic =  pathFidingAlgo(getattr(self,costFun,None), is2shuffle, popingMethod)
        else:
            totalCost,path,pathCost,heuristicCost,isItHeuristic =  pathFidingAlgo(getattr(self,costFun,None), is2shuffle, getattr(self,heuristicFun,None))
        if is2print:
            if not isItHeuristic:
                self.__showResult(totalCost,path)
            else:
                self.__showResult(totalCost,path,isItHeuristic,pathCost,heuristicCost)
        return (totalCost,path)
    
    def __showResult(self,totalCost:int,path:List[Tuple[str,int,str]],isItHeuristic:str=None,pathCost:int=None,heuristicCost:int=None) -> None:
        """
        Este é o método de impressão. Ele é responsável por imprimir as estatísticas e o caminho tomado pelo agente. 
        Ao final de cada estatística foi posto um símbolo que se relacionasse a ele. A única utilidade é desse símbolo
        é para a extração de dados após a análise.
        """
        
        if isItHeuristic :
            print(f"    Path cost from {path[0][0]} to {self.destiny}: {pathCost}◇    ")
        print(f"    Total cost from {path[0][0]} to {self.destiny} : {totalCost}•    ")
        print(f"    Visited from {path[0][0]} to {self.destiny} : {len(path)+1}●    ")
        print(f"    Generated from {path[0][0]} to {self.destiny} : {self.amountNodesGenerated}◦    ")

        for i in range(len(path)):
            print(f"{path[i][0]}-->{path[i][2]}")

    """
    Os próximos dois métodos dizem respeito aos algoritmos de busca heurísticos.
    
    A*:
        
    Cada nódulo (x,y) é representado pela tupla: 
                            `(f(n),(x,y),passos,g(n),h(n))`
    É útil guardar os valores de g(n) pois, desta forma, é possível comparar o
    custo total do caminho trilhado com os algoritmos de busca não informada.
    
    Por último, é essencial guardar o f(n) pois ele é o elemento que será usado
    pela heap mínima para selecionar o nódulo com o menor caminho entre o pai
    e o filho.
    
    Greedy:
        
    A estrutura do nódulo (x,y) do guloso é basicamente a mesma que a do A*, mas,
    como h(n) é valor que é usado para selecionar elementos da heap binária míni-
    ma.
                            `(h(n),(x,y),passos,g(n),f(n))`
    """

    def greedy(self, costFun:Callable,is2shuffle:bool, heuristic:Callable):
        """
        Mesmo que o algoritmo guloso não utilize o custo do caminho, `costFun`
        é passado como parâmetro para facilitar a comparação entre ele e os
        algoritmos de busca não informados, mas o único dado que é levado em consi-
        deração para fazer a remoção da heap binária mínima é o valor heurístico.
        """
        IT_IS_HEURISTIC = True
        
        frontier = [(0,self.origin,0,0,0)]
        """
        `mapi` é um mapa. Quando a implementação do algoritmo finaliza a sua execução, ele o retorna para que seja possível traçar
        o caminho que ele encontrou de (x1,y1) até (x2,y2)
        """
        mapi = {self.origin:(0,str(self.origin)+"'",0,0,0)} 

        while frontier:
            currentCost, currentNode, currentSteps,pathCost,totalCost = heapq.heappop(frontier)
            self.__nodesExplored.append(currentNode)
            if(currentNode == self.destiny):
                return (totalCost, self.__pathTaken(mapi,self.destiny),pathCost,currentCost,IT_IS_HEURISTIC)
            
            for neighbour in self.getNeighbours(currentNode,is2shuffle,"greedy"):
                self.amountNodesGenerated += 1
               
                heuristicNeighbour = heuristic(neighbour)
                costNeighbour = costFun(self.__isItVertical(currentNode, neighbour),currentSteps+1)
                
                neighbourTotalCost = totalCost + costNeighbour + heuristicNeighbour #Este valor é obtido somente para que seja possível compará-lo com o A*, ele não é considerado para fazer a remoção dos elementos da heap.   
                pathCostNeighbour = pathCost + costNeighbour#Útil para que se possa compará-lo com os algoritmso de busca não informada    
                
                heapq.heappush(frontier,(heuristicNeighbour,neighbour,currentSteps+1,pathCostNeighbour,neighbourTotalCost)) #o estado recém gerado é adicionado
                mapi[neighbour] = (heuristicNeighbour,currentNode,currentSteps+1,pathCostNeighbour,neighbourTotalCost)
    
    def Astar(self, costFunction:Callable, is2shuffle:bool, heuristicFun:Callable) -> Tuple[int,List[Tuple[str,int,str]]]:
        IT_IS_HEURISTIC = True
        
        frontier = [(0,self.origin,0,0,0)]#distance from parent, nextNode, steps taken to get from parent to nextNode
        mapi = {self.origin:(0,str(self.origin)+"'",0,0,0)} #da fonte para a fonte, a distância é 0

        while frontier:
            currentCost, currentNode, currentSteps,pathCost,heuristicCost = heapq.heappop(frontier)
            self.__nodesExplored.append(currentNode)
            if currentNode == self.destiny :
                return (mapi[self.destiny][0], self.__pathTaken(mapi,self.destiny),pathCost,heuristicCost,IT_IS_HEURISTIC)
            #relaxamento - (Terminologia usada em "Introdução a algoritmos", de Thomas Cormem et al.)
            neighbours = self.getNeighbours(currentNode,is2shuffle)
            for neighbour in neighbours:
                self.amountNodesGenerated += 1
                
                pathValue2neighbour = costFunction(self.__isItVertical(currentNode, neighbour),currentSteps+1)
                heuristicValue2neighbour = heuristicFun(neighbour)
                
                totalCost = currentCost + pathValue2neighbour + heuristicValue2neighbour
                newPathCost = pathCost + pathValue2neighbour
                newHeuristicCost = heuristicCost + heuristicValue2neighbour
                
                if ((neighbour not in mapi) or (totalCost < mapi[neighbour][0])):
                    heapq.heappush(frontier, (totalCost,neighbour,currentSteps+1,newPathCost,newHeuristicCost))
                    mapi[neighbour] = (totalCost,currentNode,currentSteps+1,newPathCost,newHeuristicCost)

    def D_BFS(self,costFun:Callable, is2shuffle:bool, popingMethod:str, heuristicFun=None) -> Tuple[int,List[Tuple[str,int,str]]]:
        """
        É possível salvar as informações ligadas aos dados para a análise na estrutura:
            
        (x_{filho}, y_{filho}) : (custo, (x_{pai}, y_{pai}}), passos).
        
        Quanto a fronteira, ela guardará elementos do tipo: (custo, (x_{filho, y_{filho}}), passos).

        Todas as implementações dos algortimos seguem uma variação dessa estrutura de dados.
        """
        
        frontier = deque()
        frontier.append((0,self.origin,0))
                     
        travelled = {self.origin: (0,str(self.origin)+"'",0)}       
        while frontier:
            currentCost, currentNode, currentSteps = getattr(frontier,popingMethod)() # chama o popleft/pop dinamicamente. Usa `pop` para pilha e `popleft` para fila
            
            self.__nodesExplored.append(currentNode)
            if currentNode == self.destiny:
                return (currentCost, self.__pathTaken(travelled,self.destiny),currentCost,None,None)
            #It adds the generated nodes into the frontier
            neighbours = self.getNeighbours(currentNode, is2shuffle, "DBFS")
            for neighbour in neighbours:
                self.amountNodesGenerated += 1
                #Para que o BFS não leve a eternidade para terminar
                if ((popingMethod == "popleft") and (neighbour in self.__nodesGenerated)):
                    continue
                newCost = currentCost + costFun(self.__isItVertical(currentNode,neighbour), currentSteps+1)
                frontier.append((newCost,neighbour,currentSteps+1))
                travelled[neighbour] = (newCost, currentNode, currentSteps+1)
                self.__nodesGenerated.append(neighbour)

                
    def UCS(self, costFunction:Callable, is2shuffle:bool, heuristicFun=None) -> Tuple[int,List[Tuple[str,int,str]]]:
        frontier = [(0,self.origin,0)]#distance from parent, child, steps taken to get from parent to child
        mapi = {self.origin:(0,str(self.origin)+"'",0)}
        while frontier:
            currentCost, currentNode, currentSteps = heapq.heappop(frontier)
            self.__nodesExplored.append(currentNode)
            if currentNode == self.destiny :
                """
                The total cost is returned along with the way from the source to the destination. It also 
                returns 3 None's only for a matter of compatibility with the other methods. Because, in the
                way the `runPathFiding` is implemented, it expects all the methods to return exactly the same
                number or arguments. If it receives None as argument for some of the elements of the tuple, it
                simplies ignores it. So, in essence, it just returns the parent of the destination along
                with the `mapi` the path taken from source to destination.
                """
                return (mapi[self.destiny][0], self.__pathTaken(mapi,self.destiny),None,None,None)
            #relaxamento
            neighbours = self.getNeighbours(currentNode,is2shuffle)
            for neighbour in neighbours:
                self.amountNodesGenerated += 1
                totalCost = currentCost + costFunction(self.__isItVertical(currentNode, neighbour),currentSteps+1)
                if ((neighbour not in mapi) or (totalCost < mapi[neighbour][0])):
                    heapq.heappush(frontier, (totalCost,neighbour,currentSteps+1))
                    mapi[neighbour] = (totalCost,currentNode,currentSteps+1)
                    
                
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
    """
    C1 e C2 recebem alguns argumentos mesmo que não utilizem todos
    por uma questão de compatibilidade entre o C3 e o C5, pois, como
    as funções de custo são chamadas em loop pela classe `Test` ao
    final e são chamadas dinamicamente, essa uniformidade facilita
    imensamente a implementação e diminui brutalmente o tempo de 
    implementação.
    """
    def C1(self, nothingImportant, nothingImportant2) -> None:
        return 10
    def C2(self, isVertical:bool, nothingImportant) -> None:
        if isVertical :
            return  10
        return 15
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
    def getNeighbours(self, currentNode, is2shuffle, algoName=None):
        """
        Este método é um wrapper para o método __getNeighbours. Ele recebe
        o estado atual e retorna os nós gerados. A flag `is2shuffle` é mar-
        cada com verdadeiro quando o se deseja gerar a vizinhança aleatoria-
        mente para o experimento 4. AlgoName é especificado somente quando 
        se trata do BFS ou do algoritmo guloso, pois eles são os 2 únicos
        algoritmos que não geram os filhos que já foram adicionados à fronteira.
        Por padrão, `algoName` recebe `None` que, em python, em interpretado
        como falso. 
        """
        if algoName:
            return self.__getNeighbours(currentNode, is2shuffle, algoName)
        return self.__getNeighbours(currentNode, is2shuffle)
    #Esse método é responsável por retornar a lista do caminho trilhado de origem até destino
    def __pathTaken(self, mapi, definitiveDestiny):
        pathTaken:List[Tuple[str,int,str]] = []
        
        parent = mapi[definitiveDestiny][1]
        changingDestiny = definitiveDestiny

        while True:
            pathTaken.append((mapi[changingDestiny][1],mapi[changingDestiny][0],changingDestiny))
            changingDestiny = parent
            parent = mapi[parent][1]
            if parent == str(self.origin)+"'":
                break
        
        pathTaken.reverse()
        return pathTaken

    def __getNeighbours(self,coord:Tuple[int,int],is2shuffle:bool,isItDBFS_or_greedy=None) -> List[Tuple[int,int]]:
        """
        Esse método é o responsável por gerar a vizinhança do nó recém-retirado da fronteira. 
        
        A variável `neighboursBeta` obtém elementos que podem ou não estar no espaço de busca, com (1,2) ou (31,4).
        Por causa dessa incerteza se os elementos contidos nela fazem ou não parte do espaço de busca ela é chamada de
        "beta".

        Conforme este método executa, ele retira todos os elementos que não pertencem ao espaço de busca
        """
        neighboursBeta = [self.__goLeft(coord), self.__goRight(coord), self.__goDown(coord), self.__goUp(coord)]
        
        #filter the invalid
        for i in range(len(neighboursBeta)):
            if (neighboursBeta[i][0] < 0 or neighboursBeta[i][0] > self.__gridProportion) or ((neighboursBeta[i][1] < 0 or neighboursBeta[i][1] > self.__gridProportion)):
                neighboursBeta[i] = None
        
        neighbours = []

        if isItDBFS_or_greedy:
            neighbours =  [node for node in neighboursBeta if ((node != None) and (not self.__wasItExplored(node)))] 
        else:
            neighbours = [node for node in neighboursBeta if (node != None)] 
        
        #Embaralha os elementos
        if is2shuffle:
            random.shuffle(neighbours)
        return neighbours

    #verifica se o estado recém-obtido da fronteira já foi explorado
    def __wasItExplored(self, coord:Tuple[int,int]):
        return coord in self.__nodesExplored
    def __isItVertical(self, currentNode:Tuple[int,int], neighbour:Tuple[int,int]):
        """
        As funções de custo C3 e C4 variam de custo se o estado a ser visitado 
        está ou não na vertical. Então este método auxiliar verifica isso.
        """
        return abs(currentNode[1] - neighbour[1]) > 0

    def resetAll(self):
        """
        Reset all the atributes associated with the class.
        """
        self.origin = None
        self.destiny = None
        self.resetSome()
        
    def resetSome(self):
        """
        Reset all the atributes except the origin and the destiny
        """
        self.__nodesGenerated:List[Tuple[int,int]] = []
        self.__nodesExplored: List[Tuple[int,int]] = []        
        self.amountNodesGenerated:int = 0
    


def main():   
    myFinder = Finder((0,0),(30,30)) 
    #A estrela custo C1, heurística euclidiana
    myFinder.runPathFiding("Astar", "C1", heuristicFun="euclidianHeuristic")
    myFinder.resetSome() # sempre é necessária resetar as estruturas de dados após cada teste.
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    #A estrela, custo C1, heurística manhatam
    myFinder.runPathFiding("Astar", "C1", heuristicFun="manhatamHeuristic")
    myFinder.resetSome()
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    #DFS com custo C1
    myFinder.runPathFiding("D_BFS", "C1", popingMethod="pop")
    myFinder.resetSome()
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    #BFS com custo C1
    myFinder.runPathFiding("D_BFS", "C1", popingMethod="popleft") 
    myFinder.resetSome()
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    #DFS com vizinhança aleatória
    myFinder.runPathFiding("D_BFS", "C1", popingMethod="pop", is2shuffle=True) 
    myFinder.resetSome()
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    #BFS com vizinhança aleatória
    myFinder.runPathFiding("D_BFS", "C1", popingMethod="popleft", is2shuffle=True) 
    myFinder.resetSome()
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    #greedy
    myFinder.runPathFiding("greedy", "C1", heuristicFun="euclidianHeuristic")
    myFinder.resetSome()
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

if __name__ == "__main__":
    main()
