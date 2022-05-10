#!/usr/bin/env python

from redcap import Project

from config import config 
from reports import reports
from format_redcap_res import formatResp


def allReports():
    ############  PyCap Setup ####################
    URL = config['api_url']
    TOKEN = config['api_token']
    proj = Project(URL, TOKEN)

    for report_name, report_id in reports.items():
        print("\nExporting records for report: ", report_name, ' for all subjects.')
        
        reports_all_subjects = proj.export_report(report_id, format_type='json')
        
        for report in reports_all_subjects:
            print('\n')
            
            for k,v in report.items():
                
                if len(str(v)) > 0 and str(v) != '0':
                    print(k, ": ", v)
                    
            
        
allReports()