import json
import pandas as pd

from db.excel_conv.config import files, sheets
from db.utils.dbConnect import dbConnect
from db.utils.dbUpdate import updateArango

def csv2db(filename):
    db, collection = dbConnect()

    # forPrediction = excel2json.convert_from_file('forPrediction.xlsx', engine='openpyxl')
    csv = pd.ExcelFile(filename)
    sheets = pd.ExcelFile(filename).sheet_names
    for sheet in sheets:
        print('\n\nSHEET: ', sheet)
        sheet_df = pd.read_excel(filename, engine='openpyxl', sheet_name=sheet)
        sheet_json = sheet_df.to_json(orient='records')
        jsonobject = json.loads(sheet_json)
        # print(jsonobject)
        jsonformatted = json.dumps(jsonobject, indent=4)
        # print(jsonformatted)

        # for k, v in jsonformatted:
        #     subj = k[0].replace('sub-S', '')
        #     print(k, v)
        for i in jsonobject:
            print('\n', i['narc_id'])
                # print("OBJ:", i)
            # try:
            #     subj = i['Subject ID'] or i['NARC ID']
            # except:
            #     print("ERROR")
            # if 'S' in str(subj):
            #     narc_id = subj.replace('S', '')
            # if 'sub-S' in str(subj):
            #     narc_id = subj.replace('sub-S', '')
            # else:
            #     narc_id = subj
            # print(narc_id)
            
            # task_name = sheet.split('_')[0]
            # # session = 't' + str(i['session'])
            
            for j, k in i.items():
                
                if str(k) != 'None' and k != 0.0:
                    x = str(j).split('_')
                    y = str(k).split('_') 

                    
                    print(x,y)
                
                    # update_data = {
                    #     'analysis': {
                    #         'outputs': {
                    #             task_name: { 
                    #                 'session': {session: {j:k }
                    #                             }
                    #                 }
                    #             }
                    #         }
                    #     }
                    # print(update_data)
            # # print(json.dumps(update, indent=4))
            
                    # updateArango(collection, narc_id, update_data)
        