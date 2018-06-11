#There can't be any repitition in the names of root causes, RCSs, products
#Tree has to converge for RCSs
#The tool shows the worst case scenario probability only

class Queue:
    def __init__(self):
        self.items = []
        
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

q = Queue()

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
        
    def getweight(self,node):
        if node in self.outgoingNeighbors:
            return Edge.edgesToNode[getNodeName(node)].weight
        elif node in self.incomingNeighbors:
            return Edge.edgesFromNode[getNodeName(node)].weight
        else:
            print("Invalid Argument supplied")
            
    def reset(self):
        self.isVisited = False
        self.nodeweight = 0
        
    def bfs(self):
        if self.classname == 'rootcause':
            q.enqueue(self)
            self.isVisited = True
            while not q.isEmpty():
                q.dequeue()
                for i in self.outgoingNeighbors:
                    if not i.isVisited:
                        q.enqueue(i)
                        i.isVisited = True
                        i.nodeweight *= Edge.edgesToNode[getNodeName(i)].weight
                        if i.classname == 'product':
                            print(i.name," Outage occurence percentage is ",100*i.nodeweight)
        else:
            print("Invalid rootcause")

def getNodeName(node):
    lKey = [key for key, value in Node.nodes.items() if value == node][0]
    return lKey

def addNode(nodeName):
    nodeAdded = Node(nodeName)
    
def resetNode(nodeName):
    Node.nodes[nodeName].isVisited = False
    Node.nodes[nodeName].nodeweight = 0


    
# =============================================================================
# def setClassName(nodename,classname):
#     Node.nodes[nodename].classname = classname
# =============================================================================
    
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

class History:
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
        histrec.hiddenLayer += list(HLs)
        History.history[label] = histrec
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
        












