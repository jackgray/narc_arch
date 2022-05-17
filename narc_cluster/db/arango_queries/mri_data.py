from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.dbUpdate import updateArango

def mriData():
    db, collection = getCollection('MORE', 'subjects3')

    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            FILTER subject.mri_data != null \
            RETURN { narc_id: subject._key, mri_data: subject.mri_data }',
        batch_size=1
    )
    
    for subject in cursor:
        if subject['mri_data']: 
            for session in subject['mri_data']:
                if subject['mri_data'][session]['func']:
                    print(subject['mri_data'][session]['func'])     
    return cursor
   
    
    