#!/usr/bin/env python

from datetime import date
from configs import arango
from configs.reports import reports
from utils.redcapConnect import redcapConnect
from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango

def phiReport():
    db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])    # Get arango db and collection objects
    proj = redcapConnect()
    phi_emergency = proj.export_report(reports['phi_emergency'], format_type='json')
    
    # come back to fix leap years
    def age(birthdate):
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    
    def dob(age):
        today = date.today()
        yob = today.year - age
    
    for subject in phi_emergency:
        # print('\n')
        if subject['redcap_event_name'] == 'screening_arm_1':
            if len(subject['narc_id']) < 1:
                narc_id_cursor = collection.find({'record_id': subject['record_id']})
                for i in narc_id_cursor:
                    subject['narc_id'] = i['_key']
            else: 
                subject['narc_id'] = subject['narc_id'].replace('S', '')
            # calc age if missing and DOB found
            if len(subject['age']) < 1 and len(subject['phi_dob']) > 0:
                print(subject['phi_dob'])
                dob = subject['phi_dob'].split('-')
                print(dob)
                print("No age found. Calculating (WARNING: only returns rounded int).")
                subject['age'] = age(date(int(dob[0]), int(dob[1]), int(dob[2])))
                print(subject['age'])
            
            # calc DOB if missing and age found 
            if len(subject['phi_dob']) < 1 and len(subject['age']) > 0:
                print("missing dob")
            
            update_data = { 'dob': subject['phi_dob'], 'age': subject['age'] } 
            update_data.update({'_key': subject['narc_id']})
            print(update_data)
            try:
                print('updating phi info: ', update_data)
                updateArango(collection, subject['narc_id'], update_data)  
            except:
                print("Could not update subject with info ", subject)                 