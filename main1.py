from flask import Flask, render_template, session, request
from jinja2 import Template
from nodeclass import *
from edgeclass import *
import os
import sqlite3

try:
    db = sqlite3.connect("projectv4");
    cursor = db.cursor()
    logincheck = True
except:
    logincheck = False
    
app = Flask(__name__)
app.secret_key = os.urandom(16)
app.debug = True

#@app.route('/')
#def loginpage():
#   return render_template('Login_Page.html')

#@app.route('/login/<str:username>/<str:pwd>', methods = ['POST'])
def login(username,pwd):
    if logincheck:
        try:
            cursor.execute("select * from node")
            nodes = cursor.fetchall()
            for node in nodes:
                Node(node[1], node[2], node[0], node[3].split(','), node[4].split(','))
        except:
            string3 = 'Failed to fetch nodes'

        try:
            cursor.execute("select * from edge")
            edges = cursor.fetchall()
            for edge in edges:
                Edge(edge[2], edge[3], edge[4], edge[0])
        except:
            string4 = 'Failed to fetch edges'
            return render_template('Homepage.html')
    
    else:
        return render_template('Login2.html') # In html page if default is 1 it says invalid credentials. Otherwise it says please login
            
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
    

    #add the same to the session object
    return render_template("Add_Node.html", nodeName=nodeName, classname=classname)

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
        insertcmd = "insert into edge values(%s, %s, %s, %s, %f);"%(edgeAdded.edge_id, edgeAdded.name, edgeAdded.startNode, edgeAdded.endNode, edgeAdded.weight);
        cursor.execute(insertcmd)
        #Update incomingneigh, outgoingneigh column values of start and end nodes
        return render_template('addedge.html', startnode=startnodename, endnode=endnodename)
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
    return render_template("bfsF.html", rootcause = rootcause)

#@app.route('/bfsproduct/<str:product>', methods = [])
def bfsR(product):
    if product in Node.nodes.keys():
        product.bfs(toggle=1)
    else:
        print('!!!Error!!!')
    return render_template('bfsR.html',product=product)

if __name__ == '__main__':
    app.run()


addNode("a","z")
