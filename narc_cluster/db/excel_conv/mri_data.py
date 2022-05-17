import json
import pandas as pd

from narc_cluster.db.excel_conv.config import files, sheets
from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.dbUpdate import updateArango

def mriData():
    db, collection = getCollection('MORE', 'subjects3')

    # forPrediction = excel2json.convert_from_file('forPrediction.xlsx', engine='openpyxl')
    for file_k, file_v in files.items():
        for sheet_k, sheet_v in sheets.items():
            print('\n\nSHEET: ', sheet_k)
            sheet_df = pd.read_excel(file_v, engine='openpyxl', sheet_name=sheet_v)
            sheet_json = sheet_df.to_json(orient='records')

            jsonobject = json.loads(sheet_json)
            # print(json.dumps(jsonobject, indent=2))
            for i in jsonobject:
                subj = i['narc_id']
                if 'S' in subj:
                    narc_id = subj.replace('S', '')
                if 'sub-S' in subj:
                    narc_id = subj.replace('sub-S', '')
                
                # group = i['group']
                
                print(narc_id)
                
                task_name = sheet_v.split('_')[0]
                # group = i['group']
                
                for k, v in i.items():
                    if str(v) != 'None':
                        k=k.replace(' ', '_').replace('-', '_').replace('?','_').replace('/', '_').replace('.','_').lower()
                        if 'str' in str(type(v)):
                            v=v.replace('-','_').replace('(','').replace(')','').lower()
                        # print(k,v)
                        
                        if 'explicit' in k or 'implicit' in k:
                            if 'explicit' in k:
                                version = 'explicit' 
                            else:
                                version = 'implicit'
                            taskname = 'choice'
                            
                            session = "ses_" + str(k.split('_')[1])
                            update_data = { 'tasks': { taskname: 
                                           { session:
                                               { 'scores': 
                                                   { version: 
                                                       { k.split('_')[-1]: v }
                                                    }
                                                }
                                            }
                                        }}
                        
                        if 'movie_' in k:
                            taskname = 'movie'
                            if '69' in k:
                                session = "ses_1"
                            if '35' in k:
                                session = "ses_2"
                                
                            k = "_".join(k.split('_')[-2:])
                            if 'mean' in k:
                                k = k.split('_')[-1]
                            
                                
                            update_data = { 'tasks': { taskname: 
                                { session: 
                                    { 'mri': 
                                        { 'LNAc': 
                                            { k: v }
                                            }
                                        }
                                    }
                                }}
                        # print(k)
                        if k.startswith('fa') or k.startswith('md') or k.startswith('rd'):
                            # print(k)
                            if not len(k.split('_')) > 3:

                                session = 'ses_' + k.split('_')[1].split('time')[1]
                                scalar = k.split('_')[0].upper()
                                subregion = k.split('_')[-1]
                                region = 'clusters'
                            
                                update_data = { 'diffusion': 
                                    { region: 
                                        { subregion: 
                                            { session:
                                                { scalar: v }
                                            }
                                        } 
                                    }  
                                }
                                
                                # print(json.dumps(update_data, indent=2))
                        elif '_hb' in k:
                            split = k.split('_')
                            scalar = split[3].upper()
                            region1 = split[1]
                            region2 = split[2]
                            subregion = split[0]
                            region = region1 + "_" + region2
                            update_data = { 'diffusion': 
                                { region: 
                                    { subregion: 
                                        { session: 
                                            { scalar: v }
                                        }
                                    }
                                }
                            }
                            
                        # elif k.startswith('mri'):
                        #     print(k)
                        #     split = k.split('_')
                        #     session = 'ses_' + split[1]
                        #     if 

                        # try:
                        #     print(json.dumps(update_data, indent=2))
                        #     updateArango(collection, narc_id, update_data)
                        # except:
                        #     print("No data to update yet")
                        #     continue