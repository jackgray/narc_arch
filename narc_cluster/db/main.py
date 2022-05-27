from arango_queries.respAccrossSessions import respAccrossSessions
from migrations.redcap.records import addRecords
from migrations.redcap.mssm.records import mssmRecords
# from migrations.redcap.instrument_event_mappings import allInstruments
from migrations.redcap.enrollment import addEnrollments

from transformations.enrollment_group import xfrmGroupCode

from excel_conv.forPrediction import forPrediction
from excel_conv.mri_data import mriData

from file_server.add_more import addMoreFiles
from file_server.add_baseline import addBaselineFiles

import json

'''
STEP 1: Create assessment/task vertices
'''
# allInstruments()

'''
STEP 1: import enrollment data
'''
# addEnrollments()
# change group code from numbers to letters (HC, OUD, CUD, IED)
# xfrmGroupCode()

'''
STEP 2: import RedCap data
'''
# addRecords()
# mssmRecords()

'''
STEP 3: import MRI task/analysis data
'''
# forPrediction()
# mriData()
'''
STEP 4: import file server MRI path data
'''
# crawlDirs()
addMoreFiles()
# addBaselineFiles()

# ema_sessions = respAccrossSessions('choice')

# print(ema_sessions)
# for i in sescount:
#     try: print(ema_sessions[i]['responses'])
#     except: pass
    
#     print(i)
    # ema_sessions = ema_sessions.merge()
# for i in ema_sessions:
#     print()
#     print(i)

    
#     try: print(i[session]['responses'])
#     except: pass
    # for k,v in i['ema']['sessions'].items():
    #     try: print(k, v['3'])
    #     except: pass
    
# records()