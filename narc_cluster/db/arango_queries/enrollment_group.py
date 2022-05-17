from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.dbUpdate import updateArango

def enrollmentGroup():
    db, collection = getCollection('MORE', 'subjects3')

    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            FILTER subject.enrollment_group != null \
            RETURN { narc_id: subject._key, enrollment_group: subject.enrollment_group }',
        batch_size=1
    )
    
    # for subject in cursor:
        # score calculated from total (raw) score. make sure it exists first
        # print(subject)
        # if subject['enrollment_group']:        
        #     update_data = wasiCalc(int(subject['total']), round(float(subject['age'])) )
        #     print(update_data)
        #     updateArango(collection, subject['narc_id'], update_data),
    return cursor
   
    
    