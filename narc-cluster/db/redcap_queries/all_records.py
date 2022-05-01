#!/usr/bin/env python

from arango import ArangoClient, AQLQueryExecuteError
import requests  
import json
import jsonpickle
import re


from redcap import Project

from config import config 
from reports import reports


def allRecords():
    
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

    ############  PyCap Setup ####################
    URL = config['api_url']
    TOKEN = config['api_token']
    proj = Project(URL, TOKEN)
    # print(proj.field_names, proj.is_longitudinal, proj.def_field)

    ############ REDCAP ALL RECORDS COLLECTION #########################

    all_records = proj.export_records(format_type='json', raw_or_label='label')
    all_instruments = proj.export_instrument_event_mappings(format_type='json')
    # print(all_records)

    # Doesn't return 'form' property 
    # Find way to identify unique event 
    for subject in all_records:
        narc_id = str(subject['narc_id']).strip()
        lname = str(subject['lname'])
        fname = str(subject['fname'])
        event_name = str(subject['redcap_event_name'])
        repeat_instrument = str(subject['redcap_repeat_instrument'])
        repeat_instance = subject['redcap_repeat_instance']
        unique_event_name = subject['redcap_event_name']
        record_id = str(subject['record_id'])
        # enrollmentGroup = str(subject['ie_enrollment_group'])
        if narc_id.startswith('S'):
            narc_id = narc_id.replace('S', '')
            # print("Dropped 'S' from narc ID: ", narc_id)
        
        # print("\n\n\n", subject)
        # print("\nNarc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\n")
        print('event_name:', unique_event_name)
        # print("\nUpdating form responses for redcap record ID ", record_id) 
        # print("{'<redcap_repeat_instrument_name>': {'<redcap_repeat_instance_count>': {'_' separated key 1st element: {'<elements 2-n>': {'<value>}}}")
        count = 1
        for key,value in subject.items():
            count=+1
            if len(str(value)) > 0 and value != '0':   
                # print(key, ": ", value) 
                treeDepth = []
                kelements= key.split('_')
                kelement_val = re.split("'___'|'(med)'", key)
                subcat = kelement_val[0].split('_')

                treeDepth =+ 1  # Each element is a subcategory
                # Each item in "all_records" is a different form.
                # Output in order of subject, a batch of forms is output for every subject
                # Some of the forms share the same key:value pairs, and will be overwritten if 
                # not separated into their own event subcategories
                if len(repeat_instrument) > 0 and repeat_instrument != subcat[0]:
                    print('1')
                    update_data = {
                        event_name: {
                            repeat_instrument: {
                                # a form could be filled out multiple times (i.e. follow up visits)
                                repeat_instance: {
                                    # break off first element ('[0]') in '_' separated 
                                    subcat[0]: {
                                        # join the remaining elements and make that the final key for the value to match to 
                                        # (formatting inconsistencies make uniform parcelation unpractical)
                                        # '_'.join(subcat[1:]): {
                                            kelement_val[-1]:
                                                [value]
                                            }
                                        # }  
                                    }
                                }
                            }
                    }
                elif repeat_instrument == subcat[0]:
                    print('2')
                    update_data = {
                        repeat_instrument: {
                            repeat_instance: {
                                # join the remaining elements and make that the final key for the value to match to 
                                # (formatting inconsistencies make uniform parcelation impractical)
                                '_'.join(subcat[1:]): {
                                    kelement_val[-1]: [
                                        value
                                        ]
                                    }
                                }  
                            }
                    }
                            
                else:
                    print('3')
                    update_data = {
                        # break off first element ('[0]') in '_' separated 
                        # 'test': {
                        #     value
                        # }
                        
                        event_name: {
                            subcat[0]: {                                # join the remaining elements and make that the final key for the value to match to 
                                # (formatting inconsistencies make uniform parcelation unpractical)
                                '_'.join(subcat[1:]): [
                                    # kelement_val[-1]: {
                                        value
                                        ]
                                    }
                                    # }
                                }  
                            }
                    
                    
                
                # print('\n\n   key               val: \n', key, value, '\n') 
                # print('instrument: ', subject['redcap_repeat_instrument'])
                # print('instance: ', subject['redcap_repeat_instance'])
                
                # update_data = jsonpickle.encode(update_data)
                # print("{'record_id': {", record_id.strip(), ":", update_data)
                print('Updating: ', update_data)
                
                subjects_collection.update_match(
                    {'record_id': record_id},
                    update_data 
                )
                
    # return update_data
            
allRecords()