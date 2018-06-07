#There can't be any repitition in the names of root causes, RCSs, products
#Tree has to converge for RCSs

import random as rnd

class Node:
    nodes = {}
    graph = {}
    
    def __init__(self,nodeName):
        self.name = nodeName
        self.incomingNeighbors = []
        self.outgoingNeighbors = []
        self.classname = None
        Node.nodes[self.name] = self
        Node.graph[self] = self.outgoingNeighbors
        
    def getweight(self,node):
        if node in self.outgoingNeighbors:
            print("Outgoing")
            return Edge.edgesFromNode[getNodeName(node)].weight
        elif node in self.incomingNeighbors:
            print("Incoming")
            print(getNodeName(node))
            return Edge.edgesToNode[getNodeName(node)].weight
        else:
            print("Invalid Argument supplied")

    #Below def workf only if the tree strictly diverges
    def pathweightf(self, toNode, toggle = None): #toNode can only be products
        node = toNode
        pathweight = 1
        if toggle != None:
            (self.incomingNeighbors,self.outgoingNeighbors) = (self.outgoingNeighbors,self.incomingNeighbors)
            if not len(node.incomingNeighbors):    
                while node!=self:
                    pathweight *= Edge.edgesToNode[node].weight
                    node = node.incomingNeighbors[0]
                return pathweight
            else:
                print("Multiple causes can't affect a single entity")
            (self.outgoingNeighbors,self.incomingNeighbors) = (self.incomingNeighbors,self.outgoingNeighbors)
        else:
            if not len(node.incomingNeighbors):    
                while node!=self:
                    pathweight *= Edge.edgesToNode[node].weight
                    node = node.incomingNeighbors[0]
                return pathweight
            else:
                print("Multiple causes can't affect a single entity")
        
# =============================================================================
#     def pathweightr(self,fromNode): #fromNode can only be rootcause
#         (self.incomingNeighbors,self.outgoingNeighbors) = (self.outgoingNeighbors,self.incomingNeighbors)
#         self.pathweightf(fromNode)
#         (self.outgoingNeighbors,self.incomingNeighbors) = (self.incomingNeighbors,self.outgoingNeighbors)
# =============================================================================
        
# =============================================================================
#     def maxgetweight(self,toggle = None, direction = 1): #toggle==None returns max weight
#         pathweight = 0                    #toggle!=None returns the node with the max weight
#         node = None
#         if direction:
#             for i in self.outgoingNeighbors:
#                 if self.getweight(i) >= pathweight:
#                     pathweight = self.getweight(i)
#                     node = i
#             if toggle == None:
#                 return pathweight
#             else:
#                 return node
#         else:
# =============================================================================
            
# =============================================================================
#     def maxpathWeight(self, toNode):
#          pathweight = 1
#          startnode = self.......................................
#          while startnode!=toNode:
#              pathweight *= startnode.maxgetweight()
#              startnode = startnode.maxgetweight(1)
#          return pathweight
#      def pathWeightr(self,fromNodes):
#          pathweight = 1
#          startNode = self
#          while 
# =============================================================================

def getNodeName(node):
    lKey = [key for key, value in Node.nodes.items() if value == node][0]
    return lKey

def addNode(nodeName):
    nodeAdded = Node(nodeName)
    
class Edge:
    edgesFromNode = {}
    edgesToNode = {}
    def __init__(self,fromNode,toNode,weight):
        if fromNode!=toNode:
            self.weight = weight
            self.startNode = fromNode.name
            self.endNode = toNode.name
            Node.nodes[toNode.name].incomingNeighbors.append(Node.nodes[fromNode.name])
            Node.nodes[fromNode.name].outgoingNeighbors.append(Node.nodes[toNode.name])
            Edge.edgesFromNode[self.startNode] = self
            Edge.edgesToNode[self.endNode] = self
            
def addEdge(fromNode,toNode,weight):
    edgeAdded = Edge(fromNode,toNode,weight)

rootcauses = []
RCSs = []
products = []

#A function that asks the user for no of +ve incidents of one thing affecting the other and the -ve incidents affecting the other
#Find a good way for the user to add conditional probabilities as it gets tedious if the root causes increase.
#Write another code that records history that's compatible with this code
#i.e, (Root cause) --> (HL1) --> ... --> (RCS) --> (Product)
# Basically create a data structure for each incident in history from which conditional probabilities can be calculated.
#This data structure must be dynamic as root causes, HLs, RCSs and products can be removed and/or added.

class history:
    history = {}
    def __init__(self,label,rootcause,product):
        self.name = label
        self.rootcause = rootcause
        self.product = product
        self.hiddenLayer = []
        history[self.name] = self

def recordHistory(label,rootcause,product,HLs): #HLs must be a list.
    histrec = history(label,rootcause,product)
    try:
        histrec.hiddenLayer += HLs
        print("Event recorded successfully")
    except:
        print("Hidden layers must be passed as a list only")



def rctop(rootcause):
    weightlist = []
    j=0
    for i in products:
        weightlist.append(Node.nodes[rootcause].pathweightf(i))
        print(i," outage probability is ",weightlist[j])
        j+=1
        
def ptorc(product):
    weightlist=[]
    j=0
    for i in rootcauses:
        weightlist.append(Node.nodes[product].pathweightf(j,1))
        j+=1
        
addNode('WFN')
addNode('EZLM')
addNode('HRB')
addNode('Memory usage')
addNode('Mainframe')
addNode('Unresponsive server')
addNode('Server')
addEdge(Node.nodes["Mainframe"],Node.nodes["WFN"],1)
addEdge(Node.nodes["Mainframe"],Node.nodes["EZLM"],1)
addEdge(Node.nodes["Mainframe"],Node.nodes["HRB"],1)
addEdge(Node.nodes["Memory usage"],Node.nodes["WFN"],1)
addEdge(Node.nodes["Memory usage"],Node.nodes["EZLM"],1)
addEdge(Node.nodes["Memory usage"],Node.nodes["HRB"],1)
addEdge(Node.nodes["Unresponsive server"],Node.nodes["Server"],.8)
addEdge(Node.nodes["Server"],Node.nodes["WFN"],1)
addEdge(Node.nodes["Server"],Node.nodes["EZLM"],1)
addEdge(Node.nodes["Server"],Node.nodes["HRB"],1)

print(Edge.edgesFromNode)
print(Edge.edgesToNode)
print(Edge.edgesFromNode['Mainframe'].weight)
# =============================================================================
# print(Node.nodes)
# print(Edge.edgesFromNode)
# print(Edge.edgesToNode)
# =============================================================================
print(Node.nodes['WFN'].getweight(Node.nodes["Mainframe"]))












