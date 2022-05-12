#!/usr/bin/env python

from arango import ArangoClient, AQLQueryExecuteError
import requests  


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



#################  RedCap API setup   ###################


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

subjects_collection = createCollection('subjects')

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


############ REDCAP ALL RECORDS COLLECTION #########################

redcap_events_collection = createCollection('redcap_events')

all_records = proj.export_records(format_type='json')
all_instruments = proj.export_instrument_event_mappings(format_type='json')
# print(all_records)

for subject in all_records:
    narc_id = str(subject['narc_id']).strip()
    lname = str(subject['lname'])
    fname = str(subject['fname'])
    redcap_event_name = str(subject['redcap_event_name'])
    
    redcap_repeat_instrument = str(subject['redcap_repeat_instrument'])
    
    redcap_repeat_instance = subject['redcap_repeat_instance']

    record_id = str(subject['record_id'])
    # enrollmentGroup = str(subject['ie_enrollment_group'])
    if narc_id.startswith('S'):
        narc_id = narc_id.replace('S', '')
        print("Dropped 'S' from narc ID: ", narc_id)
    
    # print("\n\n\n", subject)
    # print("\nNarc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\n")
    
####### ARANGO UPDATE #########
    print("\nUpdating form responses for redcap record ID ", record_id) 
    count = 1
    for key,value in subject.items():
        count=+1
        if len(str(value)) > 0:   
            print(key, ": ", value) 
            treeDepth = []
            kelements= key.split('_')
            treeDepth =+ 1  # Each element is a subcategory
            # Each item in "all_records" is a different form.
            # Output in order of subject, a batch of forms is output for every subject
            # Some of the forms share the same key:value pairs, and will be overwritten if 
            # not separated into their own event subcategories
            res=subjects_collection.update_match(
                {'record_id': record_id},
                {
                subject['redcap_repeat_instrument']: {
                    subject['redcap_repeat_instance']: {
                        kelements[1]: {
                            kelements[2]: {
                                kelements[3]: {
                                    value
                                }
                            }
                        }
                        }
                    }
                }
            )
            print("res: ", res)
        
    
    # redcap_events_collection.insert({
    #     '_key': record_key,
    #     'record_id': record_id,
    #     'redcap_event_name': redcap_event_name
    # })
    

################# ANALYZERS / TRANSFORMATIONS ###################
