from db.configs.arango import config
from db.calculated_fields.wrat import wratCalc
from db.utils.dbConnect import dbConnect
from db.utils.dbUpdate import updateArango

def wratUpdate():
    db, collection = dbConnect()

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
