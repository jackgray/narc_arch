#!/usr/bin/env python

from redcap import Project
from utils.redcapConnect import redcapConnect
from os import path

import json

def moveRecord(record_id, arm, project):   
    print("Looking for record in project", project)
    proj = redcapConnect(project)
    record_id = [record_id] # PyCap function takes array of record ids, but we are using it singularly
    old_record = proj.export_records(format_type='json', record_type='flat', records=record_id, raw_or_label='raw', export_blank_for_gray_form_status=False)
    record = old_record
    for i in range(len(record)):
        record[i]['redcap_event_name'] = 'screening_arm_' + arm
        record[i].pop('cocaine_selective_severity_assessment_cssa_complete', None)
        record[i].pop('items_cocaine_craving_scale_cq_complete')
        record[i].pop('obsessivecompulsive_cocaine_scale_occs_complete')
        record[i].pop('cocaine_negative_consequences_checklist_cncc_complete')
    
    # Backup original record
    try:
        print("\nCreating local file to back up original record: ", res)
        filename = path.join(path.expanduser('~'), record_id + '_backup.json')
        print('Path: ', filename)
        try:
            with open(filename, 'w') as f:
               json.dump(old_record, f)
            # Delete only if the backup saved successfully
            try:
                print("Successfully saved backup of record locally. Removing old record.")
                res = proj.delete_records(record_id)
                try:
                    proj.import_records(record)
                except Exception as e:
                    print(e)
            except Exception as e: 
                print("Encountered error while trying to delete old record from redcap")
        except Exception as e:
            print(e)
            print("\nFailed to back up RedCap record locally: ", old_record)
            print("Please copy and paste this text to your local machine as '", filename, "', then manually remove the old record on RedCap.")
            try:
                print("\nImporting record with changes: ")
                print(record[0]['redcap_event_name'])
                proj.import_records(record)
                print("Successfully updated RedCap record ", record_id, " for project '", project, "', arm ", arm)
            except Exception as e:
                print("\nFailed to update RedCap record ", record_id, " for project '", project, "', arm ", arm, '\n\n')
                print(e)
                print("Please make sure you are entering the project name in the proper format, are entering the record ID, not the narc_id, and that the record exists.")
    except Exception as e:
        print("\nCould not create file: ", filename)
        print(e)
        print("\nFailed to back up RedCap record locally: ", old_record)
        print("Please copy and paste the above JSON to your local machine as '", filename, "', then manually remove the old record on RedCap.")
        try:
            print("\nImporting record with changes: ")
            print(record[0]['redcap_event_name'])
            proj.import_records(record)
            print("Successfully updated RedCap record ", record_id, " for project '", project, "', arm ", arm)
        except Exception as e:
            print("\nFailed to update RedCap record ", record_id, " for project '", project, "', arm ", arm, '\n\n')
            print(e)
            print("Please make sure you are entering the project name in the proper format, are entering the record ID, not the narc_id, and that the record exists.")



    