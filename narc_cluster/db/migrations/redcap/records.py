#!/usr/bin/env python

from arango import ArangoClient, AQLQueryExecuteError
from pyArango.connection import *
from pyArango.graph import *
import requests  
import json
import jsonpickle
import re


from redcap import Project
from pymongo import MongoClient
from configs import mongo, redcap, arango 
from utils.dbConnect import getCollection, getGraph, getVertexCollection, getEdgeCollection, addEdge
from utils.graphIt import graphIt
from utils.dbUpdate import updateArango
# from reports import reports

def addRecords():
    missed = []
    collected = []
    
    arangodb, arango_collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    arangodb, graph= getGraph(arango.config['db_name'], arango.config['graph_name'])
    subject_vertices = getVertexCollection(graph, arango.config['collection_name'])
   
    mongodb = MongoClient(mongo.config['endpoint'])
    mongo_collection = mongodb.more.subjects
    
    ############  PyCap Setup ####################
    URL = redcap.config['api_url']
    TOKEN = redcap.config['more_token']
    proj = Project(URL, TOKEN)
    # print(proj.field_names, proj.is_longitudinal, proj.def_field)

    with open('/home/jackgray/Code/narc_arch/narc_cluster/db/migrations/redcap/all_records_raw.json') as json_file:
        all_records_fromfile = json.load(json_file)
        # print(all_records_fromfile)
        records = all_records_fromfile
    
    assessments = ['caars', 'sogs', 'surps', 'bai', 'bdi','hcq', 'bisbas', 'smast', 'sows', 'tsr', 'sds', 'tlfb', 'colorblind', 'menstrual_v2', 'menstrual', 'ftnd', 'spsrq', 'nada_t', 'nada', 'frsbe', 'mpq', 'strap_r', 'strap', 'staxi', 'ctq', 'pss', 'ffmq', 'wos_s', 'woss','aliens', 'cohs', 'mini', 'mcq']
    drugs = ['opioid', 'thc', 'alc', 'coc', 'barb', 'hall', 'sed', 'stim']
    asi_cat1s = [['lastuse'], ['abs'], ['abs_end'], 'dur_yrs', 'hx', 'quit_attempts']
    # asi_cat2s = [['lastuse']['amt', 'date', 'money'], ['abs']['longest', 'end'] ]
    last_instrument = 0
    print('awaiting response from server')
    for subject in records:
        subjcount=+1
        # print(subject)
     
        narc_id = str(subject['narc_id']).strip()
        current_data = arango_collection.find({'_key': narc_id})
        event_name = str(subject['redcap_event_name'])
        repeat_instrument = str(subject['redcap_repeat_instrument'])
        repeat_instance = subject['redcap_repeat_instance']
        record_id = str(subject['record_id']).strip()
       
        if narc_id.startswith('S'):
            narc_id = narc_id.replace('S', '')
        if len(narc_id) < 1:
            narc_id_cursor = arango_collection.find({'record_id': record_id})
            for i in narc_id_cursor:
                narc_id = i['_key']
        if len(narc_id) < 1:
            continue
            
        subj_data = {'_key': narc_id}
        if narc_id != '66666':
            for key,value in subject.items():
                itemcount=+1
                # print('ITEM COUNT ', itemcount)
                if len(str(value)) > 0 and str(value) != '0': 

                    kelements= key.split('_')
                    kelement_val = re.split('___', key)

                    subcat = kelement_val[0].split('_')
                    
                    if kelements[0]== 'asi':
                        questionnaire = 'asi'
                        print("\nASI")
                        if any (x in kelements[1] for x in drugs):
                            questionnaire = 'asi'
                            question = "_".join(kelements[2:])
                            # except: print("nope") 
                            # pass
                        
                            update_data = {'assessments': {questionnaire: { kelements[1]: { question: value } } } } 
                            # graph.link(asi_resp, _from, _id)
                        
                        # else:
                        question = '_'.join(kelements[1:])
                        update_data = {'assessments': {'asi': { question: value } } }
                        # graphIt(graph, arango.config['collection_name'], narc_id, questionnaire, question, value)

                        
                    elif kelements[0] == 'wasi':
                        print('\nWASI')
                        print(key, value)
                        question = '_'.join(kelements[1:])
                        questionnaire = 'wasi'
                        update_data = {'assessments': {'wasi': { question: value } } }
                          
                    
                    elif kelements[0] == 'wrat':
                        questionnaire = 'wrat'
                        print('\n\n\n\n\n\n\n\n\nWRAT\n\n\n\n\n\n\n\n')    
                        print(key, value) 
                        if kelements[1] == 'blue' or kelements[1] == 'tan': 
                            question = '_'.join(kelements[2:])         
                            update_data = {'assessments': {'wrat': {'version': kelements[1], question: value } } }
                        else:
                            question = '_'.join(kelements[1:])

                            update_data = {'assessments': {'wrat': { question: value } } }
                        print(update_data)
    # # '''

    # reports idea: assume all reports on redcap preceded with "toDB_ are legitimate. scan for all reports, add them based on their name by subject

    # '''
                    
                    # Case when record is from a repeat instrument
                    elif len(repeat_instrument) > 0:
                        if last_instrument == (repeat_instrument or 0):
                            count=+1
                        else:
                            count=0
                            last_instrument = repeat_instrument
                        # if repeat instrument is the same as last iteration, keep counting question #
                        # if new repeat instrument, start count over
                        
                        session = 'ses_' + str(repeat_instance)
                        if str(kelements[0]).strip() == repeat_instrument:
                            question = "_".join(kelements[1:])
                        else:
                            question = key
                            
                    #     ### CURRDRUGS_DAILY_INTERVIEW ########
                        if repeat_instrument == 'currdrugs':
                            # print(key, value)
                            session = 'ses_' + str(repeat_instance)
                        
                            if kelements[-1] == 'currdrugs':
                                question = "_".join(kelements[:-1])
                            if key.startswith('curr_'):
                                question = '_'.join(kelements[1:])
                            elif key.endswith('currdrugs'):
                                question = '_'.join(kelements[:-1])
                            elif key.startswith('currdrugs_daily'):
                                question = '_'.join(kelements[2:])
                            
                            fieldstr = str("{assessments: { currdrugs: { redcap_repeat_instance }")
                            index_fields = [fieldstr]
                            match_criteria = {'_key': narc_id, 'assessments': { 'currdrugs': { 'redcap_repeat_instance': repeat_instance}}}
                            # print(update_data)
                        
                        update_data = { 'assessments': { repeat_instrument: { session: {question: value} } } }
                        print(update_data)
                        
                    elif 'ema' in key:
                        
                        session = 'ses_' + event_name.split('_')[2]
                        if key.startswith('ema_'):
                            key = '_'.join(key.split('_')[1:])
                        if 'complete' in key:
                            key = 'complete'
                        # date = subject['asi_date']
                        update_data = { 'assessments': { 'ema': { session: {key: value } }} }
                        print(update_data)
                        
                    elif 'panas' in key:
                        date = subject['panas_date']
                        
                        if 'complete' in key:
                            key = 'complete'
                            questionnaire = 'panas'
                        
                        if key.startswith('panas'):
                            key = '_'.join(key.split('_')[1:])
                        try: 
                            update_data.update({ 'assessments': { 'panas':  {key: value} } })
                            print(update_data)
                        except: pass
                
                    elif any (x in assessments for x in kelements):
                        print(key, value)
                        if any (x in kelements[1] for x in drugs):
                            questionnaire = 'asi'
                            question = "_".join(kelements[2:])
                        
                            update_data = {'assessments': {questionnaire: { kelements[1]: { question: value } } } }                   
                            
                        if 'strap' in key or 'nada' in key and not 'complete' in key:
                            question = '_'.join(kelements[2:])
                            questionnaire = '_'.join(kelements[:2])
                            print('questionnaire: ', questionnaire)
                        elif kelements[0] == 'frsbe':
                            question = kelements[1]
                            questionnaire = 'frsbe'
                        elif 'non_dual' in key or 'aliens' in key:
                            questionnaire = kelements[-2]
                            question = kelements[-1]
                        elif 'hcq' in key:
                            question = "_".join(kelements[1:])
                            questionnaire = 'hcq'
                        # determine label index no.
                        else: 
                            if len(kelements) < 2:
                                question = '_'.join(kelements[1:])
                                questionnaire = kelements[0]
                            else: 
                                question = "_".join(kelements[1:])
                                questionnaire = kelements[0]
                        
                        if 'complete' in key:
                            # pass
                            # print(key)
                            question = 'complete'
                            questionnaire = kelements[-2]
                            print('IF COMPLETE')
                            print(questionnaire)   
                        
                        # try:
                        # graphIt(graph, arango.config['collection_name'], narc_id, questionnaire, question, value)
                        # except: 
                        #     print("\n\n\nUR A FAILURE")
                        q_date = questionnaire + '_date'
                
                        try: 
                            update_data = { 'assessments': { questionnaire: {question: value } } }
                            print(update_data)
                        except: 
                            print("FAILLLLLLLLEDDDD")
                            pass
                        
                    elif key.startswith('phi_'):
                        question = '_'.join(kelements[1:])
                        update_data = { 'phi': { question: value}}
                        # print(json.dumps(update_data))
                        
                    elif 'task_day' in event_name:
                        print("TASK DAY")
                        print(event_name)
                        print(key,value)
                        session = 'ses_' + str(event_name.split('_')[2])
                        
                        # print("_".join(kelements[0:2]))
                        if "_".join(kelements[0:2]) =='wos_s':
                            questionnaire = 'wos_s'
                            question = kelements[-1]
                            
                        elif kelements[0] in event_name:
                            question = key
                            questionnaire = kelements[0]
                        elif 'currdrugs' in key or kelements[0] == 'curr':
                            questionnaire = 'currdrugs'
                            if kelements[-1] == 'currdrugs':
                                question = "_".join(kelements[:-1])
                            elif kelements[-1] == 'complete':
                                question = 'complete'
                            else:
                                question = "_".join(kelements[1:])                                       
                        
                        else:
                            question = '_'.join(kelements[1:])
                            questionnaire = kelements[0]                      
                                                                        
                        if 'complete' in key:
                            question = 'complete'
                            if 'currstatus' in key or 'current_status' in key:
                                questionnaire = 'currstatus'
                                question = key
                                
                            # pass
                            # print(key)
                            else:
                                questionnaire = kelements[-2]
                                if questionnaire == 'woss':
                                    questionnaire = 'wos_s'
                                question = key
                                       
                        # if 'curr' in key:
                        #     kelements[0] = 'curr_drugs'
                        #     question = '_'.join('_'.join(key.split('_currdrugs')).split('currdrugs_'))
                        update_data = {'assessments': { questionnaire: { session: { question: value } } } }
                        print(update_data)
                    
                    else:
                        # print(event_name)
                        print("\n\nMISSSSEEDDDD")
                        print(key, value)
                        print(narc_id)
                        # print(update_data)
                        continue
                    
                    print('Attempting to update DB with data: ', update_data)
                    try:
                        update_data.update({"_key": narc_id })

                        # arango_collection.find_one_and_update({'_id': narc_id}, {'$set': update_data})
                        print('UPDATING DB')
                        print(update_data)
                    except: 
                        print("you done fucked up son")
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
                        print("FAILED TO UPDATE\n\n\n")
                    if 'questionnaire' in locals(): 
                        print("Graphing it")
                        try:
                            graphIt(graph, arango.config['collection_name'], narc_id, questionnaire, question, value)
                        except:
                            print("graph errored out for ", key, value)
                    # except: 
                    elif len(update_data) < 0:
                        print('Nothing in update body\n\n')
                    else:
                        print('\n\n\n\nFAILED TO UPDATE DB')
                        print(update_data)
                        print('\n\n')
                        
                    
                