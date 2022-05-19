from narc_cluster.db.arango_queries.enrollment_group import groupQuery
from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.dbUpdate import updateArango

enrollment_groups = groupQuery()   # returns dict of db query of narc_ids and enrollment_groups
db, collection = getCollection('MORE', 'subjects3')

for subject in enrollment_groups:
    if subject['enrollment_group'] == '1':
        update_data = { 'enrollment_group': 'HC' }
    elif subject['enrollment_group'] == '2':
        update_data = { 'enrollment_group': 'OUD' }
    else:
        update_data = { 'enrollment_group': 'None'}
    
    updateArango(collection, subject['narc_id'], update_data)
    
    # prune 
    # aql.execute({
    #     '
    #     FOR subject in subjects3
    #         FILTER subject.enrollment_group == None
    #         REMOVE { enrollment_group: subject.enrollment_group } in subjects3
    #     '
    # })