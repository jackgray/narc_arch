from collections import Counter
from pandas import pandas as pd
import re
import json

from db.calculated_fields.wasi import wasiCalc
from db.utils.dbConnect import getCollection
from db.utils.dbUpdate import updateArango


from db.configs.arango import config

'''
This query shows how to retrieve specific data based on other data. 
It first retrieves all ema response data available for each subject
in json format, separated by treatment day ("day_n"). The structure
is subject.tasks.ema.<task_day as int>.<question number as int>

## How to abstract when a parent value is unknown or not cared about:

Currently, there is not support for * substitutionse
(i.e.: subject.tasks.ema.[*][3] for responses to question 3 
accross all treatment days), so the query string must be explicit 
(i.e.: subject.tasks.ema.day_8[3]), so to abstract, we must 
pull all days and iterate through the json and use logical operators 
for filtering. (i.e.: for key,value in subjects['query attribute label'].items(): for value2, key2 in value.items(): for value2, key3 in..etc.)
This pattern crawls through the tree directory structure. The the specific path is called a branch, and a collection of branches is a tree.

The query response is an iterable cursor object that must be looped through to pull json 
objects for each subject. There are many ways of interacting with the json response.
Two common ways are to (1) read the json object into a pandas dataframe, which 
can be appended into a dataframe of dataframes, or (2) iterating through the json tree 
structure with simple for loops, as expressed below.

In JSON, each level is a {key: value} pair. The value in these key:value pairs is 
itself a key:value pair, except for the final value at the end of the branch, which 
can be a string, int, tuple, or list, but is not k:v. Below is an example of 
an n-depth tree structure where n=4. The first level value where n=1 includes all data 
in the tree under it. As a branch is traversed, its value returned is a smaller and smaller json
object until the bottom is reached.

example_JSON = [{
    key1_aka_category_1: {
        value1_aka_key2_aka_sub_category_1: {
            value2_aka_key3_aka_sub_sub_category_1: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                }
            }
        },
        value1_aka_key2_aka_sub_category_2: {
            value2_aka_key3_aka_sub_sub_category_1: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                }
            },
            value2_aka_key3_aka_sub_sub_category_2: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                }
            },
            value2_aka_key3_aka_sub_sub_category_3: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                },
                value3_aka_key4_aka_final_key_2: { value4_aka_final_value_aka_no_value_to_this }
                },
                value3_aka_key4_aka_final_key_3: { [value4_aka_final_value_aka_no_value_to_this_1, value4_aka_final_value_aka_no_value_to_this_2 }
                },
                value3_aka_key4_aka_final_key_4: { value4_aka_final_value_aka_no_value_to_this }
                }
            }
        },
        key1_aka_category_2: {
        value1_aka_key2_aka_sub_category_1: {
            value2_aka_key3_aka_sub_sub_category_1: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                }
            }
        },
        value1_aka_key2_aka_sub_category_2: {
            value2_aka_key3_aka_sub_sub_category_1: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                }
            },
            value2_aka_key3_aka_sub_sub_category_2: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                }
            },
            value2_aka_key3_aka_sub_sub_category_3: {
                value3_aka_key4_aka_final_key_1: { value4_aka_final_value_aka_no_value_to_this }
                },
                value3_aka_key4_aka_final_key_2: { value4_aka_final_value_aka_no_value_to_this }
                },
                value3_aka_key4_aka_final_key_3: {[ value4_aka_final_value_aka_no_value_to_this_1, value4_aka_final_value_aka_no_value_to_this_2 ]} <--- final value as array
                },
                value3_aka_key4_aka_final_key_4: { value4_aka_final_value_aka_no_value_to_this }
                }
            }
        }
    }]

Each level is iterable by k:v pairs via the .items() attribute. An item() is a k:v pair, 
where v can also have a k:v pair indexable again by the .items() attribute.
(i.e.: 
     >> for category, sub_categories in example_JSON.items():   # 1st level k:v = category:sub_categories
            for sub_category, sub_sub_categories in sub_categories.items():     # 2nd level k:v = sub_category:sub_sub_categories
                for final_key, final_value  in final_key.items():       # 3rd level k:v = sub_sub_category:final_value
                    print(final_value)  # final value is not iterable because it is not a k:v pair, it is just v
            
)

Any element of a tree data structure can be explicitly accessed as well.
if example_JSON['key1']['key2']['key3'] == 'final_value comparison':
    do stuff

'''

def emaQuery():
    # Connect to the database (function at db/utils/dbConnect.py, config vars at db/configs/arango.py)
    db, collection = getCollection(config['db_name'], config['collection_name'])

    # arango api function to call on the db server
    query_result = db.aql.execute(
        'FOR s IN subjects \
            FILTER s.tasks.ema != null \
            RETURN { narc_id: s._key, ema: s.tasks.ema, asi_drug: s.tasks.asi.drug }',
        batch_size=1
    )
    '''
    Access the data returned above by iterating through the response object and
    calling i['query_defined_label'] aka i['narc_id'] or i['ema'] gives that data for 
    subject i
    '''
    
    subj_dfs = []    # You can store dataframes for each subject as into an array as they are collected
    # query_result is an arango Cursor object that must be iterated through to be extracted. each iteration returns python dict
    for subject in query_result:
        ema_days = subject['ema']
        
        # Use json.dumps() to ensure proper json format
        all_subjs_ema_days_df = pd.read_json(json.dumps(ema_days), orient='record')
        
        try: subj_dfs.append(all_subjs_ema_days_df)
        except: pass
        # print(json.dumps(ema_days, indent=2))
        for day, questions in ema_days.items():
            
            # bandaid for bug in db
            if 'day_' in day:
                day_int = int(day.split('day_')[-1])
                try: 
                    # Use try statement to catch error when a subject doesn't have a response for that question
                    if questions['3'] > 7 and day_int > 15:
                        
                        '''
                        Get ao of all drugs if subject responds with temptation to do drugs above x on a treatment day past y.
                        Condition that the response to question '3' must be above 7 and the day must be past 15
                        
                        '''
                        for druglabel, drug in subject['asi_drug'].items():
                            # handle error when subj doesn't provide ao for indexed drug
                            try: print(druglabel, drug['ao'])
                            except: pass
                        
                except: pass
                
                for question, resp in questions.items():
                    # 3. "How badly do you want to use drugs? 0-10"
                    if question == '3' and day_int > 15 and int(resp) > 7:
               
                        # Query more data by adding condition to the AQL RETURN statement,
                        # or by sending a second query only when warranted (below)
                        for drug, drug_responses in subject['asi_drug'].items():
                            try: print(drug, drug_responses['ao']) 
                            except: pass
                            
                        # Alternate way to retrieve data (more granular)
                        new_data = collection.find({'_key': subject['narc_id']})    # Makes simple query of all data for a subject
                        for focus_subject in new_data:
                            asi = focus_subject['assessments']['asi']
                            for drug, drug_qs in asi['drug'].items():
                                # Use try statement to handle errors where no data exists
                                try: print(drug, drug_qs['ao'])
                                except: pass
                        # print(json.dumps(new_data, indent=2))     
    return subj_dfs
    
            
    