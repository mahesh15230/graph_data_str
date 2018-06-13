# =============================================================================
# #There can't be any repitition in the names of root causes, RCSs, products
# #Tree has to converge for RCSs
# #The tool shows the worst case scenario probability only
# 
# class Node:
#     nodes = {}
#     graph = {}
#     
#     def __init__(self,nodeName,classname):
#         self.name = nodeName
#         self.incomingNeighbors = []
#         self.outgoingNeighbors = []
#         self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
#         self.isVisited = False
#         self.nodeweight = 1
#         Node.nodes[self.name] = self
#         Node.graph[self] = self.outgoingNeighbors
#         
#     def getweight(self,node):
#         if node in self.outgoingNeighbors:
#             return Edge.edgesToNode[getNodeName(node)].weight
#         elif node in self.incomingNeighbors:
#             return Edge.edgesFromNode[getNodeName(node)].weight
#         else:
#             print("Invalid Argument supplied")
#             
#     def reset(self):
#         self.isVisited = False
#         self.nodeweight = 0
#         
#     def bfs(self, toggle = None): # toggle == None is rootcause to products
#         s = self
#         q = []
#         if toggle == None:
#             if self.classname == 'rootcause':
#                 q.append(s)
#                 self.isVisited = True
#                 while len(q):
#                     s = q.pop(0)
#                     for i in s.outgoingNeighbors:
#                         if not i.isVisited:
#                             q.append(i)
#                             i.isVisited = True
#                             i.nodeweight *= Edge.edgesToNode[getNodeName(i)].weight
#                             if i.classname == 'product':
#                                 print("Outage occurence percentage for", i.name,"is ",100*i.nodeweight,"%")
#             else:
#                 print("Invalid rootcause")
#             for i in Node.nodes.values():
#                 i.reset()
#         else:
#             if self.classname == 'product':
#                 q.append(s)
#                 self.isVisited = True
#                 while len(q):
#                     s = q.pop(0)
#                     for i in s
# =============================================================================
#There can't be any repitition in the names of root causes, RCSs, products
#Tree has to converge for RCSs ?
#The tool shows the worst case scenario probability only

class Node:
    nodes = {}
    graph = {}
    
    def __init__(self,nodeName,classname):
        self.name = nodeName
        self.incomingNeighbors = []
        self.outgoingNeighbors = []
        self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
        self.isVisited = False
        self.nodeweight = 1
        Node.nodes[self.name] = self
        Node.graph[self] = self.outgoingNeighbors

            
    def resetnode(self):
        self.isVisited = False
        self.nodeweight = 0
        
    def bfs(self, toggle = None): # toggle == None is rootcause to products
        s = self
        q = []
        if toggle == None:
            #print("toggle is None...")
            if self.classname == 'rootcause':
                #print("classname is ROOTCAUSE")
                q.append(s)
                self.isVisited = True
                #print(self.name,"is source node")
                while len(q):
                    #print(len(q))
                    s = q.pop(0)
                    #print("Current source node is",s.name)
                    #print("Queue is dequeued")
                    for i in s.outgoingNeighbors:
                        if not i.isVisited:
                            q.append(i)
                            i.isVisited = True
                            #print(i.name,"is visited")
                            #print(i.nodeweight,"is pathweight so far")
                            #print("Upcoming node is",i.name,"weight to be multiplied is", Edge.edges[s.name+str(":")+i.name].weight)
                            i.nodeweight *= Edge.edges[s.name+str(":")+i.name].weight * s.nodeweight
                            #print("Pathweight so far is", i.nodeweight)
                            if i.classname == 'product':
                                print("Outage occurence percentage for", i.name,"is ",100*i.nodeweight,"%")
            else:
                print("Invalid rootcause")
            for i in Node.nodes.values():
                i.resetnode()
        else:
            if self.classname == 'product':
                #print("toggle ISN'T none")
                q.append(s)
                self.isVisited = True
                #print(self.name,"is source node")
                while len(q):
                    #print(len(q))
                    s = q.pop(0)
                    #print("Queue is dequeued")
                    for i in s.incomingNeighbors:
                        #print("inside for loop")
                        if not i.isVisited:
                            q.append(i)
                            i.isVisited = True
                            #print(i.name,"is visited")
                            #print(i.nodeweight,"is pathweight so far")
                            #print("Upcoming node is",i.name,"weight to be multiplied is", Edge.edges[i.name+str(":")+s.name].weight)
                            i.nodeweight *= Edge.edges[i.name+str(":")+s.name].weight * s.nodeweight
                            #print("Pathweight so far is", i.nodeweight)
                            if i.classname == 'rootcause':
                                print("Rootcauses that could causing the outage", i.name,"are ",100*i.nodeweight,"%")
            else:
                print("Invalid product")
            for i in Node.nodes.values():
                i.resetnode()


def addNode(nodeName,classname):
    nodeAdded = Node(nodeName,classname)
    
def resetNode(nodeName):
    Node.nodes[nodeName].isVisited = False
    Node.nodes[nodeName].nodeweight = 0

class Edge:
    edges = {}
    def __init__(self,fromNode,toNode,weight):
        if fromNode!=toNode:
            self.name = fromNode.name+str(":")+toNode.name
            self.weight = weight
            self.startNode = fromNode.name
            self.endNode = toNode.name
            Node.nodes[toNode.name].incomingNeighbors.append(Node.nodes[fromNode.name])
            Node.nodes[fromNode.name].outgoingNeighbors.append(Node.nodes[toNode.name])
            Edge.edges[self.name] = self

            
def addEdge(fromNode,toNode,weight):
    edgeAdded = Edge(fromNode,toNode,weight)

