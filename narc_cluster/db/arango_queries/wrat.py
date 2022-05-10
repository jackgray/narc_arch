from arango import ArangoClient
from narc_cluster.db.configs.arango import config
from narc_cluster.db.calculated_fields.wrat import wratCalc
from narc_cluster.db.dbConnect import dbConnect
from narc_cluster.db.dbUpdate import updateArango
# from ..redcap_queries.config import config

def wratUpdate():
    db, collection = dbConnect()
    
    # subjects = db.collection(config['collection_name'])
    # # subjects.all()
    # print('subjs', subjects)

    # FYI: tan = 
    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            RETURN { narc_id: subject._key, total: subject.battery.wrat.total.reading, age: subject.age, blue: subject.battery.wrat.blue, tan: subject.battery.wrat.tan }',
        batch_size=1
    )
    
    for subject in cursor:
        if subject['total']:
            # print(subject)  
            if subject['blue']:
                version = 'blue' 
            if subject['tan']:
                version = 'tan'
            
            update_data = wratCalc(int(subject['total']), version, round(float(subject['age'])) )
        
            print(update_data)
            print(subject['narc_id'])
            updateArango(collection, subject['narc_id'], update_data),
    # # cursor.id
        # print(cursor)
        
    # while cursor.has_more():
    #     subject = cursor.next()
    #     print(subject)
        
    # cursor.fetch() 
    # print("batch:", cursor.batch())
   
    
    