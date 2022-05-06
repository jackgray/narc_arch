import excel2json
from arango import ArangoClient
import json
import pandas as pd
from config import files, sheets, config

# from narc_arch.narc_cluster.db.redcap_queries.config import config


#############  ArangoDB Setup  #############
client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
print("Setting up client object for ", client)
# Connect to system as root - returns api wrapper for "_system" database
sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to system db: ", sys_db)
# Connect to db as root user - returns api wrapper for this database 
db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
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
subjects_collection = createCollection(config['collection_name'])

def updateByKey(update_data, update_key, update_value):
    subjects_collection.update_match(
        {update_key: update_value},
        update_data
    )

# forPrediction = excel2json.convert_from_file('forPrediction.xlsx', engine='openpyxl')
for file_k, file_v in files.items():
    for sheet_k, sheet_v in sheets.items():
        print('\n\nSHEET: ', sheet_k)
        sheet_df = pd.read_excel(file_v, engine='openpyxl', sheet_name=sheet_v)
        sheet_json = sheet_df.to_json(orient='records')

        jsonobject = json.loads(sheet_json)
        jsonformatted = json.dumps(jsonobject, indent=4)
        # print(jsonformatted)

        # for k, v in jsonformatted:
        #     subj = k[0].replace('sub-S', '')
        #     print(k, v)
        for i in jsonobject:
            # print(i['subj'])
            _key = i['subj'].replace('sub-S', '')
            print(_key)
            # print(i)
            
            task_name = sheet_v.split('_')[0]
            session = i['session']
            
            for j, k in i.items():
                print(j,k)
            
                update = { 'task': {task_name: { 'session': {session: {j:k }}}}}
                print(update)
            # # print(json.dumps(update, indent=4))
            
                updateByKey(update, '_key', _key)
            
            
            # for k in i['subj']:
            #     print(k)
        