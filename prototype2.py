# =============================================================================
# Author : Mahesh Chandra Yayi
# Filename : prototype2.py
# 
# (C) Copyright 2018 ADP Pvt. Ltd.
# ALL RIGHTS RESERVED
# 
# =============================================================================

import matplotlib.pyplot as plt

class Node:
    nodes = {}
    node_id = {}
    def __init__(self,nodeName,classname):
        self.name = nodeName
        self.id = len(Node.nodes)
        self.incomingNeighbors = []
        self.outgoingNeighbors = []
        self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
        self.isVisited = False
        self.nodeweight = 1
        Node.nodes[self.name] = self
        Node.node_id[self.id] = self
        
            
    def resetnode(self):
        self.isVisited = False
        self.nodeweight = 0
        
    def bfs(self, toggle = None): # toggle == None is rootcause to products
        s = self
        q = []
        if toggle == None:
            if self.classname == 'rootcause':
                q.append(s)
                self.isVisited = True
                while len(q):
                    s = q.pop(0)
                    for i in s.outgoingNeighbors:
                        if not i.isVisited:
                            q.append(i)
                            i.isVisited = True
                            i.nodeweight *= Edge.edges[s.name+str(":")+i.name].weight * s.nodeweight
                            if i.classname == 'product':
                                print("Outage occurence percentage for", i.name,"is ",100*i.nodeweight,"%")
            else:
                print("Invalid rootcause")
            for i in Node.nodes.values():
                i.resetnode()
        else:
            if self.classname == 'product':
                q.append(s)
                self.isVisited = True
                while len(q):
                    s = q.pop(0)
                    for i in s.incomingNeighbors:
                        if not i.isVisited:
                            q.append(i)
                            i.isVisited = True
                            i.nodeweight *= Edge.edges[i.name+str(":")+s.name].weight * s.nodeweight
                            if i.classname == 'rootcause':
                                print("Rootcauses that could causing the outage", i.name,"are ",100*i.nodeweight,"%")
            else:
                print("Invalid product")
            for i in Node.nodes.values():
                i.resetnode()


def addNode(nodeName,classname):
    nodeAdded = Node(nodeName,classname)
    
def delNode(nodeName):
    for i in Edge.edges.keys():
        if nodeName+":" in i:
            Edge.edges[None] = Edge.edges.pop(nodeName)
            Edge.edges[i].startNode = None
        elif ":"+nodeName in i:
            Edge.edges[None] = Edge.edges.pop(nodeName)
            Edge.edges[i].endNode = None
    del Node.nodes[nodeName]
    print(nodeName,"is deleted")
    
def delEdge(fromNodename, toNodename):
    del Edge.edges[fromNodename+":"+toNodename]
    print("Edge is deleted")
    
class Edge:
    edges = {}
    edge_id = {}
    def __init__(self,fromNode,toNode,weight):
        if fromNode!=toNode:
            self.id = len(Edge.edges)
            self.name = fromNode.name+str(":")+toNode.name
            self.weight = weight
            self.startNode = fromNode.name
            self.endNode = toNode.name
            Node.nodes[toNode.name].incomingNeighbors.append(Node.nodes[fromNode.name])
            Node.nodes[fromNode.name].outgoingNeighbors.append(Node.nodes[toNode.name])
            Edge.edges[self.name] = self
            Edge.edges[self.id] = self
            
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
        
        
        
        
        