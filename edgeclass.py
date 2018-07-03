from nodeclass import *

class Edge:
    edges = {}
    edge_id = {}
    def __init__(self,id,fromNode,toNode,weight,name=None): # Except for weight and id everything else is a string
        if name == None:    
            if fromNode!=toNode:
                self.id = len(Edge.edges)
                self.name = fromNode+":"+toNode
                self.weight = weight
                self.startNode = fromNode
                self.endNode = toNode
                Node.nodes[toNode].incomingNeighbors.append(fromNode)
                Node.nodes[fromNode].outgoingNeighbors.append(toNode)
                Edge.edges[self.name] = self
                Edge.edges[self.id] = self
            else:
                print("Error : Edge can't be created")
        else:
            if fromNode!=toNode:
                self.id = len(Edge.edges)
                self.name = name
                self.weight = weight
                self.startNode = fromNode
                self.endNode = toNode
                Node.nodes[toNode].incomingNeighbors.append(fromNode)
                Node.nodes[fromNode].outgoingNeighbors.append(toNode)
                Edge.edges[self.name] = self
                Edge.edges[self.id] = self
            else:
                print("Error : Edge can't be created")
    
    def get_id(self,toNode=None,fromNode=None):
        a = []
        if toNode == None and fromNode == None:
            return self.id
        elif toNode == None and fromNode != None:
            for i in Edge.edges.keys():
                if fromNode+':' in i:
                    a.append(Edge.edges[i].id)
            return a
        else:
            for i in Edge.edges.keys():
                if ":"+toNode in i:
                    a.append(Edge.edges[i].id)
            return a
