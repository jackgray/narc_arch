from configs.arango import config
from calculated_fields.wrat import wratCalc
from utils.dbConnect import getCollection, getGraph
from utils.dbUpdate import updateArango
from utils.graphIt import graphIt

def wratUpdate():
    db, collection = getCollection(config['db_name'], config['collection_name'])
    db, graph = getGraph(config['db_name'], config['graph_name'])

    cursor = db.aql.execute(
        'FOR subject IN MORE_Subjects \
            RETURN { narc_id: subject._key, total_reading: subject.assessments.wrat.total_reading, age: subject.age, version: subject.assessments.wrat.version }',
        batch_size=1
    )
    # cursor = collection.find({'record_id': subject['record_id']})

    # 0 = blue , 1 = tan
    for subject in cursor:
        try:
            # print(subject)  
            version = subject['version']
            total = subject['total_reading']
            age = subject['age']
            narc_id = subject['narc_id']
            
            update_data = wratCalc(int(total), version, round(float(age)) )
            # update_data.update({'_key': subject['narc_id']})
            print("TO UPDATE", update_data)
            print(narc_id)
            updateArango(collection, narc_id, update_data),
            graphIt(graph, collection, narc_id, 'WRAT', 'standard_score', update_data['assessments']['wrat']['standard_score'])

            graphIt(graph, collection, narc_id, 'WRAT', 'grade_equivalent', update_data['assessments']['wrat']['ge'])

            graphIt(graph, collection, narc_id, 'WRAT', 'version', update_data['assessments']['wrat']['version'])
    
        except: 
            print("Couldn't get age or dob to perform calculation on subject ", subject)
            # print('subject: ', subject)
