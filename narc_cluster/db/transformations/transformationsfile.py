#!/usr/bin/env python

from arango import ArangoClient, AQLQueryExecuteError
import requests  

from narc_cluster.db.utils.dbConnect import getCollection
from narc_cluster.db.utils.redcapConnect import redcapConnect
from narc_cluster.db.configs import arango, redcap, reports

db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
proj = redcapConnect()

############ REDCAP ALL RECORDS COLLECTION #########################

db, redcap_events_collection = getCollection(arango.config['db_name'], 'redcap_events')

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
            res=redcap_events_collection.update_match(
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
        
    

    

################# ANALYZERS / TRANSFORMATIONS ###################

