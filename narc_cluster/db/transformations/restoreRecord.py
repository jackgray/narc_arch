#!/usr/bin/env python

from redcap import Project
from utils.redcapConnect import redcapConnect
from os import path

import json

def restoreRecord(text_file, project, arm):   
    print("Looking for record in project", project)
    proj = redcapConnect(project)
    record = {}
    # open text file and convert to json
    with open(text_file, 'r') as fh:
        # list = fh.split
        for line in fh:
            key = line.split('=')[0].replace('(', '___').split(')')[0].strip()
            choice_ans = line.split('=')
            value = line.split('=')[-1].strip().replace(',', '').replace("'", '')
            if value == 'checked':
                value = '1'
            elif value == 'unchecked':
                value = '2'
            else:
                print("\n Possible invalid format! ", value)
            record[key] = value
    record['redcap_event_name'] = 'screening_arm_2'
    record['redcap_repeat_instance'] = ''
    record['redcap_repeat_instrument'] = ''
    # print(json.dumps(record))
    record = [record]
    # print(record['record_id'])
    print(json.dumps(record, indent=4))
    try:
        print("\nImporting record... ")
        # print(record[0]['redcap_event_name'])
        res = proj.import_records(record, import_format='json')
        print("Successfully updated RedCap record for project '", project, "', arm ", arm, '\n', res)
    except Exception as e:
        # print("\nFailed to update RedCap record ", record_id, " for project '", project, "', arm ", arm, '\n\n')
        print(e)
        print("Please make sure you are entering the project name in the proper format, are entering the record ID, not the narc_id, and that the record exists.")
        print(e)