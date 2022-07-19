#!/usr/bin/env python

from redcap import Project
from utils.redcapConnect import redcapConnect
from os import path

import json

def moveRecord(record_id, arm, project):   
    print("Looking for record in project", project)
    proj = redcapConnect(project)
    # print(proj.field_names, proj.is_longitudinal, proj.def_field)
    record_id = [record_id] # PyCap function takes array of record ids, but we are using it singularly
    record = proj.export_records(format_type='json', record_type='flat', records=record_id, raw_or_label='raw', export_blank_for_gray_form_status=False)
    # print(record[0])
    for i in range(len(record)):
        record[i]['redcap_event_name'] = 'screening_arm_' + arm
        # new_record = map(lambda x: str.replace(x,'screening_arm_1', 'screening_arm_2'), record)
        record[i].pop('cocaine_selective_severity_assessment_cssa_complete', None)
        record[i].pop('items_cocaine_craving_scale_cq_complete')
        record[i].pop('obsessivecompulsive_cocaine_scale_occs_complete')
        record[i].pop('cocaine_negative_consequences_checklist_cncc_complete')
  
        
    
    print("Importing record with changes: ")
    print(record[0]['redcap_event_name'])
    
    try:
        proj.import_records(record)
        print("Successfully updated RedCap record ", record_id, " for project '", project, "', arm ", arm)
    except Exception as e:
        print("Failed to update RedCap record ", record_id, " for project '", project, "', arm ", arm, '\n\n')
        print(e)

    print("Cleaning up old record...")
    try:
        res = proj.delete_records(record_id)
        print("Successfully removed old record. Saving to local file as backup: ", res)
        filename = path.join(path.expanduser('~'), record_id + '_backup.json')
        print('Path: ', filename)
        try:
           with open(filename, 'w') as f:
               json.dump(res, f)
        except Exception as e:
            print("Failed to save RedCap record: ", res)
            print(e)
    except Exception as e:
        print("Could not remove old record: ", record_id)
        print(e)
        