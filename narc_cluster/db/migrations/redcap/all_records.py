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
    if input('\nWould you like to scan for new data? (y/n)') == 'y':
        all_records = proj.export_records(format_type='json', raw_or_label='raw')
        all_instruments = proj.export_instrument_event_mappings(format_type='json')
        # print(all_records)
    
        ####### WRITE DUMP TO JSON #########
        with open('all_records_raw.json', 'w') as json_file:
            json.dump(all_records, json_file)
        records = all_records
    else:
        try:
            with open('all_records_raw.json') as json_file:
                all_records_fromfile = json.load(json_file)
                # print(all_records_fromfile)
            records = all_records_fromfile
        except:
            print("Could not open json file")
            exit()
        
    
    ############################# JSON APPEND FUNCTION ##########################
    def write_json(new_data, filename, append_index):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            print(file_data[0][append_index])
            # Join new_data with file_data inside selected field
            file_data[0][append_index].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    
    def updateArango(update_data, record_id):
        subjects_collection.update_match(
            {'record_id': record_id},
            update_data
        )
    
    questionaires = ['asi', 'wasi', 'caars']
    drugs = ['opioid', 'thc', 'alc', 'coc', 'barb', 'hall', 'sed', 'stim']
    asi_cat1s = [['lastuse'], ['abs'], ['abs_end'], 'dur_yrs', 'hx', 'quit_attempts']
    # asi_cat2s = [['lastuse']['amt', 'date', 'money'], ['abs']['longest', 'end'] ]
    
    # write full data dump to json 
    # write_json(all_records, 'all_records.json', 'subjects'[0])
    # print('\nRECORDS')
    # print(records)
#     # Doesn't return 'form' property 
#     # Find way to identify unique event 
    for subject in records:
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
                kelement_val = re.split('___', key)

                subcat = kelement_val[0].split('_')
                
                if 'asi' in key and not 'wasi' in key:
                    if any (x in kelements[1] for x in drugs):
                        update = {'battery': {'asi': {'drug': { kelements[1]: { '_'.join(kelements[2:]): value } } } } } 
                        print(update)
                        updateArango(update, record_id)
                    else:
                        update = {'battery': {'asi': { '_'.join(kelements[1:]): value } } }
                        updateArango(update, record_id)
                
                if 'wasi' in key:
                    update = {'battery': {'wasi': { '_'.join(kelements[1:]): value } } }
                    print(update)
                    updateArango(update, record_id)

                if 'wrat' in key:
                    if 'tan' or 'blue' in key:  
                        update = {'battery': {'wrat': {kelements[1]: { '_'.join(kelements[2:]): value } } } }
                    else:
                        update = {'battery': {'wrat': { '_'.join(kelements[1:]): value } } }

                    print(update)
                    
                    updateArango(update, record_id)
                
                # if any ([x in key for x in questionaires]):
                    # print('x: ', kelements[0], kelements[1:], value)
                    # print('k:', key, 'v:', value)
                    # update_data =
                
                # if len(repeat_instrument) > 0 and repeat_instrument != subcat[0]:
                    # print('1')
                    # write_json(subcat[0], 'all_records.json', 0)
                    # print(key, value)
                    update_data = [{
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
                        }]
                    # print(update_data)
                    # if len(subcat) == 2:
                    #     print('\n\n2')
                    #     print(key, value)
                    #     try:
                    #         print(kelement_val[1])
                    #     except:
                    #         pass
                    # if len(subcat) == 3:
                    #     print('\n\n3\n', key, value)
                    #     try:
                    #         print(kelement_val[1])
                    #     except:
                    #         pass                
                    # if len(subcat) == 4:
                    #     print('\n\n4\n', key,value)
                    #     try:
                    #         print(kelement_val[1])
                    #     except:
                    #         pass
                    # # for cat in subcat:
                    # #     print(cat)

                treeDepth =+ 1  # Each element is a subcategory
                # Each item in "all_records" is a different form.
                # Output in order of subject, a batch of forms is output for every subject
                # Some of the forms share the same key:value pairs, and will be overwritten if 
                # not separated into their own event subcategories
                # if len(repeat_instrument) > 0 and repeat_instrument != subcat[0]:
                #     print('1')
                #     write_json(subcat[0], 'all_records.json', 0)
                        
#                         repeat_instrument: {
#                             # a form could be filled out multiple times (i.e. follow up visits)
#                             repeat_instance: {
#                                 # break off first element ('[0]') in '_' separated 
#                                 subcat[0]: {
#                                     # join the remaining elements and make that the final key for the value to match to 
#                                     # (formatting inconsistencies make uniform parcelation unpractical)
#                                     # '_'.join(subcat[1:]): {
#                                         kelement_val[-1]:
#                                             [value]
#                                         }
#                                     # }  
#                                 }
#                             }
#                         }
#                     write_json(update_data, 'all_records.json', 0)
                    
#                 elif repeat_instrument == subcat[0]:
#                     print('2')
#                     update_data = {
#                         repeat_instrument: {
#                             repeat_instance: {
#                                 # join the remaining elements and make that the final key for the value to match to 
#                                 # (formatting inconsistencies make uniform parcelation impractical)
#                                 '_'.join(subcat[1:]): {
#                                     kelement_val[-1]: [
#                                         value
#                                         ]
#                                     }
#                                 }  
#                             }
#                     }
                            
#                 else:
#                     print('3')
#                     update_data = {
#                         # break off first element ('[0]') in '_' separated 
#                         # 'test': {
#                         #     value
#                         # }
                        
                        
#                         subcat[0]: {                                # join the remaining elements and make that the final key for the value to match to 
#                             # (formatting inconsistencies make uniform parcelation unpractical)
#                             '_'.join(subcat[1:]): [
#                                 # kelement_val[-1]: {
#                                     value
#                                     ]
#                                 }
#                                 # }
#                             }  
                            
                    
                    
                
#                 # print('\n\n   key               val: \n', key, value, '\n') 
#                 # print('instrument: ', subject['redcap_repeat_instrument'])
#                 # print('instance: ', subject['redcap_repeat_instance'])
                
#                 # update_data = jsonpickle.encode(update_data)
#                 # print("{'record_id': {", record_id.strip(), ":", update_data)
#                 print('Updating: ', update_data)
                
#                 subjects_collection.update_match(
#                     {'record_id': record_id},
#                     update_data 
#                 )
                
#     # return update_data
            
allRecords()