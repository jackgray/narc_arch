from asyncio import tasks
from collections import Counter
from pandas import pandas as pd
import re
import json

from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango


from configs.arango import config


def respAccrossSessions(task_or_survey):
    # Connect to the database (function at db/utils/dbConnect.py, config vars at db/configs/arango.py)
    db, collection = getCollection(config['db_name'], config['collection_name'])
    
    # tasks_and_surveys = db.aql.execute(
    #     'FOR s IN subjects \
    #         FILTER s.tasks. != null \
    #         RETURN { narc_id: s._key, ema: s.tasks.ema, asi_drug: s.tasks.asi.drug }',
    #     batch_size=1
    # )    # Makes simple query of all data for a subject
    # for task_or_survey in tasks_and_surveys:
    #     print(task_or_survey)
    #     if task_or_survey['task_or_survey'] != 'null':
    #         var_task_or_survey = 'tasks'
    #     else:
    #         var_task_or_survey = 'surveys'
    #     print(task_or_survey['task_or_survey'])
        
    # Creat docstring for query function arg
    var_task_or_surveys = ['tasks', 'surveys']
    task_or_survey_sessions = []
    for var_task_or_survey in var_task_or_surveys:
        query_resp = db.aql.execute(str('FOR s in ' + config['collection_name'] + '\
            FILTER s.' + var_task_or_survey + '.' + task_or_survey + '!= null \
            RETURN { ' + task_or_survey + ': s.' + var_task_or_survey + '.' + task_or_survey + ' }'),
            batch_size=1
        )
        
        for task_survey in query_resp:
            try:
                task_or_survey_sessions.append(task_survey[task_or_survey]['sessions'])
                print('\n\n')
                # print(task_or_survey_sessions)
            except: pass
            
    return task_or_survey_sessions

    # # arango api function to call on the db server
    # query_result = db.aql.execute(
    #     'FOR s IN subjects \
    #         FILTER s.tasks.ema != null \
    #         
    # '''
    # Access the data returned above by iterating through the response object and
    # calling i['query_defined_label'] aka i['narc_id'] or i['ema'] gives that data for 
    # subject i
    # '''
    
    # subj_dfs = []    # You can store dataframes for each subject as into an array as they are collected
    # # query_result is an arango Cursor object that must be iterated through to be extracted. each iteration returns python dict
    # for subject in query_result:
    #     ema_days = subject['ema']
        
    #     # Use json.dumps() to ensure proper json format
    #     all_subjs_ema_days_df = pd.read_json(json.dumps(ema_days), orient='record')
        
    #     try: subj_dfs.append(all_subjs_ema_days_df)
    #     except: pass
    #     # print(json.dumps(ema_days, indent=2))
    #     for day, questions in ema_days.items():
            
    #         # bandaid for bug in db
    #         if 'day_' in day:
    #             day_int = int(day.split('day_')[-1])
    #             try: 
    #                 # Use try statement to catch error when a subject doesn't have a response for that question
    #                 if questions['3'] > 7 and day_int > 15:
                        
    #                     '''
    #                     Get ao of all drugs if subject responds with temptation to do drugs above x on a treatment day past y.
    #                     Condition that the response to question '3' must be above 7 and the day must be past 15
                        
    #                     '''
    #                     for druglabel, drug in subject['asi_drug'].items():
    #                         # handle error when subj doesn't provide ao for indexed drug
    #                         try: print(druglabel, drug['ao'])
    #                         except: pass
                        
    #             except: pass
                
    #             for question, resp in questions.items():
    #                 # 3. "How badly do you want to use drugs? 0-10"
    #                 if question == '3' and day_int > 15 and int(resp) > 7:
               
    #                     # Query more data by adding condition to the AQL RETURN statement,
    #                     # or by sending a second query only when warranted (below)
    #                     for drug, drug_responses in subject['asi_drug'].items():
    #                         try: print(drug, drug_responses['ao']) 
    #                         except: pass
                            
    #                     # Alternate way to retrieve data (more granular)
    #                     new_data = collection.find({'_key': subject['narc_id']})    # Makes simple query of all data for a subject
    #                     for focus_subject in new_data:
    #                         asi = focus_subject['assessments']['asi']
    #                         for drug, drug_qs in asi['drug'].items():
    #                             # Use try statement to handle errors where no data exists
    #                             try: print(drug, drug_qs['ao'])
    #                             except: pass
    #                     # print(json.dumps(new_data, indent=2))     
    # return subj_dfs
    
            
    