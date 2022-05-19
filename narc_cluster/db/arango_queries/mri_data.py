from db.utils.dbConnect import getCollection
from db.utils.dbUpdate import updateArango

def mriData(select_task):
    db, collection = getCollection('MORE', 'subjects3')

    cursor = db.aql.execute(
        'FOR subject IN subjects3 \
            FILTER subject.tasks != null \
            RETURN { narc_id: subject._key, tasks: subject.tasks }',
        batch_size=1
    )
    
    subjects = []
    all_taskdata_paths = []
    mri_data = []
    for subject in cursor:
        for task, data in subject['tasks'].items():
            for ses in subject['tasks'][task]:
                if ses.startswith('ses_'):
                    # Get all imaging data for task
                    mri_data =subject['tasks'][task][ses]['mri_data']
                    for filename, path in mri_data.items():  
                        # print(filename, path)
                        if 'nii.gz' in filename:
                            all_taskdata_paths.append(mri_data[filename]) # same as calling path
                    
                    sst_data = subject['tasks']['sst'][ses]
                    scores_data = subject['tasks']['sst'][ses]['scores']
               
                    mri_data.append(data)                        
        
    return mri_data
   
   
    
    