import json
from arango import ArangoClient
from redcap import Project
from db.configs.reports import reports
from db.utils.dbConnect import getCollection
from db.utils.redcapConnect import redcapConnect
from db.configs import arango, redcap, mongo

from pymongo import MongoClient

def addEnrollments():
    client = MongoClient(mongo.config['endpoint'])
    mongo_collection = client.more['subjects']

    db, arango_collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
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
        
            
        # print("Narc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\nUD Group :", enrollmentGroup, "\n")
        
        update_data = { '_key': narc_id,
                       'record_id': record_id, 
                       'group': enrollmentGroup,
                       'contact': {
                           'name': {
                               'first': fname,
                               'last': lname
                           },
                           'phone': subject['phonenum'],
                       },
                       'recruitment': {
                            'date': subject['recruitment_date'].strip(),
                            'location': str(subject['recruitment_location']).strip(),
                            'location_other': str(subject['recruitment_location_other']).strip(),
                            'meets_criteria': subject['ie_enrollment_group'],
                            'recruited_from': subject['recruitment_location'] or subject['recruitment_location_other']                      
                    }}
        print(json.dumps(update_data))
        arango_collection.insert(update_data)
        # for k, v in subject.items():
        #     # print(k,v)
        #     if len(v) >0:
        #         update_data.update({k:v})
                
      
        # print(json.dumps(update_data, indent=2))
        # db.insert_one(update_data)
        # db.delete_one({'_id': narc_id})
        # data = db.find_one({'_id': narc_id})
        # print(data)
