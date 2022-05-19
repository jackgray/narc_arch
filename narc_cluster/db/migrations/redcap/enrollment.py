from arango import ArangoClient
from redcap import Project
from db.configs.reports import reports
from db.utils.dbConnect import getCollection
from db.utils.redcapConnect import redcapConnect
from db.configs import arango, redcap

db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
proj = redcapConnect()

# Contains all responses from enrollment report by report_id
enrollment_rpt = proj.export_report(report_id=reports['enrollment'], format_type='json')

for subject in enrollment_rpt:
    narc_id = str(subject['narc_id']).strip()
    record_id = str(subject['record_id']).strip()
    lname = str(subject['lname'])
    fname = str(subject['fname'])
    enrollmentGroup = str(subject['ie_enrollment_group'])
    if narc_id.startswith('S'):
        narc_id = narc_id.replace('S', '')
        # print("Dropped 'S' from narc ID: ", narc_id)
        
    print("Narc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\nUD Group :", enrollmentGroup, "\n")
    
    print("\nInserting data for subject ", narc_id)
    collection.insert({
        '_key': narc_id, 
        'record_id': record_id, 
        'group': enrollmentGroup, 
        'name': {
            'first': fname,
            'last': lname
            },
        })

