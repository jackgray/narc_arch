from arango import ArangoClient
from config import config
# from ..redcap_queries.config import config

############  ArangoDB Setup  #############
client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
print("Setting up client object for ", client)
# Connect to system as root - returns api wrapper for "_system" database
sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to system db: ", sys_db)
# Connect to db as root user - returns api wrapper for this database 
db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to db: ", db)

cursor = db.aql.execute(
    'FOR subj IN subjects3 \
        RETURN subj.task.choice.session.2'
)

cursor.id
print(cursor.batch()[1])