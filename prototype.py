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

db = pymysql.connect(host="localhost", user="root", db="graph");
cursor = db.cursor()

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


# =============================================================================
# def addNode(nodeName,classname):
#     nodeAdded = Node(nodeName,classname)
# =============================================================================
    
def delNode(nodeName,toggle=None):
    if toggle == None:  
        for i in Edge.edges.keys():
            if nodeName+":" in i:
                Edge.edges[i].startNode = None
                Edge.edges['None'+str(Edge.edges[i].endNode)] = Edge.edges.pop(i)
            elif ":"+nodeName in i:
                Edge.edges[i].endNode = None
                Edge.edges[str(Edge.edges[i].startNode)+'None'] = Edge.edges.pop(i)
        del Node.nodes[nodeName]
        print(nodeName,"is deleted")
    else:
        for i in Edge.edges.keys():
            if nodeName in i:
                del Edge.edges[i]
        del Node.nodes[nodeName]
        print("Node along with attached edges are deleted")
    
def delEdge(id):
    del Edge.edge_id[id]
    print("Edge is deleted")
    
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
    try:
      cursor.execute("select * from node;")
      nodes = cursor.fetchall()
      for node in nodes:
          Node(node[1], node[2])
    except:
        print 'Failed to fetch nodes'

    try:
      cursor.execute("select * from edge;")
      edges = cursor.fetchall()
      for edge in edges:
          Edge(edge[2], edge[3], edge[4])
    except:
        print 'Failed to fetch edges'


    #options would be addnode, addedge, do bfs forward direction, do bfs reverse direction,addhistory
    #redirect to respective html page
@app.route("/addnode/<str:classname>/<str:nodename>",methods = ['GET','POST'])
def addNode(nodeName,classname):
    nodeAdded = Node(nodeName,classname)
    #send this to database
    insertcmd = "insert into node values(%d, %s, %s, %s, %s);"%(nodeAdded.id, nodeAdded.name, nodeAdded.classname, nodeAdded.incomingNeighbors, nodeAdded.outgoingNeighbors);
    cursor.execute(insertcmd);

    #add the same to the session object
    return render_template("addnode.html", nodeName=nodeName, classname=classname)

@app.route('/addedge/<str:startnodename>/<str:endnodename>/<float:weight>', methods = ['GET','POST'])
def addEdge(startnodename,endnodename,weight):
    if startnodename in Node.nodes.keys() and endnodename in Node.nodes.keys():
        edgeAdded = Edge(startnodename,endnodename,weight)
        #Send this to database
        insertcmd = "insert into edge values(%d, %s, %d, %d, %d);"%(edgeAdded.edge_id, edgeAdded.name, edgeAdded.startNode, edgeAdded.endNode, edgeAdded.weight);
        cursor.execute(insertcmd)
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