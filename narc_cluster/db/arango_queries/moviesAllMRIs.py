from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
from configs import arango

def groupQuery():
    db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])

    cursor = db.aql.execute(
        'FOR s IN subjects \
            movie_mris = s.tasks.movie.raw_data != null \
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