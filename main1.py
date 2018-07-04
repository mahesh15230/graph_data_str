from flask import Flask, render_template, session, request
from jinja2 import Template
from nodeclass import *
from edgeclass import *
import os
import sqlite3

try:
    db = sqlite3.connect('p1');
    cursor = db.cursor()
    logincheck = True
except:
    logincheck = False
    
#app = Flask(__name__)
#app.secret_key = os.urandom(16)
#app.debug = True

#@app.route('/')
#def loginpage():
#   #return render_template('Login_Page.html')

#@app.route('/login/<str:username>/<str:pwd>', methods = ['POST'])

class Node:
    nodes = {}
    node_id = {}
    def __init__(self,nodeName,classname,id=None,incneigh=None,outneigh=None):
        if not nodeName in Node.nodes.keys():
            if id==None and incneigh==None and outneigh==None:
                self.name = nodeName
                self.id = randgen()
                self.incomingNeighbors = [] # List of strings
                self.outgoingNeighbors = [] # List of strings
                self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
                self.isVisited = False
                self.nodeweight = 1
                Node.nodes[self.name] = self
                Node.node_id[self.id] = self
            else:
                self.name = nodeName
                self.id = id
                self.incomingNeighbors = incneigh # List of strings
                self.outgoingNeighbors = outneigh # List of strings
                self.classname = classname # Can be 'rootcause','HL','RCS' or 'product'
                self.isVisited = False
                self.nodeweight = 1
                Node.nodes[self.name] = self
                Node.node_id[self.id] = self
        else:
            strin1g = "Node already exists"
        
            
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

def randgen1():
    lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
    str = "".join(lst)
    return str


class Edge:
    edges = {}
    edge_id = {}
    def __init__(self,fromNode,toNode,weight):#,id=None):   
        if id == None:    
            if fromNode!=toNode:
                self.id = randgen1()
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


def login(username,pwd):
    if logincheck:
        try:
            cursor.execute("select * from node")
            nodes = cursor.fetchall()
            #print(nodes)
            for i in nodes:
                print(i)
                dummy = Node(node[1], node[2], node[0])#node[3].split(','), node[4].split(','))
                #print(Node.nodes)
        except:
            string3 = 'Failed to fetch nodes'

        try:
            cursor.execute("select * from edge")
            edges = cursor.fetchall()
            for edge in edges:
                Edge(edge[2], edge[3], edge[4], edge[0])
        except:
            string4 = 'Failed to fetch edges'
            #return render_template('Homepage.html')
    
    #else:
        #return render_template('Login2.html') # In html page if default is 1 it says invalid credentials. Otherwise it says please login

#for key in Node.nodes:
 #   print(Node.nodes[key])

def randgen():
    lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
    str = "".join(lst)
    return str


    
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

# =============================================================================
# #@app.route('/postlogin/<int:option>')
# def postlogin(option):
#     try:
#       cursor.execute("select * from node;")
#       nodes = cursor.fetchall()
#       for node in nodes:
#           Node(node[1], node[2])
#     except:
#         print('Failed to fetch nodes')
# 
#     try:
#       cursor.execute("select * from edge;")
#       edges = cursor.fetchall()
#       for edge in edges:
#           Edge(edge[2], edge[3], edge[4])
#     except:
#         print('Failed to fetch edges')
# =============================================================================



#@app.route("/addnode/<str:classname>/<str:nodename>",methods = ['GET','POST'])
def addNode(nodeName,classname):
    if not nodeName in Node.nodes.keys():
        nodeAdded = Node(nodeName,classname)
    else:
        string2 = "Node can't be created with a name that already exists"
    #send this to database
    cursor.execute("insert into node(nodeid,nodename,classname) values(?,?,?)",(nodeAdded.id, nodeAdded.name, nodeAdded.classname))
    db.commit()

    #add the same to the session object
    ##return render_template("Add_Node.html", nodeName=nodeName, classname=classname)

#@app.route("/delnode/<str:nodename>/<str:toggle>", methods = [])
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
        
#@app.route('/addedge/<str:startnodename>/<str:endnodename>/<float:weight>', methods = ['GET','POST'])
def addEdge(startnodename,endnodename,weight):
    if startnodename in Node.nodes.keys() and endnodename in Node.nodes.keys():
        edgeAdded = Edge(startnodename,endnodename,weight)
        #Send this to database
        cursor.execute('insert into edge(edgeid,edgename,startnode,endnode,weight) values(?,?,?,?,?)',(randgen1(),edgeAdded.name,edgeAdded.startNode,edgeAdded.endNode,edgeAdded.weight))
        #cursor.execute('insert into edge(edgeid,edgename,startnode,endnode,weight) values(?,?,?,?,?)',(edgeAdded.id, edgeAdded.name, edgeAdded.startNode, edgeAdded.endNode, edgeAdded.weight))
        #Update incomingneigh, outgoingneigh column values of start and end nodes
        ##return render_template('addedge.html', startnode=startnodename, endnode=endnodename)
        db.commit()
    else:
        return "!!!Error!!!"

#@app.route('/deledge/<str:startnodename>/<str:endnodename>', methods = [])
def delEdge(startnodename,endnodename):
    del Edge.edges[startnodename + ":" + endnodename]
    print("Edge is deleted")
    
#@app.route('/bfsrootcause/<str:rootcause>', methods = [])
def bfsF(rootcause):
    if rootcause in Node.nodes.keys():
        rootcause.bfs()
    else:
        print("!!!Error!!!")
    #return render_template("bfsF.html", rootcause = rootcause)

#@app.route('/bfsproduct/<str:product>', methods = [])
def bfsR(product):
    if product in Node.nodes.keys():
        product.bfs(toggle=1)
    else:
        print('!!!Error!!!')
    #return render_template('bfsR.html',product=product)

#if __name__ == '__main__':
    #app.run()
login('a','a')
print(Node.nodes)