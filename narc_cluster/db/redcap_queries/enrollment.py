from arango import ArangoClient
from redcap import Project
from config import config
from reports import reports


#############  ArangoDB Setup  #############

client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
print("Setting up client object for ", client)
# Connect to system as root - returns api wrapper for "_system" database
sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to system db: ", sys_db)
# Connect to db as root user - returns api wrapper for this database 
db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to db: ", db)


############ using PyCap ####################
URL = config['api_url']
TOKEN = config['api_token']
proj = Project(URL, TOKEN)
# print(proj.field_names, proj.is_longitudinal, proj.def_field)



############# FIND || CREATE COLLECTION ####################
# Create collection if not exist - return api for collection 
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

############ REDCAP ENROLLMENTS COLLECTION

subjects_collection = createCollection(config['collection_name'])

enrollment_rpt = proj.export_report(report_id=reports['enrollment'], format_type='json')

for subject in enrollment_rpt:
    
    narc_id = str(subject['narc_id']).strip()
    record_id = str(subject['record_id']).strip()
    lname = str(subject['lname'])
    fname = str(subject['fname'])
    enrollmentGroup = str(subject['ie_enrollment_group'])
    if narc_id.startswith('S'):
        narc_id = narc_id.replace('S', '')
        # print("Dropped 'S' from narc ID: ", narc_id)
        
    print("Narc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\nUD Group :", enrollmentGroup, "\n")
    
##########  ARANGO DB INSERTION #####################
    print("\nInserting data for subject ", narc_id)
    subjects_collection.insert({
        '_key': narc_id, 
        'record_id': record_id, 
        'enrollment_group': enrollmentGroup, 
        'name': {
            'first': fname,
            'last': lname
            },
        })

