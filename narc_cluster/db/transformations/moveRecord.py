#!/usr/bin/env python

from redcap import Project
from utils.redcapConnect import redcapConnect

import json

def moveRecord(record_id, arm='null', project='null'):   
     
    proj = redcapConnect()
    # print(proj.field_names, proj.is_longitudinal, proj.def_field)
    record_id = [record_id]
    record = proj.export_records(format_type='json', record_type='flat', records=record_id, raw_or_label='raw', export_blank_for_gray_form_status=False)
    print(record[0])
    # for i in range(len(record)):
    #     record[i]['redcap_event_name'] = 'screening_arm_2'
        # record[i] = 'record_id'
        # record[i]['record_id'] = record[i]['record']
        # record[i]
        # new_record = map(lambda x: str.replace(x,'screening_arm_1', 'screening_arm_2'), record_copy)
    
    # new_record = " ".join(record_copy.get(ele, ele) for ele in test_str.split())
    # print()
    # for i in new_record:
    #     print(i)\
    print("\nNew Record: \n\n")
    # print(record)
    # proj.import_records(record)
    