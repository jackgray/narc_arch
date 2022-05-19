import json
import pandas as pd

from db.excel_conv.config import files, sheets
from db.utils.dbConnect import getCollection
from db.utils.dbUpdate import updateArango

def forPrediction():
    db, collection = getCollection('MORE', 'subjects3')

    # forPrediction = excel2json.convert_from_file('forPrediction.xlsx', engine='openpyxl')
    for file_k, file_v in files.items():
        for sheet_k, sheet_v in sheets.items():
            print('\n\nSHEET: ', sheet_k)
            sheet_df = pd.read_excel(file_v, engine='openpyxl', sheet_name=sheet_v)
            sheet_json = sheet_df.to_json(orient='records')

            jsonobject = json.loads(sheet_json)
            jsonformatted = json.dumps(jsonobject, indent=4)
            # print(jsonformatted)

            # for k, v in jsonformatted:
            #     subj = k[0].replace('sub-S', '')
            #     print(k, v)
            for i in jsonobject:
                
                subj = i['subj']
                if 'S' in subj:
                    narc_id = subj.replace('S', '')
                if 'sub-S' in subj:
                    narc_id = subj.replace('sub-S', '')
                
                group = i['group']
                
                print(narc_id)
                
                task_name = sheet_v.split('_')[0]
                session = 'ses_' + str(i['session'])
                group = i['group']
                
                for k, v in i.items():
                    if v != 'None':
                        # print(j,k)
                    
                        update_data = {'tasks': { task_name: 
                                            { session: 
                                                { 'scores': 
                                                    { k: v }
                                                }
                                            }}
                                        }
                                                 
                        print(json.dumps(update_data, indent=2))
                # # print(json.dumps(update, indent=4))
                
                        updateArango(collection, narc_id, update_data)
            