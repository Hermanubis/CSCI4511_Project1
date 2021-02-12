import numpy as np
import time
import math
# keep track of program excution time
start_time = time.time()
class Graph:
    def __init__(self):
        self.dictionary = dict()
    
    def add_edge(self, From, To, dist=0):
        # add edge between two vertices with correct distance, 
        # both direction are added since it's undirected
        self.dictionary.setdefault(From, {})[To] = dist
        self.dictionary.setdefault(To, {})[From] = dist

    def neighbor(self, node1, node2=None):
        # find vertices connected to the current vertex
        paths = self.dictionary.setdefault(node1, {})
        if node2 != None:
            return paths.get(node2)
        return paths
    
class vertex:
    def __init__(self, vertexID:int, previous:int):
        self.vertexID = vertexID
        self.previous = previous # parent vertex
        self.g = 0 
        self.h = 0 
        self.f = 0 

    def __eq__(self, other):
        return self.vertexID == other.vertexID

    def __lt__(self, other):
        # defines < for sorting
        return self.f < other.f

def a_star(graph, heuristics, source, destination):
    
    openList = []
    closedList = []
    path = [] # to keep track of the path
   
    start = vertex(source, None)
    end = vertex(destination, None)

    openList.append(start)
    
    # while openlist is not empty
    while len(openList) > 0:
        
        openList.sort() # sort list to prioritize the vertex with lowest cost
        curr_vertex = openList.pop(0)
        closedList.append(curr_vertex)
        
        # destination reached
        if curr_vertex == end:
            # add to path from destination to source
            if curr_vertex != start:
                path.append('ID:' + str(curr_vertex.vertexID) + ' | Distance=' + str(curr_vertex.g))
                curr_vertex = curr_vertex.previous
            while curr_vertex != start:
                path.append('ID:' + str(curr_vertex.vertexID))
                curr_vertex = curr_vertex.previous
            path.append('ID:' + str(start.vertexID))
            return path[::-1] # return path in the correct sequence

        neighbors = graph.neighbor(curr_vertex.vertexID)
        for key, value in neighbors.items(): # for all neighbors
            node = vertex(key, curr_vertex)
            if(node in closedList): # if already in closed list
                continue
            
            # calculate the correct h, g, and f score
            node.h = heuristics.get(node.vertexID) #estimated distance to goal
            node.g = curr_vertex.g + graph.neighbor(curr_vertex.vertexID, node.vertexID) # distance from start
            node.f = node.g + node.h
           
            check = 1
            for i in openList:
                if (node == i and node.f > i.f):
                    check = 0
                    break
            if check == 1:
                openList.append(node)
            # do not add vertex to openlist if lower cost one already exist

    return -1

# Main
if __name__ == "__main__":
    
    myfile = open("p1_graph.txt", "r+")
    txtLines = myfile.readlines()
    # remove commented lines
    txtLines[:] = [x for x in txtLines if not x.startswith('#')]
    
    square = []
    edges = []
    src = 0
    dest = 0
    for lines in txtLines:
        
        # format lines from txt
        lines = lines.rstrip()
        lines = lines.strip("\n")
        lines = lines.split(",")
        
        if len(lines) == 2:
            # located source and dest
            if lines[0] == 'S':
                src = int(lines[1])
            elif lines[0] == 'D':
                dest = int(lines[1])
            else: #in the format of Vertex ID, Square ID
                square.append(int(lines[1]))
             
        elif len(lines) == 3:
            # in the format of From, To, Distance
            for i in range(len(lines)):
                lines[i] = int(lines[i])
            edges.append(lines)
    
    graph = Graph()
    heuristic = {}
    
    #  heuristic is the distance to the destination square
    for i in range(len(square)):
        temp1 = abs((square[dest] // 10)*100 - (square[i] // 10)*100)
        temp2 = abs((square[dest] % 10) *100 - (square[i] % 10) *100)
        heuristic[i] = math.sqrt(temp1 ** 2 + temp2 ** 2)
    
    # add edges to graph
    for i in range(len(edges)):
        graph.add_edge(edges[i][0], edges[i][1], edges[i][2])

    shortestPath = a_star(graph, heuristic, src, dest)
    if shortestPath != -1:
        print(shortestPath)
    print("Execution Time: %.10s seconds" % (time.time() - start_time))