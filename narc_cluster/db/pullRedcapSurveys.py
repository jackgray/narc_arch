from redcap import Project 
from config import config

############ using PyCap ####################
URL = config['api_url']
TOKEN = config['api_token']
proj = Project(URL, TOKEN)
# print(proj.field_names, proj.is_longitudinal, proj.def_field)


# ############ REDCAP ALL Surveys COLLECTION #########################

# # redcap_surveys_collection = createCollection('redcap_surveys')

# all_instruments = proj.export_instrument_event_mappings(format_type='json')
# for instrument in all_instruments:
#     print('\n')
#     print(instrument)
#     unique_event_name = instrument['unique_event_name']
#     form = instrument['form']
#     # print('\n\n\n\n')
#     try:
#         all_surveys = proj.export_survey_participant_list(instrument=form, event=unique_event_name, format_type='json')
    
#         for survey in all_surveys:
#             print('SURVEY:')
#             print(survey)
#     except:
#         continue


############ REDCAP ALL Surveys COLLECTION #########################

# redcap_surveys_collection = createCollection('redcap_surveys')

field_names = proj.export_field_names(format_type='json')
for field_name in field_names:
    print('\n')
    # print(field_name)
    
    if len(field_name['choice_value']) > 0:
        for k,v in field_name.items():
            
            print(k, ': ', v)