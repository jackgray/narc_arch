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
from migrations.redcap.functions import hasComplete
# from reports import reports

def mssmRecords():
    
    arangodb, arango_collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    
    mongodb = MongoClient(mongo.config['endpoint'])
    mongo_collection = mongodb.more.subjects
    
    ############  PyCap Setup ####################
    URL = redcap.config['api_url']
    TOKEN = redcap.config['mssm_token']
    proj = Project(URL, TOKEN)
    # print(proj.field_names, proj.is_longitudinal, proj.def_field)

    if input('\nWould you like to scan for new data? (y/n)') == 'y':
            all_records = proj.export_records(format_type='json', raw_or_label='raw')
            all_instruments = proj.export_instrument_event_mappings(format_type='json')
            # print(all_records)
        
            ####### WRITE DUMP TO JSON #########
            with open('/home/jackgray/Code/narc_arch/narc_cluster/db/migrations/redcap/mssm/all_records_raw.json', 'w') as json_file:
                json.dump(all_records, json_file)
            records = all_records
    else:
        with open('/home/jackgray/Code/narc_arch/narc_cluster/db/migrations/redcap/mssm/all_records_raw.json') as json_file:
                all_records_fromfile = json.load(json_file)
                # print(all_records_fromfile)
                records = all_records_fromfile
    
    assessments = ['caars', 'sogs', 'surps', 'bai', 'bdi','hcq', 'bisbas', 'smast', 'sows', 'tsr', 'sds', 'tlfb', 'colorblind', 'menstrual_v2', 'menstrual', 'ftnd', 'spsrq', 'nada_t', 'nada', 'frsbe', 'mpq', 'strap_r', 'strap', 'staxi', 'ctq', 'pss', 'ffmq', 'wos_s', 'wos','aliens', 'cohs', 'ars', 'erq', 'pes', 'dsm',    ]
    drugs = ['opioid', 'thc', 'alc', 'coc', 'barb', 'hall', 'sed', 'stim']
    asi_cat1s = [['lastuse'], ['abs'], ['abs_end'], 'dur_yrs', 'hx', 'quit_attempts']
    # asi_cat2s = [['lastuse']['amt', 'date', 'money'], ['abs']['longest', 'end'] ]
    print('awaiting response from server')
    for subject in records:
        # print(subject)
     
        narc_id = str(subject['narc_id']).strip()
        current_data = arango_collection.find({'_key': narc_id})
        event_name = str(subject['redcap_event_name'])
        repeat_instrument = str(subject['redcap_repeat_instrument'])
        repeat_instance = subject['redcap_repeat_instance']
        record_id = str(subject['record_id']).strip()
        group = str(subject['dx_group'])
        
        # record id and narc id are the same in this redcap project
        if len(narc_id) < 1:
            narc_id = record_id
        if narc_id.startswith('S'):
            narc_id = narc_id.replace('S', '')
            
        # print(narc_id, group)
            
        subj_data = {'_key': narc_id, 'record_id': record_id}
        
        # print(subj_data)
        
        try: arango_collection.insert(subj_data)
        except: print('Could not add new subject. NARC ID exists already')
        
        for key,value in subject.items():
            if len(str(value)) > 0 and value != '0': 
                # print(key, value)
                kelements= key.split('_')
                kelement_val = re.split('___', key)

                subcat = kelement_val[0].split('_')
                
                if 'asi' in key and not 'wasi' in key:
                    if any (x in kelements[1] for x in drugs):
                        update_data = {'assessments': {'asi': { kelements[1]: { '_'.join(kelements[2:]): value } } } } 
                        # print(update)
                    else:
                        update_data = {'assessments': {'asi': { '_'.join(kelements[1:]): value } } }
                    
                elif 'wasi' in key:
                    update_data = {'assessments': {'wasi': { '_'.join(kelements[1:]): value } } }
                   
                elif 'wrat' in key:                
                    update_data = {'assessments': {'wrat': { '_'.join(kelements[1:]): value } } }
                    
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
                        
                    ### CURRDRUGS_DAILY_INTERVIEW ########
                    if repeat_instrument == 'currdrugs':
                        # print(key, value)
                        session = 'ses_' + str(repeat_instance)
                       
                        if kelements[-1] == 'currdrugs':
                            k = "_".join(kelements[:-1])
                        if key.startswith('curr_'):
                            k = '_'.join(kelements[1:])
                        elif key.endswith('currdrugs'):
                            k = '_'.join(kelements[:-1])
                        elif key.startswith('currdrugs_daily'):
                            k = '_'.join(kelements[2:])
                        
                        fieldstr = str("{assessments: { currdrugs: { redcap_repeat_instance }")
                        index_fields = [fieldstr]
                        match_criteria = {'_key': narc_id, 'assessments': { 'currdrugs': { 'redcap_repeat_instance': repeat_instance}}}
                        # print(update_data)
                    
                    update_data = { 'assessments': { repeat_instrument: { session: {k: value} } } }

                    
                elif 'ema' in key:
                    
                    session = 'ses_' + event_name.split('_')[2]
                    if key.startswith('ema_'):
                        key = '_'.join(key.split('_')[1:])
                    if 'complete' in key:
                        key = 'complete'
                    # date = subject['asi_date']
                    update_data = { 'assessments': { 'ema': { session: {key: value } }} }
              
                    
                elif 'panas' in key:
                    date = subject['panas_date']
                    
                    if 'complete' in key:
                        k = 'complete'
                    
                    if key.startswith('panas'):
                        k = '_'.join(key.split('_')[1:])
                    try: update_data.update({ 'assessments': { 'panas':  {k: value} } })
                    except: pass
              
                elif any (x in assessments for x in kelements):
                        
                    if 'strap' in key or 'nada' in key and not 'complete' in key:
                        k = '_'.join(kelements[2:])
                        assessment = '_'.join(kelements[0:2])
                        
                        # print('assessment: ', assessment)
                    
                    elif 'non_dual' in key or 'aliens' in key:
                        assessment = assessment
                        k = kelements[-1]
                    else: 
                        if len(kelements) < 2:
                            k = '_'.join(kelements[1:])
                            assessment = kelements[0]
                        else: 
                            k = kelements[-1]
                            assessment = kelements[0]
                    if hasComplete(key) != None:
                        k, assessment = hasComplete(key)
                        # print(k, assessment)
                        
                                 
                    q_date = assessment + '_date'
              
                    try: update_data = { 'assessments': { assessment: {k: value } } }
                    except: pass
                    
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
                        kelements[0] = 'curr_drugs'
                        k = '_'.join('_'.join(key.split('_currdrugs')).split('currdrugs_'))
                    
                    update_data = { 'tasks': { 'curr_drugs': { session: { kelements[0]: { k: value } } } } }
                
                elif key.startswith('bis'):
                    assessment = 'bis'
                    k = "_".join(key.split('bis')[1:])
                    update_data = {'assessments': { assessment:{ k: value}}}
                
                else:
                    for i in kelements:
                        if len(i) > 5:
                            uncaught = { key : value}
                            # print("\n\n", event_name, uncaught, repeat_instrument, "\n\n")
                        else:
                            continue
                    # print(event_name)
                    # print("Unmatched criteria: ")
                    # print(key, value)
                    continue
                if len(update_data) > 0 and len(group) > 0:
                    update_data.update({"group": group })

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
                try:                
                    updateArango(arango_collection, narc_id, update_data)
                except: 
                    print("Could not update record with data:\n", update_data)

               