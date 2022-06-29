import json
from arango import ArangoClient
from redcap import Project
from utils.dbConnect import getCollection, getGraph, getVertexCollection
from utils.redcapConnect import redcapConnect
from utils.log import log
from configs import arango, redcap, mongo
from configs.reports import reports

from pymongo import MongoClient

def addEnrollments():
    
    # client = MongoClient(mongo.config['endpoint'])
    # mongo_collection = client.more['subjects']

    db, arango_collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    narc_dev_db, graph = getGraph(arango.config['db_name'], arango.config['graph_name'])
    log("Retrieving subject vertices")
    subj_vertices = getVertexCollection(graph, arango.config['collection_name'])
    
    log("Authenticating RedCap...")
    proj = redcapConnect()
    # Contains all responses from enrollment report by report_id
    enrollment_rpt = proj.export_report(report_id=reports['enrollment'], format_type='json')
        
    for subject in enrollment_rpt:
        
        narc_id = str(subject['narc_id']).strip()
        record_id = str(subject['record_id']).strip()
        lname = str(subject['lname'])
        fname = str(subject['fname'])
        group = str(subject['ie_enrollment_group'])
        race = str(subject['race'])
        ethnicity = str(subject['ethnicity'])
        handedness = str(subject['handedness'])
        if str(subject['phi_sex']) == '2':
            sex = 'F'
        elif str(subject['phi_sex']) == '1':
            sex = 'M'
        else:
            sex = 'O'
        
        if str(subject['gender']) == '1':
            gender = 'M'
        elif str(subject['gender']) == '2':
            gender = 'F'
        else:
            pass
        
        if race == '1':
            race = 'White'
        elif race == '2':
            race = 'Black'
        elif race == '3':
            race = 'Asian'
        elif race == '4':
            race = '4'
        elif race == '5':
            race = 'Native American'
        
        if ethnicity == '1':
            ethnicity = 'Hispanic'
        elif ethnicity == '2':
            ethnicity = 'Non-hispanic'
        
        if arango.config['collection_name'] == 'Baseline3T_Subjects':
            if group == '1':
                group = 'HC'
            elif group == '2':
                group = 'CUD'
            elif group == '3':
                group = 'IED'
            elif group == '4':
                group = 'CUD/IED'
            else:
                pass  
        elif arango.config['collection_name'] == 'MORE_Subjects': 
            if group == '1':
                group = 'HC'
            elif group == '2':
                group = 'OUD'
            elif group == '3':
                group = 'CUD'
            else:
                pass
        
        if handedness == '1':
            handedness = 'R'
        elif handedness == '2':
            handedness = 'L'
        elif handedness == '3':
            handedness = 'A'
        else:
            pass
        
        
        if narc_id.startswith('S'):
            narc_id = narc_id.replace('S', '')
            # log("Dropped 'S' from narc ID: ", narc_id)
            
        # log("Narc ID: ", narc_id, "\nRecord ID: ", record_id, "\nName: ", lname, "\nUD Group :", enrollmentGroup, "\n")
        update_data = { '_key': narc_id,
                        'record_id': record_id, 
                        'group': group,
                        # maybe don't include identifying info for security... this stuff doesn't need to be easily accessed
                    #    'contact': {
                    #        'name': {
                    #            'first': fname,
                    #            'last': lname
                    #        },
                    #        'phone': subject['phonenum'],
                    #    },
                        'age': subject['age'],
                        'dob': subject['phi_dob'],
                        'sex': sex,
                        'gender': gender,
                        'handedness': handedness,
                        'recruitment': {
                            'date': subject['recruitment_date'].strip(),
                            'location': str(subject['recruitment_location']).strip(),
                            'location_other': str(subject['recruitment_location_other']).strip(),
                            'meets_criteria': subject['ie_enrollment_group'],
                            'recruited_from': subject['recruitment_location'] or subject['recruitment_location_other']                      
                    }}
        
        log(update_data)
        try:
            subj_vertices.insert(update_data)
        except:
            log('Data already inserted. Asserting new data as update.')
            # update_data.update({'_id': narc_id})
            # log(update_data)
            try:
                subj_vertices.update_match({'_key': narc_id}, update_data)
            except: 
                log("Error updating subject vertex")
        # arango_collection.insert(update_data)
        # for k, v in subject.items():
        #     # log(k,v)
        #     if len(v) >0:
        #         update_data.update({k:v})
                
      
        # log(json.dumps(update_data, indent=2))
        # db.insert_one(update_data)
        # db.delete_one({'_id': narc_id})
        # data = db.find_one({'_id': narc_id})
        # log(data)
