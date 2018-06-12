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
            print("toggle is None...")
            if self.classname == 'rootcause':
                print("classname is ROOTCAUSE")
                q.append(s)
                self.isVisited = True
                print(self.name,"is source node")
                while len(q):
                    #print(len(q))
                    s = q.pop(0)
                    print("Queue is dequeued")
                    for i in s.outgoingNeighbors:
                        if not i.isVisited:
                            q.append(i)
                            i.isVisited = True
                            print(i.name,"is visited")
                            print(i.nodeweight,"is pathweight so far")
                            print("Upcoming node is",i.name,"weight to be multiplied is", Edge.edges[s.name+str(":")+i.name].weight)
                            i.nodeweight *= Edge.edges[s.name+str(":")+i.name].weight
                            print("Pathweight so far is", i.nodeweight)
                            if i.classname == 'product':
                                print("Outage occurence percentage for", i.name,"is ",100*i.nodeweight,"%")
            else:
                print("Invalid rootcause")
            for i in Node.nodes.values():
                i.resetnode()
        else:
            if self.classname == 'product':
                print("toggle ISN'T none")
                q.append(s)
                self.isVisited = True
                print(self.name,"is source node")
                while len(q):
                    #print(len(q))
                    s = q.pop(0)
                    print("Queue is dequeued")
                    for i in self.incomingNeighbors:
                        print("inside for loop")
                        if not i.isVisited:
                            q.append(i)
                            i.isVisited = True
                            print(i.name,"is visited")
                            print(i.nodeweight,"is pathweight so far")
                            print("Upcoming node is",i.name,"weight to be multiplied is", Edge.edges[i.name+str(":")+s.name].weight)
                            i.nodeweight *= Edge.edges[i.name+str(":")+s.name].weight
                            print("Pathweight so far is", i.nodeweight)
                            if i.classname == 'product':
                                print("Outage occurence percentage for", i.name,"is ",100*i.nodeweight,"%")
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

addNode('a','rootcause')
addNode('b','rootcause')
addNode('c','rootcause')
addNode('d','HL')
addNode('e','HL')
addNode('f','product')
addNode('g','product')
addNode('h','product')
addNode('i','product')
addEdge(Node.nodes['a'],Node.nodes['f'],1)
addEdge(Node.nodes['a'],Node.nodes['d'],.3)
addEdge(Node.nodes['b'],Node.nodes['d'],1)
addEdge(Node.nodes['b'],Node.nodes['e'],.68)
addEdge(Node.nodes['d'],Node.nodes['f'],.98)
addEdge(Node.nodes['d'],Node.nodes['g'],.76)
addEdge(Node.nodes['d'],Node.nodes['e'],.9)
addEdge(Node.nodes['c'],Node.nodes['e'],.5)
addEdge(Node.nodes['e'],Node.nodes['h'],.6)
addEdge(Node.nodes['e'],Node.nodes['i'],.7)
addEdge(Node.nodes['c'],Node.nodes['i'],.4)
# =============================================================================
print(Node.nodes['a'].bfs())