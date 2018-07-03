from nodeclass import *
import string
import random

def randgen():
    lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
    str = "".join(lst)
    return str

class Edge:
    edges = {}
    edge_id = {}
    def __init__(self,fromNode,toNode,weight,id=None):   
        if id == None:    
            if fromNode!=toNode:
                self.id = randgen()
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
                self.id = id
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
    
#     def get_id(self,toNode=None,fromNode=None):
#         a = []
#         if toNode == None and fromNode == None:
#             return self.id
#         elif toNode == None and fromNode != None:
#             for i in Edge.edges.keys():
#                 if fromNode+':' in i:
#                     a.append(Edge.edges[i].id)
#             return a
#         else:
#             for i in Edge.edges.keys():
#                 if ":"+toNode in i:
#                     a.append(Edge.edges[i].id)
#             return a
