from calculated_fields.wasi import wasiCalc
from utils.dbConnect import getCollection, getGraph
from utils.dbUpdate import updateArango
from configs import arango
from utils.graphIt import graphIt

def wasiUpdate():
    db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    db, graph = getGraph(arango.config['db_name'], arango.config['graph_name'])
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
            total = subject['total']
            age = subject['age']
            narc_id = subject['narc_id']
          
            update_data = wasiCalc(int(total), round(float(age)) )
            print("WASI UPDATE: ", update_data)
            updateArango(collection, narc_id, update_data),

   
            graphIt(graph, collection, narc_id, 'WASI', 't_score', update_data['assessments']['wasi']['t_score'])

            graphIt(graph, collection, narc_id, 'WASI', 'scaled_score', update_data['assessments']['wasi']['scaled_score'])
        except: 
            print("ERROR UPDATING WASI SCORES")