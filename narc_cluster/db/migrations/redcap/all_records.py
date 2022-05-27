#!/usr/bin/env python

from arango import ArangoClient, AQLQueryExecuteError
import requests  
import json
import jsonpickle
import re


from redcap import Project
from pymongo import MongoClient
from configs import mongo, redcap, arango 
from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
# from reports import reports

def allRecords():
    
    arangodb, arango_collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    
    mongodb = MongoClient(mongo.config['endpoint'])
    mongo_collection = mongodb.more.subjects
    
    ############  PyCap Setup ####################
    URL = redcap.config['api_url']
    TOKEN = redcap.config['api_token']
    proj = Project(URL, TOKEN)
    # print(proj.field_names, proj.is_longitudinal, proj.def_field)

    ############ REDCAP ALL RECORDS COLLECTION #########################
    # all records take a long time, so safe results to json file for dev mode 
    if input('\nWould you like to scan for new data? (y/n)') == 'y':
        all_records = proj.export_records(format_type='json', raw_or_label='raw')
        all_instruments = proj.export_instrument_event_mappings(format_type='json')
        # print(all_records)
    
        ####### WRITE DUMP TO JSON #########
        with open('/home/jackgray/Code/narc_arch/narc_cluster/db/migrations/redcap/all_records_raw.json', 'w') as json_file:
            json.dump(all_records, json_file)
        records = all_records
    else:
        with open('/home/jackgray/Code/narc_arch/narc_cluster/db/migrations/redcap/all_records_raw.json') as json_file:
                all_records_fromfile = json.load(json_file)
                # print(all_records_fromfile)
                records = all_records_fromfile
    
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
    
    questionaires = ['caars', 'sogs', 'surps', 'bai', 'bdi','hcq', 'bisbas', 'smast', 'sows', 'tsr', 'sds', 'tlfb', 'colorblind', 'menstrual_v2', 'menstrual', 'ftnd', 'spsrq', 'nada_t', 'nada', 'frsbe', 'mpq', 'strap_r', 'strap', 'staxi', 'ctq', 'pss', 'ffmq', 'wos_s', 'wos','aliens', 'cohs' ]
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
        
        print('\n\n')
        narc_id = str(subject['narc_id']).strip()
        current_data = arango_collection.find({'_key': narc_id})
        # print('CURRENT_DATA')
        # print(current_data)
        lname = str(subject['lname'])
        fname = str(subject['fname'])
        event_name = str(subject['redcap_event_name'])
        repeat_instrument = str(subject['redcap_repeat_instrument'])
        repeat_instance = subject['redcap_repeat_instance']
        record_id = str(subject['record_id']).strip()
       
        # enrollmentGroup = str(subject['ie_enrollment_group'])
        print(record_id)
        if narc_id.startswith('S'):
            narc_id = narc_id.replace('S', '')
        if len(narc_id) < 1:
            narc_id_cursor = arango_collection.find({'record_id': record_id})
            for i in narc_id_cursor:
                narc_id = i['_key']
                print("NARCID")
        if len(narc_id) < 1:
            continue
            
            

            # print("Dropped 'S' from narc ID: ", narc_id)
        # print("\n\n\n", subject)
        # print("\nNarc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\n")
        # print('event_name:', unique_event_name)
        # print("\nUpdating form responses for redcap record ID ", record_id) 
        # print("{'<redcap_repeat_instrument_name>': {'<redcap_repeat_instance_count>': {'_' separated key 1st element: {'<elements 2-n>': {'<value>}}}")
        count = 1
        update_data = {'_key': narc_id}
        for key,value in subject.items():
            print("\n\nUPDATE DATA")
            print(update_data)
            count=+1
            if len(str(value)) > 2 and value != '0': 
                # print('\n\n\nNARC',narc_id)

                # print(key, ": ", value) 
                treeDepth = []
                kelements= key.split('_')
                kelement_val = re.split('___', key)

                subcat = kelement_val[0].split('_')
                
                if 'asi' in key and not 'wasi' in key:
                    if any (x in kelements[1] for x in drugs):
                        update_data.update({'questionaires': {'asi': { kelements[1]: { '_'.join(kelements[2:]): value } } } } )
                        # print(update)
                    else:
                        update_data.update({'questionaires': {'asi': { '_'.join(kelements[1:]): value } } })
                        # updateArango(update, record_id)
                    update_attributes = 'questionaires.asi'
                    hash_index_fields = ['questionaires: { asi }']
                    match_criteria = { '_key': narc_id }
                    
                elif 'wasi' in key:
                    update_data.update({'questionaires': {'wasi': { '_'.join(kelements[1:]): value } } })
                    update_attributes = 'questionaires.wasi'
                    hash_index_fields = ["{ questionaires: { wasi: { date }}}"]
                    match_criteria = { '_key': narc_id }
                elif 'wrat' in key:                
                    update_data.update({'questionaires': {'wrat': { '_'.join(kelements[1:]): value } } })
                    update_attributes = 'questionaires.wrat'
                    hash_index_fields = ['{ questionaires: { wrat: { date']
                    match_criteria = { '_key': narc_id}
                    # print(update)
                    
                    # updateArango(update, record_id)
                    
                    '''
                    
                    reports idea: assume all reports on redcap preceded with "toDB_ are legitimate. scan for all reports, add them based on their name by subject
                    
                    '''
        
              
                
                # Case when record is from a repeat instrument
                elif len(repeat_instrument) > 0:
                    session = 'ses_' + str(repeat_instance)
                    if str(kelements[0]).strip() == repeat_instrument:
                        k = "_".join(kelements[1:])
                    else:
                        k = key
                    
                    
                        
                    #### CURRDRUGS_DAILY_INTERVIEW ########
                    # if repeat_instrument == 'currdrugs':
                    #     # print(key, value)
                    #     session = 'ses_' + str(repeat_instance)
                    #     if key.startswith('curr_'):
                    #         key = '_'.join(kelements[1:])
                    #     elif key.endswith('currdrugs'):
                    #         key = '_'.join(kelements[:-1])
                    #     elif key.startswith('currdrugs_daily'):
                    #         key = '_'.join(kelements[2:])
                        
                    #     currdrugs_session = repeat_instance
                    #     fieldstr = str("{questionaires: { currdrugs: { redcap_repeat_instance }")
                    #     index_fields = [fieldstr]
                    #     match_criteria = {'_key': narc_id, 'questionaires': { 'currdrugs': { 'redcap_repeat_instance': repeat_instance}}}
                    #     # print(update_data)
                    
                    update_data.update({ 'questionaires': { repeat_instrument: [{k: value}] } })
                    update_attributes = 'questionaires.' + repeat_instrument + '[' + str(repeat_instance) + ']'
                    fieldstr = 'questionaires.', repeat_instrument, '.redcap_repeat_instance'
                    hash_index_fields = [fieldstr]
                    # date = subject[repeat_instrument]
                    match_criteria = { '_key': narc_id, 'questionaires': { repeat_instrument: [{'redcap_repeat_instance': repeat_instance }] } }
                    # print(json.dumps(update_data)) 
                    
                elif 'ema' in key:
                    
                    session = event_name.split('_')[2]
                    if key.startswith('ema_'):
                        key = '_'.join(key.split('_')[1:])
                    if 'complete' in key:
                        key = 'complete'
                    # if 'date' in value == 
                    # date = subject['asi_date']
                    update_data = update_data.update({ 'questionaires': { 'ema': [{key: value }] }})
                    # print('\nEMA: ', session)
                    update_attributes = 'questionaires.ema'
                    hash_index_fields = ['questionaires/ema/date']
                    match_criteria = { '_key': narc_id, 'questionaires': { 'ema': [{ 'date': subject['ema_date']}] }}
                    filter_criteria = 'questionaires.ema.date == ' + subject['ema_date']
                    # print(update_data)
                    
                elif 'panas' in key:
                    date = subject['panas_date']
                    # print(event_name, repeat_instrument, repeat_instance)
                    # print(key, value)
                    
                    if 'complete' in key:
                        key = 'complete'
                    
                    if key.startswith('panas'):
                        key = '_'.join(key.split('_')[1:])
                    try: update_data.update({ 'questionaires': { 'panas':  [{key: value}] } })
                    except: pass
                    update_attributes = 'questionaires.panas[0]'
                    text_index_fields = ['questionaires.panas']
                    hash_index_fields = ['questionaires.panas.date']
                    match_criteria = {'_key': narc_id, 'questionaires': { 'panas': { 'date': subject['panas_date']} } }
                    # print(update_data)
                
                elif any (x in questionaires for x in kelements):
                    
                    # if 'complete' in key:
                    #     pass
                    #     # # print(key)
                    #     # k = 'complete'
                    #     # questionaire = questionaire
                    
                        
                    if 'strap' in key or 'nada' in key and not 'complete' in key:
                        print('key:', key)
                        k = '_'.join(kelements[2:])
                        questionaire = '_'.join(kelements[0:2])
                        print('questionaire: ', questionaire)
                    
                    elif 'non_dual' in key or 'aliens' in key:
                        questionaire = questionaire
                        k = kelements[-1]
                    else: 
                        print('key: ', key)
                        if len(kelements) < 3:
                            k = '_'.join(kelements[1:])
                            questionaire = kelements[0]
                        else: 
                            k = kelements[-1]
                            questionaire = questionaire
                        
                    
                    print('questionaire: ', questionaire)
                    print(update_data)
                    try: update_data.update({ 'questionaires': { questionaire: [{k: value }] } } )
                    except: pass
                    update_attributes = 'questionaires.' + questionaire + '[0]'

                    # date = subject['questionaires'][questionaire]['date']
                    # fieldstr = ' '.join("{ questionaires: {", questionaire, ": { date }}")
                    # hash_index_fields = [fieldstr]
                    q_date = questionaire + '_date'
                    if 'menstrual' in key:
                        questionaire = 'menstrual'
                        q_date = 'menstrual_hx_date'
                    print('q_date: ' + q_date)
                    
                    if questionaire == 'ftnd':
                        match_criteria = { '_key': narc_id }
                    else:
                        match_criteria = { '_key': narc_id, 'questionaires': { questionaire: { 'date': subject[q_date]}}}
                        filter_criteria = 'questionaires.' + questionaire + '.date == ' + subject[q_date]
                    index_type = 'persistent'
                    # update_data = { 'questionaires': { questionaire: [{date: q_date }] } } 
                    
                elif key.startswith('phi_'):
                    update_data = { 'phi': { '_'.join(kelements[1:]): value}}
                    # print(json.dumps(update_data))
                
                elif 'task_day' in event_name:
                    # print(event_name)
                    # print(key,value)
                    session = 'ses_' + str(event_name.split('_')[2])
                    if kelements[0] in event_name:
                        k = key
                    else:
                        k = '_'.join(kelements[1:])
                        
                    if 'curr' in key:
                        print(k)
                        kelements[0] = 'curr_drugs'
                        k = '_'.join('_'.join(key.split('_currdrugs')).split('currdrugs_'))
                    update_data = update_data.update({ 'tasks': { 'curr_drugs': [{kelements[0]: { k: value, 'session': event_name.split("_")[2] }}] } } )
                    update_attributes = 'tasks.curr_drugs[0]'
                    hash_index_fields = ['tasks/curr_drugs/date']
                    match_criteria = { '_key': narc_id, 'tasks': { 'curr_drugs': [{'session': event_name.split('_')[2] }] }}
                else:
                    # print(event_name)
                    # print(key, value)
                    pass
                # if len(update_data) > 0 and len(narc_id) > 0:
                    # update_data.update({"_": narc_id })

                    # subjects_collection.find_one_and_update({'_id': narc_id}, {'$set': update_data})
                    
                    
                    # print(update_data)
                    # arango_collection.update_match({'_key': narc_id }, update_data)

                    # query_string = str("FOR s in " + arango.config['collection_name'] + " FILTER s._key == " + narc_id + " FILTER filter_criteria UPDATE s WITH { " + ':{'.join(update_attributes.split('.')[0:2]) + "}: APPEND(s." + update_attributes + ", " + json.dumps(update_data)+ ")} IN " + arango.config['collection_name'] )
                    # print(query_string)
                    # arangodb.aql.execute(query_string,
                    #                 batch_size=1
                    #             )
    
                    # if len(hash_index_fields) > 0:
                    #     print(hash_index_fields)
                    #     index = arango_collection.add_persistent_index(fields=hash_index_fields, sparse=True)
                    #     print(index)
    print(json.loads(update_data))
                    # updateArango(arango_collection, narc_id, update_data)

                # if any ([x in key for x in questionaires]):
                    # print('x: ', kelements[0], kelements[1:], value)
                    # print('k:', key, 'v:', value)
                    # update_data =
                
                # if len(repeat_instrument) > 0 and repeat_instrument != subcat[0]:
                    # print('1')
                    # write_json(subcat[0], 'all_records.json', 0)
                    # print(key, value)
                    # update_data = [{
                    #     repeat_instrument: {
                    #     # a form could be filled out multiple times (i.e. follow up visits)
                    #         repeat_instance: {
                    #             # break off first element ('[0]') in '_' separated 
                    #             subcat[0]: {
                    #                 # join the remaining elements and make that the final key for the value to match to 
                    #                 # (formatting inconsistencies make uniform parcelation unpractical)
                    #                 # '_'.join(subcat[1:]): {
                    #                     kelement_val[-1]:
                    #                         [value]
                    #                     }
                    #                 # }  
                    #             }
                    #         }
                    #     }]
                    # # print(update_data)
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

                # treeDepth =+ 1  # Each element is a subcategory
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
                
#                 collection.update_match(
#                     {'record_id': record_id},
#                     update_data 
#                 )
                
#     # return update_data
            
allRecords()