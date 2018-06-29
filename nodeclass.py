class Node:
    nodes = {}
    node_id = {}
    def __init__(self,nodeName,classname,incneigh=None,outneigh=None,id=None):
        self.name = nodeName
        self.id = len(Node.nodes)
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
                                print("Outage occurence percentage for", i,"is ",100*Node.nodes[i].nodeweight,"%")
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
                    for i in Node.nodes[s].incomingNeighbors:
                        if not Node.nodes[i].isVisited:
                            q.append(i)
                            Node.nodes[i].isVisited = True
                            Node.nodes[i].nodeweight *= Edge.edges[i+":"+s].weight * Node.nodes[s].nodeweight
                            if Node.nodes[i].classname == 'rootcause':
                                print("Rootcauses that could causing the outage", i,"are ",100*Node.nodes[i].nodeweight,"%")
            else:
                print("Invalid product")
            for i in Node.nodes.values():
                i.resetnode()