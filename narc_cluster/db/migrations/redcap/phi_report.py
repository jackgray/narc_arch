#!/usr/bin/env python

from datetime import date

from narc_cluster.db.configs.reports import reports
from narc_cluster.db.utils.redcapConnect import redcapConnect
from narc_cluster.db.utils.dbConnect import dbConnect
from narc_cluster.db.utils.dbUpdate import updateArango

def phiReport():
    db, collection = dbConnect()    # Get arango db and collection objects
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
            # print(update_data)
            updateArango(db, subject['record_id'], update_data)                   