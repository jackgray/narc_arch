import json
import pandas as pd

from excel_conv.config import files, sheets
from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
from configs import arango

def forPrediction():
    db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])

    # forPrediction = excel2json.convert_from_file('forPrediction.xlsx', engine='openpyxl')
    for file_k, file_v in files.items():
        for sheet_k, sheet_v in sheets.items():
            print('\n\Scanning sheet: ', sheet_k)
            sheet_df = pd.read_excel(file_v, engine='openpyxl', sheet_name=sheet_v)
            sheet_json = sheet_df.to_json(orient='records')

            jsonobject = json.loads(sheet_json)
            jsonformatted = json.dumps(jsonobject, indent=4)
      
            for i in jsonobject: 
                subj = i['subj']
                session = 'ses_' + str(i['session'])
                if 'S' in subj:
                    narc_id = subj.replace('S', '')
                if 'sub-S' in subj:
                    narc_id = subj.replace('sub-S', '')                           
                task_name = sheet_v.split('_')[0]
                
                for k, v in i.items():
                    if len(str(v)) > 0 and v != 'None' and v != '0':
                        
                        update_data = {'tasks': { task_name: {
                                        'scores': { 
                                            session:  { k: v }
                                            }}
                                        }}
                        print(update_data)
                        updateArango(collection, narc_id, update_data)
            