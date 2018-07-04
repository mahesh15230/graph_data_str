from edgeclass import *
import string
import random

def randgen():
    lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
    str = "".join(lst)
    return str

class Node:
    nodes = {}
    node_id = {}
    def __init__(self,nodeName,classname,id=None,incneigh=None,outneigh=None):
        self.name = nodeName
        self.id = randgen()
        self.incomingNeighbors = [] # List of strings
        self.outgoingNeighbors = [] # List of strings
        self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
        self.isVisited = False
        self.nodeweight = 1
        Node.nodes[self.name] = self
        Node.node_id[self.id] = self
            
    def resetnode(self):
        self.isVisited = False
        self.nodeweight = 0
        
    def bfs(self, toggle = None): # toggle == None is rootcause to products
        s = self.name
        q = []
        string1 = ''
        if toggle == None:
            if self.classname == 'rootcause':
                q.append(s)
                self.isVisited = True
                while len(q):
                    s = q.pop(0)
                    for i in Node.nodes[s].outgoingNeighbors:
                        if not Node.nodes[i].isVisited:
                            q.append(i)
                            Node.nodes[i].isVisited = True
                            Node.nodes[i].nodeweight *= Edge.edges[s+":"+i].weight * Node.nodes[s].nodeweight
                            if Node.nodes[i].classname == 'product':
                                textout = "Outage occurence probability for %s is %f" %(i, Node.nodes[i].nodeweight)
                                string1 += textout + '\n'
            else:
                textout1 = "Invalid rootcause"
            for i in Node.nodes.values():
                i.resetnode()
        else:
            if self.classname == 'product':
                q.append(s)
                self.isVisited = True
                while len(q):
                    s = q.pop(0)
                    for i in Node.nodes[s].incomingNeighbors:
                        if not Node.nodes[i].isVisited:
                            q.append(i)
                            Node.nodes[i].isVisited = True
                            Node.nodes[i].nodeweight *= Edge.edges[i+":"+s].weight * Node.nodes[s].nodeweight
                            if Node.nodes[i].classname == 'rootcause':
                                textout2 = "Rootcause %s could result in an outage with probability %f" %(i, Node.nodes[i].nodeweight)
                                string1 += textout2 + '\n'
            else:
                textout3 = "Invalid product"
            for i in Node.nodes.values():
                i.resetnode()
