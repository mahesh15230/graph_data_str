# Author : Mahesh Chandra Yayi
# Filename : prototype2.py
# 
# (C) Copyright 2018 ADP Pvt. Ltd.
# ALL RIGHTS RESERVED
# 
# =============================================================================

import matplotlib.pyplot as plt

import sqlite3



conn = sqlite3.connect('projectv2')

cur= conn.cursor()

cur.execute('select * from History')
for row in cur:
    (hn,hrc,hp,hhis) = row    


def update_edge():
    cur.execute('select * from Edge')
    for row in cur:
        (ei,en,es,ee) = row


def update_node():
    cur.execute('select * from Node')
    for row in cur:
        (ni,nn,cn,nw) = row


update_edge()
update_node()



conn.create_function("md5",0,update_node)
conn.create_function("md6",0,update_edge)
cur.execute('CREATE TRIGGER IF NOT EXISTS node_trigger AFTER INSERT on Node BEGIN select md5();END;')
cur.execute('CREATE TRIGGER IF NOT EXISTS node_trigger AFTER UPDATE on Node BEGIN select md5();END;')
cur.execute('CREATE TRIGGER IF NOT EXISTS node_trigger AFTER DELETE on Node BEGIN select md5();END;')
cur.execute('CREATE TRIGGER IF NOT EXISTS node_trigger AFTER INSERT on Edge BEGIN select md5();END;')
cur.execute('CREATE TRIGGER IF NOT EXISTS node_trigger AFTER UPDATE on Edge BEGIN select md5();END;')
cur.execute('CREATE TRIGGER IF NOT EXISTS node_trigger AFTER DELETE on Edge BEGIN select md5();END;')



class Node:
    nodes = {}
    dict_id = {}
    def __init__(self,nodeName,classname):#working#insert the incoming and Outgoing Neighbours List and then Decomment the Sql code at the end
        self.name = nodeName
        self.id = len(Node.nodes)
        self.incomingNeighbors = []
        self.outgoingNeighbors = []
        self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
        self.isVisited = False
        self.nodeweight = 1
        Node.nodes[self.name] = self
        Node.dict_id[self.id] = self
        # executing  SQL query using execute() method.
        cur.execute('insert into Node(node_id,node_name,class_name,node_weight) values(?,?,?,1)',(self.id,nodeName,classname,))
        conn.commit()
        for index in self.incomingNeighbors:
            cur.execute('insert into Node_incoming values(?,?)',(self.id,self.incomingNeighbors[index].name))
            conn.commit()
        for index in self.outgoingNeighbors:
            cur.execute('insert into Node_outgoing values(?,?)',(self.id,self.outgoingNeighbors[index].name))
            conn.commit()
            
    def resetnode(self): #checking not possible ,pls check using bfs
        self.isVisited = False
        self.nodeweight = 0
        cur.execute('update Node set node_weight = ? where node_name = ?',(0,self.name))
        conn.commit()

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
                            i.nodeweight *= Edge.edges[s.name+str(':')+i.name].weight * s.nodeweight
                            if i.classname == 'product':
                                print('Outage occurence percentage for', i.name,'is ',100*i.nodeweight,'%')
            else:
                print('Invalid rootcause')
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
                            i.nodeweight *= Edge.edges[i.name+str(':')+s.name].weight * s.nodeweight
                            if i.classname == 'rootcause':
                                print('Rootcauses that could causing the outage', i.name,'are ',100*i.nodeweight,'%')
            else:
                print('Invalid product')
            for i in Node.nodes.values():
                i.resetnode()


def addNode(nodeName,classname): #working
    nodeAdded = Node(nodeName,classname)
    
def delNode(nodeName):#working
    for i in Edge.edges.keys():
        if nodeName+':' in i:
            Edge.edges[None] = Edge.edges.pop(nodeName)
            Edge.edges[i].startNode = None
        elif ':'+nodeName in i:
            Edge.edges[None] = Edge.edges.pop(nodeName)
            Edge.edges[i].endNode = None
    del Node.nodes[nodeName]
    print(nodeName,'is deleted')
    cur.execute('delete from Node where node_name = ?',nodeName)
    conn.commit()

    
def delEdge(fromNodename, toNodename):
    #check this line,The Sql Part is working fine.
    #del Edge.edges[fromNodename+str(':')+toNodename]
    print('Edge is deleted')
    cur.execute('delete from Edge where edge_start = (?) and edge_end = (?)',(fromNodename,toNodename))
    conn.commit()

class Edge:
    edges = {}
    def __init__(self,fromNode,toNode,weight):#working
        if fromNode!=toNode:
            self.name = fromNode.name+str(':')+toNode.name
            self.weight = weight
            self.startNode = fromNode.name
            self.endNode = toNode.name
            Node.nodes[toNode.name].incomingNeighbors.append(Node.nodes[fromNode.name])
            Node.nodes[fromNode.name].outgoingNeighbors.append(Node.nodes[toNode.name])
            Edge.edges[self.name] = self
            cur.execute('insert into Edge values (?,?,?,?,?)',(len(Edge.edges),self.name,self.startNode,self.endNode,self.weight))
            conn.commit()
            
def addEdge(fromNode,toNode,weight):#working
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
        #here,i assumed HLs to be a list, So i coded likewise
        for index in self.hiddenLayer:
            cur.execute('insert into History(his_name,his_root_cause,his_product,his_hid) values(?,?,?,?)',(self.name,self.rootcause,self.product,self.hiddenLayer[index]))
            conn.commit()

#Updating from Previous Databse as Soon as Code Runs




        
           

# =============================================================================
