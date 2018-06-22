# =============================================================================
# Author : Mahesh Chandra Yayi
# Filename : prototype2.py
# 
# (C) Copyright 2018 ADP Pvt. Ltd.
# ALL RIGHTS RESERVED
# 
# =============================================================================

from flask import Flask, render_template, session, request
import os

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


# =============================================================================
# def addNode(nodeName,classname):
#     nodeAdded = Node(nodeName,classname)
# =============================================================================
    
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

class History:
    history = {}
    def __init__(self,label,rootcause,product,HLs = None): # HLs must be a list
        self.name = label
        self.rootcause = rootcause
        self.product = product
        self.hiddenLayer = HLs
        History.history[self.name] = self
# =============================================================================
app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/')
def loginpage():
    return render_template('prelogin.html', default = 0)

@app.route('/login/<str:username>/<str:pwd>', methods = [])
def login(username,pwd):
    #If vaidated check his access status go to homepage
        return render_template('postlogin.html', auth = string)
    else:
        return render_template('prelogin.html', default = 1) # In html page if default is 1 it says invalid credentials. Otherwise it says please login
@app.route('/<int:option>')
def selectfn(option):
    #options would be addnode, addedge, do bfs forward direction, do bfs reverse direction,addhistory
    #redirect to respective html page
@app.route("/addnode/<str:classname>/<str:nodename>",methods = ['GET','POST'])
def addNode(nodeName,classname):
    nodeAdded = Node(nodeName,classname)
    #send this to database
    #add the same to the session object
    return render_template("addnode.html", nodeName=nodeName, classname=classname)

@app.route('/addedge/<str:startnodename>/<str:endnodename>/<float:weight>', methods = ['GET','POST'])
def addEdge(startnodename,endnodename,weight):
    if startnodename in Node.nodes.keys() and endnodename in Node.nodes.keys():
        edgeAdded = Edge(startnodename,endnodename,weight)
        #Send this to database
        #Update incomingneigh, outgoingneigh column values of start and end nodes
        return render_template('addedge.html', startnode=startnodename, endnode=endnodename)
    else:
        return "!!!Error!!!"
    
@app.route('/bfsrootcause/<str:rootcause>', methods = [])
def bfsF(rootcause):
    if rootcause in Node.nodes.keys():
        rootcause.bfs()
    else:
        print("!!!Error!!!")
    return render_template("bfsF.html", rootcause = rootcause)

@app.route('/bfsproduct/<str:product>', methods = [])
def bfsR(product):
    if product in Node.nodes.keys():
        product.bfs(toggle=1)
    else:
        print('!!!Error!!!')
    return render_template('bfsR.html',product=product)
        
        
        
        
        
        
   