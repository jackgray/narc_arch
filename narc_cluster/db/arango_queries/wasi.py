from db.calculated_fields.wasi import wasiCalc
from db.utils.dbConnect import dbConnect
from db.utils.dbUpdate import updateArango

def wasiUpdate():
    db, collection = dbConnect()

    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            RETURN { narc_id: subject._key, total: subject.battery.wasi.total, age: subject.age }',
        batch_size=1
    )
    
    for subject in cursor:
        # score calculated from total (raw) score. make sure it exists first
        if subject['total']:        
            update_data = wasiCalc(int(subject['total']), round(float(subject['age'])) )
            print(update_data)
            updateArango(collection, subject['narc_id'], update_data),

   
    
    