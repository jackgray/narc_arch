#!/usr/bin/env python

from redcap import Project

from ..configs import redcap, arango 
from narc_cluster.db.redcap_queries.reports import reports
from narc_cluster.db.dbConnect import dbConnect
from narc_cluster.db.dbUpdate import updateArango

def phiReport():
    
    db = dbConnect()
    ############  PyCap Setup ####################
    URL = redcap.config['api_url']
    TOKEN = redcap.config['api_token']
    proj = Project(URL, TOKEN)


    phi_emergency = proj.export_report(reports['phi_emergency'], format_type='json')
    
    for subject in phi_emergency:
        # print('\n')
        if subject['redcap_event_name'] == 'screening_arm_1':
            update_data = { 'dob': subject['phi_dob']}
            print(update_data)
            updateArango(db, subject['record_id'], update_data)
            # for k,v in subject.items():
            #     if len(str(v)) > 0 and str(v) != '0':
            #         # print(k, ": ", v)
            #         # print(update_data)
                    
                    
                
phiReport()