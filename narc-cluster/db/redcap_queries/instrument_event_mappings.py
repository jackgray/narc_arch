
import json
from redcap import Project
from all_records import allRecords
from config import config

def allInstruments():
    ############  PyCap Setup ####################
    URL = config['api_url']
    TOKEN = config['api_token']
    proj = Project(URL, TOKEN)
    
    instrument_events = proj.export_instrument_event_mappings(format_type='json')
    repeating_instruments = proj.export_repeating_instruments_events(format_type='json')
    
    for inst in repeating_instruments:
        form = inst['form_name']
        event = inst['event_name']
        
        # insts.append(json.loads(form))
        print('fuck')
        print(json.loads(form))
        
        # print(json.dumps(insts))

    return insts
    
    # unique_event_name = event_name
    # form = form_name
    
print(allInstruments())