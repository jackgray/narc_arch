#!/usr/bin/env python

from arango import ArangoClient
import requests  


from redcap import Project
from config import config 

#############  ArangoDB Setup  #############

client = ArangoClient(hosts=config['arango_endpoint'])  # Replace this with env variable
print("Setting up client object for ", client)
# Connect to system as root - returns api wrapper for "_system" database
sys_db = client.db('_system', verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to system db: ", sys_db)
# Connect to db as root user - returns api wrapper for this database 
db = client.db(config['db_name'], verify=False, username=config['sys_dbName'], password=config['arango_root_pass'])
print("Connected to db: ", db)
# Create collection if not exist - return api for collection 
if db.has_collection(config['collection_name']):
    print("Found collection: ", config['collection_name'])
    subj_collection = db.collection(config['collection_name'])
else:
    print("Collection '", config['collection_name'], "' doesn't exist. Creating it now.")
    subj_collection = db.create_collection(config['collection_name'])

# create hash index for collection 
print("Creating hash index.")
subj_collection.add_hash_index(fields=['narc_id'], unique=True)

subj_collection.truncate() 



#################  RedCap API setup   ###################


############ using PyCap ####################
URL = config['api_url']
TOKEN = config['api_token']
proj = Project(URL, TOKEN)
print(proj)
reports = dict(
    enrollment = '21141'
)

enrollment_rpt = proj.export_report(report_id=reports['enrollment'])
    
##########  ARANGO DB INSERTION #####################

    # db.collection('subjects').insert({'narc_id': enrollment['narc_id']})

# Begin batch execution via context manager. This returns an instance of
# BatchDatabase, a database-level API wrapper tailored specifically for
# batch execution. The batch is automatically committed when exiting the
# context. The BatchDatabase wrapper cannot be reused after commit.
with db.begin_batch_execution(return_result=True) as batch_db:

    # Child wrappers are also tailored for batch execution.
    batch_aql = batch_db.aql
    batch_col = batch_db.collection(subj_collection)

    # API execution context is always set to "batch".
    assert batch_db.context == 'batch'
    assert batch_aql.context == 'batch'
    assert batch_col.context == 'batch'

    for subject in enrollment_rpt:
    
        print("\nNarc ID: ", subject['narc_id'], "\nRecord ID: ", subject['record_id'], "\nName: ", subject['lname'])

        # db.collection('subjects').insert({'narc_id': enrollment['narc_id']})

        # BatchJob objects are returned instead of results.
        job_narcId = batch_col.insert({'narc_id': subject['narc_id']})
        job_recordId = batch_col.insert({'record_id': subject['record_id']})
        job_name = batch_col.insert({ 'name': [
            {'first_name': subject['fname']}, 
            {'last_name': subject['lname']}
            ]})
        job_phone = batch_col.insert({'phone': subject['phonenum']})
        job_recrtDate = batch_col.insert({'recruitment_date': subject['recruitment_date']})
        job_enrlGroup = batch_col.insert({'enrollment_group': subject['ie_enrollment_group']})
        job_meetsCriteria = batch_col.insert({'meets_criteria': subject['ie_enrollment']})

        
        job_narcId = batch_aql.execute('RETURN 100000')
        job_recordId = batch_aql.execute('INVALID QUERY')  # Fails due to syntax error.

# Upon exiting context, batch is automatically committed.
# assert 'Kris' in students
# assert 'Rita' in students

# Retrieve the status of each batch job.
for job in batch_db.queued_jobs():
    # Status is set to either "pending" (transaction is not committed yet
    # and result is not available) or "done" (transaction is committed and
    # result is available).
    assert job.status() in {'pending', 'done'}

# Retrieve the results of successful jobs.
# metadata = job_narcId.result()
# assert metadata['_id'] == 'students/Kris'

# metadata = job2.result()
# assert metadata['_id'] == 'students/Rita'

# cursor = job3.result()
# assert cursor.next() == 100000

# If a job fails, the exception is propagated up during result retrieval.
try:
    result = job4.result()
except AQLQueryExecuteError as err:
    assert err.http_code == 400
    assert err.error_code == 1501
    assert 'syntax error' in err.message

# Batch execution can be initiated without using a context manager.
# If return_result parameter is set to False, no jobs are returned.
batch_db = db.begin_batch_execution(return_result=False)
batch_db.collection('students').insert({'_key': 'Jake'})
batch_db.collection('students').insert({'_key': 'Jill'})

# The commit must be called explicitly.
batch_db.commit()
assert 'Jake' in students
assert 'Jill' in students
