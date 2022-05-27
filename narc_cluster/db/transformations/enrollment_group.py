from arango_queries.group import groupQuery
from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
from configs.arango import config

def xfrmGroupCode():
    groups = groupQuery()   # returns dict of db query of narc_ids and groups
    db, collection = getCollection(config['db_name'], config['collection_name'])
    
    for subject in groups:
        print(subject)
        if config['collection_name'] == 'Baseline3T_Subjects':
            if subject['group'] == '1':
                update_data = { 'group': 'HC' }
            elif subject['group'] == '2':
                update_data = { 'group': 'CUD' }
            elif subject['group'] == '3':
                update_data = { 'group': 'IED'}
            elif subject['group'] == '4':
                update_data = {'group': 'CUD/IED'}
            else:
                update_data = { 'group': subject['group']}   
        elif config['collection_name'] == 'MORE_Subjects': 
            if subject['group'] == '1':
                update_data = { 'group': 'HC' }
            elif subject['group'] == '2':
                update_data = { 'group': 'OUD' }
            elif subject['group'] == '3':
                update_data = { 'group': 'CUD'}
            else:
                update_data = { 'group': subject['group']}
        
        print(update_data)
        updateArango(collection, subject['narc_id'], update_data)
        
        # prune 
        # aql.execute({
        #     '
        #     FOR subject in subjects3
        #         FILTER subject.group == None
        #         REMOVE { group: subject.group } in subjects3
        #     '
        # })