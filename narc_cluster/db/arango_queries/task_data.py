from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.dbUpdate import updateArango

def taskData(task):
    db, collection = getCollection('MORE', 'subjects3')

    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            FILTER subject.tasks != null \
            RETURN { narc_id: subject._key, tasks: subject.tasks }',
        batch_size=1
    )
    
    subjects = []
    all_taskdata_paths = []
    returnable = []
    for subject in cursor:
        try:
            for ses in subject['tasks'][task]:
                if ses.startswith('ses_'):
                    # Get all imaging data for task
                    task_data =subject['tasks'][task][ses]
                    
                    scores_data = subject['tasks']['sst'][ses]['scores']
                
                    returnable.append(task_data['scores'])                        
        except: pass
    return returnable
   
   
    
    