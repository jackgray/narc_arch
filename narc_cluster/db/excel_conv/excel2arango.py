import json
import pandas as pd

from narc_cluster.db.excel_conv.config import files, sheets
from narc_cluster.db.dbConnect import dbConnect
from narc_cluster.db.dbUpdate import updateArango

def csv2db():
    db, collection = dbConnect()

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
                
                print(narc_id)
                
                task_name = sheet_v.split('_')[0]
                session = 't' + str(i['session'])
                
                for j, k in i.items():
                    if k != 'None':
                        # print(j,k)
                    
                        update_data = { 'task': {task_name: { 'session': {session: {j:k }}}}}
                        print(update_data)
                # # print(json.dumps(update, indent=4))
                
                        updateArango(collection, narc_id, update_data)
            