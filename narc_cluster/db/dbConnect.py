from arango import ArangoClient
from narc_cluster.db.configs.arango import config 
    
def dbConnect():   
    #############  ArangoDB Setup  #############
    client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
    print("Setting up client object for ", client)
    # Connect to system as root - returns api wrapper for "_system" database
    sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['root_passwd'])
    print("Connected to system db: ", sys_db)
    # Connect to db as root user - returns api wrapper for this database 
    db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['root_passwd'])
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
            collection.add_hash_index(fields=['record_id'], unique=True)

            collection.truncate() 
        return collection
    collection = createCollection(config['collection_name'])
    return db, collection