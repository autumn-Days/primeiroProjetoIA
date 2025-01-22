from finder import *

class DataGenerator():
    def generateData(self, is2GenerateNew50Coordinates:bool,is2GenerateNew20Coordinates:bool, file50Coordinates=None, file20Coordinates=None):
        """
        This class is responsible for testing all the methods and generating all the data for the report.
        It has 4 atributes, they are:

        1.is2GenerateNew50Coordinates : A flag that indicates whether or not to it is to generate random coordinates for the tests.
        If it is false, than it is expected the user of the class to give it a file by especifying the parameter "file50Coordinates"
        2.is2GenerateNew20Coordinates: This is a flag that indicates whether or not to create 20 random coordinates for testing the
        randomization of the neighbourhood for experiment 4. If it is false, than it is expected the user to give a file with 20 random
        coordinates by expecifying "file20Coordinates".

        -->All the files the coordinates used for the report are already in the folder of the project. Its names are "coordinates.txt"
        for the 50 coordinates and "20coordinates.txt" for the random coordinates.<--
        """
        
        randomCoordinates = []
        if is2GenerateNew50Coordinates:
            randomCoordinates = self.__generateRandomCoordinates()
        else:
            randomCoordinates = self.__readCoordinatesFromFile(file50Coordinates)
        finder = Finder()
        
        i = 0
        
        #this loop is responsible for generating all the data for experiments 1 to 3
        for coord in randomCoordinates:
            x1,y1,x2,y2 = coord
            finder.origin = (x1,y1)
            finder.destiny = (x2,y2)
            self.BFS_DFS_Data(finder,i)
            self.UCSData(finder,i)
            self.AstarData(finder,i)
            self.greedyData(finder,i)
            i += 1
        
        randomCoordinates = []

        if is2GenerateNew20Coordinates:
            randomCoordinates = self.__generateRandomCoordinates(amountCoordinates=20,file2beGeneratedName="random20coordinates.txt")
        else:
            randomCoordinates = self.__readCoordinatesFromFile(file20Coordinates)
        
        i = 0
        #generates the data for experiment 4
        for coord in randomCoordinates:
            x1,y1,x2,y2 = coord
            finder.origin = (x1,y1)
            finder.destiny = (x2,y2)
            self.randomizedNeighbourhoodData(finder,i)
            i += 1
    
    def randomizedNeighbourhoodData(self, finder:Finder,timesRunned:int):
        """
        It is responsible for generating the data related to experiment 4. Combines all the possibilities for function costs.
        """
        costs = ["C1","C2","C3","C4"]
        dataStrucutureMethods = ["popleft","pop"]
        for dataStructureMethod in dataStrucutureMethods:
            for cost in costs:
                openingType = self.__selectOpeningType2(timesRunned)
                fileName = ""
                if dataStructureMethod == "pop":
                    fileName = f"DFS_{timesRunned+1}_random_neighbourhood_{cost}.txt"
                elif dataStructureMethod == "popleft":
                    fileName = f"BFS_{timesRunned+1}_random_neighbourhood_{cost}.txt"
                for i in range (10):
                    with open(fileName,openingType) as file:
                        with contextlib.redirect_stdout(file):
                            print(f"-=-=-=-=-=-=-={i+1}°-=-=-=-=-=-=-=")
                            finder.runPathFiding("D_BFS",cost,is2shuffle=True,popingMethod=dataStructureMethod)
                            finder.resetSome()
        print("[Executando. O output está sendo salvo em arquivos na pasta do projeto. Isto deve levar em torno de 1min]")
                            
    def AstarData(self, finder:Finder, timesRunned):
        #Combines all the possibilities for cost functions and heuristics for the A*
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
        print("[Executando. O output está sendo salvo em arquivos na pasta do projeto. Isto deve levar em torno de 1min]")
            
    def BFS_DFS_Data(self,finder:Finder,timesRunned):
        #Combines all the possibilities for function costs for the BFS and the DFS
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
        print("[Executando. O output está sendo salvo em arquivos na pasta do projeto. Isto deve levar em torno de 1min]")
                
    def UCSData(self, finder:Finder,timesRunned):
        #combines all the costs for the UCS
        costs = ["C1","C2","C3","C4"]
        for cost in costs:
            openingType = self.__selectOpeningType2(timesRunned)
            with open(f"UCS_{cost}.txt", openingType) as file:
                with contextlib.redirect_stdout(file):
                    print(f"-=-=-=-=-=-=-={timesRunned+1}°-=-=-=-=-=-=-=")
                    finder.runPathFiding("UCS",cost,"None")#None é o valor da heurística, pois o UCS não é heurístico, logo, passando "None" a heurística é ignorada.
                    finder.resetSome()
        print("[Executando. O output está sendo salvo em arquivos na pasta do projeto. Isto deve levar em torno de 1min]")
                
    def greedyData(self, finder:Finder,timesRunned):
        #Combines all the possibilities for cost functions and heuristics for the A*
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
        print("[Executando. O output está sendo salvo em arquivos na pasta do projeto. Isto deve levar em torno de 1min]")
                        
    def __generateRandomCoordinates(self, amountCoordinates=50,file2beGeneratedName="random50Coordinates.txt"):
        """
        This method generates pseudo-random coordinates. The destination and the origin are never equal to one another
        and if the origin and the destination were already generated, it creates another one.
        """
        coordinates = []
        for i in range(amountCoordinates):
            
            while True:
                x1,y1,x2,y2 = (random.randint(0,30),random.randint(0,30),random.randint(0,30),random.randint(0,30))
                if ((x1,y1) == (x2,y2) or (x1,y1,x2,y2) in coordinates):               
                    continue
                coordinates.append((x1,y1,x2,y2))
                break
        
        with open(file2beGeneratedName,"w") as file:
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

    def __selectOpeningType2(self,timesRunned:int):
        if (timesRunned == 0):
            return "w"
        else:
            return "a"

def main():
    #para ler dos arquivos já existentes
    DataGenerator().generateData(is2GenerateNew50Coordinates=False, is2GenerateNew20Coordinates=False,file50Coordinates="coordinates.txt", file20Coordinates="20coordinates.txt")
    #para gerar coordernadas aleatórias para testar, basta descomentar a linha abaixo. e rodar o programa novamente
    #DataGenerator().generateData(is2GenerateNew50Coordinates=True, is2GenerateNew20Coordinates=True,file50Coordinates="coordinates.txt", file20Coordinates="20coordinates.txt")
if __name__ == "__main__":
    main()
