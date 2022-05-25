from arango import ArangoClient
from configs import arango, mongo

from pymongo import MongoClient

def getMongoCollection():
    client = MongoClient(mongo.config['endpoint'])
    db = client.more
    
def getCollection(db_name, collection_name):   
    #############  ArangoDB Setup  #############
    client = ArangoClient(hosts=arango.config['arango_endpoint'])  # Replace this with env variable
    print("Setting up client object for ", client)
    # Connect to system as root - returns api wrapper for "_system" database
    sys_db = client.db('_system', verify=False, username=arango.config['sys_dbName'], password=arango.config['root_passwd'])
    print("Connected to system db: ", sys_db)
    # Connect to db as root user - returns api wrapper for this database
    if not db_name: 
        db = client.db(arango.config['db_name'], verify=False, username=arango.config['sys_dbName'], password=arango.config['root_passwd'])
    else:
        db = client.db(db_name, verify=False, username=arango.config['sys_dbName'], password=arango.config['root_passwd'])

    print("Connected to db: ", db)
    
    def createCollection(collection_name):
        
        if db.has_collection(collection_name):
            print("Found collection: ", collection_name)
            collection = db.collection(collection_name)
        else:
            print("Collection '", collection_name, "' doesn't exist. Creating it now.")
            collection = db.create_collection(collection_name)

            # create hash index for collection 
            print("Creating hash index.")
            collection.add_hash_index(fields=['tasks', 'record_id','narc_id'], unique=True)

            collection.truncate() 
        return collection
    if not collection_name:
        collection = createCollection(collection_name)
    else:
        collection = createCollection(collection_name)
    return db, collection
    
def getGraph(db_name, graph_name):   
    #############  ArangoDB Setup  #############
    client = ArangoClient(hosts=arango.config['arango_endpoint'])  # Replace this with env variable
    print("Setting up client object for ", client)
    # Connect to system as root - returns api wrapper for "_system" database
    sys_db = client.db('_system', verify=False, username=arango.config['sys_dbName'], password=arango.config['root_passwd'])
    print("Connected to system db: ", sys_db)
    # Connect to db as root user - returns api wrapper for this database
    if not db_name: 
        db = client.db(arango.config['db_name'], verify=False, username=arango.config['sys_dbName'], password=arango.config['root_passwd'])
    else:
        db = client.db(db_name, verify=False, username=arango.config['sys_dbName'], password=arango.config['root_passwd'])

    print("Connected to db: ", db)
    
    def createGraph(graph_name):
        
        if db.has_graph(graph_name):
            print("Found graph: ", graph_name)
            graph = db.graph(graph_name)
        else:
            print("Graph '", graph_name, "' doesn't exist. Creating it now.")
            graph = db.create_graph(graph_name)

            # create hash index for collection 
            # print("Creating hash index.")
            # graph.add_hash_index(fields=['record_id'], unique=True)
            # graph.truncate() 
        return graph
    if not graph_name:
        graph = createGraph(arango.config['collection_name'])
    else:
        graph = createGraph(graph_name)

    return db, graph

def getEdgeDef(graph, edge_name, from_vertex, to_vertex):
    print('\nCreating edge definition for ', edge_name)
    if not graph.has_edge_definition(edge_name):
        edge_definition = graph.create_edge_definition(
            edge_collection=edge_name,
            from_vertex_collections=[from_vertex],
            to_vertex_collections=[to_vertex]
        )
    else:
        print("\nEdge definition already exists for ", edge_name)
    return edge_definition

def getVertexCollection(graph, vertex_name):
    print('Getting vertex collection for ', vertex_name)
    if graph.has_vertex_collection(vertex_name):
        vertex_collection = graph.vertex_collection(vertex_name)
    else:
        vertex_collection = graph.create_vertex_collection(vertex_name)
    return vertex_collection

def getEdgeCollection(graph, edge_name, from_vertex, to_vertex):
    print('\nGetting edge collection: ', edge_name)
    if graph.has_edge_definition(edge_name):
        edge_collection = graph.edge_collection(edge_name)
    else:
        edge_collection = graph.create_edge_definition(
            edge_collection=edge_name,
            from_vertex_collections=[from_vertex],
            to_vertex_collections=[to_vertex]
        )
    return edge_collection

def addEdge(edge_collection, from_vertex, to_vertex):
    edge_key = from_vertex.split('/')[1] + '-' + to_vertex.split('/')[1]
    edge_collection.insert({
        '_key': edge_key,
        '_from': from_vertex,
        '_to': to_vertex
    })