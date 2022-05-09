from arango import ArangoClient
from narc_cluster.db.configs.arango import config

# from ..redcap_queries.config import config

def test():
    ############  ArangoDB Setup  #############
    print("Setting up Arango client")
    client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
    print("Retrieved Arango client object: ", client)
    print("Setting up client object for ", client)
    # Connect to system as root - returns api wrapper for "_system" database
    sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['root_passwd'])
    print("Connected to system db: ", sys_db)
    # Connect to db as root user - returns api wrapper for this database 
    db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['root_passwd'])
    print("Connected to db: ", db)
    
    # subjects = db.collection(config['collection_name'])
    # # subjects.all()
    # print('subjs', subjects)

    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            RETURN { key: subject._key, total: subject.battery.wasi.total, age: subject.dob }',
        batch_size=1
    )
    # print(subjects)
    
    # result = [subject for subject in cursor]
    # print("res: ", result)
    
    for subject in cursor:
        # print("key:", subject, "\nwasi total: ", subject.total)
        print(subject)
    # # cursor.id
        # print(cursor)
        
    # while cursor.has_more():
    #     subject = cursor.next()
    #     print(subject)
        
    # cursor.fetch() 
    # print("batch:", cursor.batch())
   
    
    