rootcauses = []
RCSs = []
products = []

class History:
    history = {}
    def __init__(self,label,rootcause,product,HLs = None): # HLs must be a list
        self.name = label
        self.rootcause = rootcause
        self.product = product
        self.hiddenLayer = HLs
        History.history[self.name] = self
# =============================================================================
# Debug rootcause to product
# Debug product to rootcause
# =============================================================================
addNode('a','rootcause')
addNode('b','rootcause')
addNode('c','rootcause')
addNode('d','HL')
addNode('e','HL')
addNode('f','HL')
addNode('g','HL')
addNode('h','HL')
addNode('i','product')
addNode('j','product')
addNode('k','product')
addNode('l','product')
addNode('a','rootcause')
addNode('b','rootcause')
addNode('c','rootcause')
addNode('d','HL')
addNode('e','HL')
addNode('f','HL')
addNode('g','HL')
addNode('h','HL')
addNode('i','product')
addNode('j','product')
addNode('k','product')
addNode('l','product')
addEdge(Node.nodes['a'],Node.nodes['f'],.69)
addEdge(Node.nodes['a'],Node.nodes['d'],1)
addEdge(Node.nodes['a'],Node.nodes['e'],.6)
addEdge(Node.nodes['b'],Node.nodes['d'],.8)
addEdge(Node.nodes['b'],Node.nodes['e'],.67)
addEdge(Node.nodes['c'],Node.nodes['d'],.72)
addEdge(Node.nodes['c'],Node.nodes['e'],.39)
addEdge(Node.nodes['d'],Node.nodes['f'],.5)
addEdge(Node.nodes['d'],Node.nodes['g'],.9)
addEdge(Node.nodes['d'],Node.nodes['h'],1)
addEdge(Node.nodes['e'],Node.nodes['g'],.8)
addEdge(Node.nodes['e'],Node.nodes['h'],.76)
addEdge(Node.nodes['f'],Node.nodes['i'],.26)
addEdge(Node.nodes['f'],Node.nodes['j'],1)
addEdge(Node.nodes['g'],Node.nodes['j'],.81)
addEdge(Node.nodes['g'],Node.nodes['k'],.62)
addEdge(Node.nodes['g'],Node.nodes['l'],.43)
addEdge(Node.nodes['h'],Node.nodes['j'],.97)
addEdge(Node.nodes['h'],Node.nodes['k'],1)
addEdge(Node.nodes['h'],Node.nodes['l'],.68)
# =============================================================================
print(Node.nodes['a'].bfs())
print(Node.nodes['j'].bfs(toggle=1))
#.incomingNeighbors:
#                         if not i.isVisited:
#                             q.append(i)
#                             i.isVisited = True
#                             i.nodeweight *= Edge.edgesFromNode[getNodeName(i)].weight
#                             if i.classname == 'product':
#                                 print("Outage occurence percentage for", i.name,"is ",100*i.nodeweight,"%")
#             else:
#                 print("Invalid product")
#             for i in Node.nodes.values():
#                 i.reset()
# 
# def getNodeName(node):
#     lKey = [key for key, value in Node.nodes.items() if value == node][0]
#     return lKey
# 
# def addNode(nodeName,classname):
#     nodeAdded = Node(nodeName,classname)
#     
# def resetNode(nodeName):
#     Node.nodes[nodeName].isVisited = False
#     Node.nodes[nodeName].nodeweight = 0
# 
# 
#     
# # =============================================================================
# # def setClassName(nodename,classname):
# #     Node.nodes[nodename].classname = classname
# # =============================================================================
#     
# class Edge:
#     edgesFromNode = {}
#     edgesToNode = {}
#     def __init__(self,fromNode,toNode,weight):
#         if fromNode!=toNode:
#             self.weight = weight
#             self.startNode = fromNode.name
#             self.endNode = toNode.name
#             Node.nodes[toNode.name].incomingNeighbors.append(Node.nodes[fromNode.name])
#             Node.nodes[fromNode.name].outgoingNeighbors.append(Node.nodes[toNode.name])
#             Edge.edgesFromNode[self.startNode] = self
#             Edge.edgesToNode[self.endNode] = self
#             
# def addEdge(fromNode,toNode,weight):
#     edgeAdded = Edge(fromNode,toNode,weight)
# 
# rootcauses = []
# RCSs = []
# products = []
# 
# #A function that asks the user for no of +ve incidents of one thing affecting the other and the -ve incidents affecting the other
# #Find a good way for the user to add conditional probabilities as it gets tedious if the root causes increase.
# #Write another code that records history that's compatible with this code
# #i.e, (Root cause) --> (HL1) --> ... --> (RCS) --> (Product)
# # Basically create a data structure for each incident in history from which conditional probabilities can be calculated.
# #This data structure must be dynamic as root causes, HLs, RCSs and products can be removed and/or added.
# 
# class History:
#     history = {}
#     def __init__(self,label,rootcause,product):
#         self.name = label
#         self.rootcause = rootcause
#         self.product = product
#         self.hiddenLayer = []
#         History.history[self.name] = self
# 
# def recordHistory(label,rootcause,product,HLs): #HLs must be a list.
#     histrec = History(label,rootcause,product)
#     try:
#         histrec.hiddenLayer += list(HLs)
#         History.history[label] = histrec
#         print("Event recorded successfully")
#     except:
#         print("Hidden layers must be passed as a list only")
# 
# addNode('a','rootcause')
# addNode('b','rootcause')
# addNode('c','rootcause')
# addNode('d','HL')
# addNode('e','HL')
# addNode('f','product')
# addNode('g','product')
# addNode('h','product')
# addNode('i','product')
# 
# =============================================================================
