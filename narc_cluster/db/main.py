from arango_queries.respAccrossSessions import respAccrossSessions
from arango_queries.wasi import wasiUpdate
from arango_queries.wrat import wratUpdate
from arango_queries.wasi import wasiUpdate
from migrations.redcap.records import addRecords
from migrations.redcap.mssm.records import mssmRecords
from migrations.redcap.phi_report import phiReport
# from migrations.redcap.instrument_event_mappings import allInstruments
from migrations.redcap.enrollment import addEnrollments

from transformations.enrollment_group import xfrmGroupCode
from transformations.moveRecord import moveRecord

from excel_conv.forPrediction import forPrediction
from excel_conv.mri_data import mriData

from file_server.add_more import addMoreFiles
from file_server.add_baseline import addBaselineFiles

import json
from utils.log import log

debug = True
print(globals()['debug'])
# globals()['debug'] = True
log("Test")


moveRecord('49')
'''
STEP 1: import enrollment data
'''
def Step1():
    log("Adding enrollment data...\n")
    addEnrollments()
    # change group code from numbers to letters (HC, OUD, CUD, IED)
    log("Transforming enrollment group codes...\n")
    # xfrmGroupCode()
    # log("Adding PHI report")
    # phiReport()
# try:
# Step1()
# except: 
#     log("Step 1 failed!")

'''
STEP 2: import RedCap data
'''
# addRecords()
# # mssmRecords()
# wasiUpdate()
# wratUpdate()

'''
STEP 3: import MRI task/analysis data
'''
# forPrediction()
# mriData()
'''
STEP 4: import file server MRI path data
'''
def Step4():
    # crawlDirs()
    addMoreFiles()
    # addBaselineFiles()
# try: Step4()
# except: pass

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