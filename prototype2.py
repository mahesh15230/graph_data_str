'''class Predictor:
    def __init__(self,rootCause,RCS,product):
        self.rootcause = Node(rootCause)
        self.hls = []
        self.rcs = Node(RCS)
        self.product = Node(product)
    def addDL(rootcause,dlname,weight): #Make the func so that rootcause is a list and all the stuff in the list can be connected to the node dlname.
        #also, make sure the function works if "weights" argument is a list
        for i in rootcause:'''
            



import random as rnd
root_causes = []
root_symbols = []
products = []
class Node:
    nodes = {}
    graph = {}
    def __init__(self,nodeName):
        self.name = nodeName
        self.status = False #True : The node event occurs. False : otherwise
        self.incomingNeighbors = []
        self.outgoingNeighbors = []
        Node.nodes[self.name] = self
        Node.graph[self] = self.outgoingNeighbors
    def getweight(self,nextnode):
         if nextnode in self.outgoingNeighbors:
             return Edge.edges[self.startNode].weight
         else:
             print("Invalid Argument supplied")
     def maxgetweight(self,toggle = None): #toggle==None returns max weight
         pathweight = 0                    #toggle!=None returns the node with the max weight
         node = None
         for i in self.outgoingNeighbors:
             if self.getweight(i) >= pathweight:
                 pathweight = self.getweight(i)
                 node = i
         if toggle == None:
             return pathweight
         else:
             return i
     def pathweight(self, toNode):
         pathweight = 1
         startnode = self
         while startnode!=toNode:
             pathweight *= startnode.maxgetweight()
             startnode = startnode.maxgetweight(1)
         return pathweight

def addNode(nodeName):
    nodeAdded = Node(nodeName)
class Edge:
    edges = {}
    def __init__(self,fromNode,toNode,weight):
        if fromNode!=toNode:
            self.weight = weight
            self.startNode = fromNode
            self.endNode = toNode
            Node.nodes[toNode].incomingNeighbors.append(Node.nodes[fromNode])
            Node.nodes[fromNode].outgoingNeighbors.append(Node.nodes[toNode])
            Edge.edges[self.startNode] = self
    
            
def addEdge(fromNode,toNode,weight):
    edgeAdded = Edge(fromNode,toNode,weight)
'''class Predictor:
    def __init__(self,root_causes, Product = None):
        self.rootCauses = root_causes
        self.rootCauseAnalysis = None
        self.rootCauseSymbol = None
        self.product = Product
    def''' 
#def pathweight(fromNode,toNode):
addNode('a')
print(Node.nodes)
print("Node a Incoming : ",Node.nodes['a'].incomingNeighbors,"outgoing : ",Node.nodes['a'].outgoingNeighbors)
addNode("b")
addNode("g")
addNode("f")
addNode("e")
addNode("d")
addNode("c")
addEdge('a','c',rnd.random())
addEdge('a','d',rnd.random())
addEdge('a','e',rnd.random())
addEdge('b','c',rnd.random())
addEdge('b','d',rnd.random())
addEdge('b','e',rnd.random())
addEdge('c','f',rnd.random())
addEdge('c','g',rnd.random())
addEdge('d','f',rnd.random())
addEdge('d','g',rnd.random())
addEdge('e','f',rnd.random())
addEdge('e','g',rnd.random())
print(Node.nodes['a'].outgoingNeighbors)
