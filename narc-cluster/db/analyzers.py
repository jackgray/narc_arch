from arango import ArangoClient
from config import config
#############  ArangoDB Setup  #############

client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
print("Setting up client object for ", client)
# Connect to system as root - returns api wrapper for "_system" database
sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to system db: ", sys_db)
# Connect to db as root user - returns api wrapper for this database 
db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to db: ", db)


db.analyzers()
db.create_analyzer(
    name='general_analyzer',
    analyzer_type='identity',
    properties={},
    features=[]
)

# Create ArangoSearch view 
db.create_arangosearch_view(
    name='all_fields',
)
link = {
    "inclueAllFields": True,
    "fields": { "description": { "analyzers" : [ "text_en" ] } }
    
}

db.update_arangosearch_view(
    name='all_fields',
    properties={'links': { 'subjects': link}}
)