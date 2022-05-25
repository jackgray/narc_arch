import json
import pickle
import sys
import pprint
from copy import deepcopy
# from turtle import update
from file_server.connect import sshConnect
from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
from configs import arango

# from ssh_utilities import Connection, SSHPath

def addMoreFiles():
        
    db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    db, mri_collection = getCollection(arango.config['db_name'], 'MRI_DATA')
    
    pp = pprint.PrettyPrinter(depth=8, indent=1, compact=False)
    ssh = sshConnect()

    (stdin, stdout, stderr) = ssh.exec_command('find /volume1/narclab/bids/more/nifti -maxdepth 100 -type f') 
# # stdin.write(fileServer.config['password'])

    jsonpath = '/home/jackgray/Code/narc_arch/narc_cluster/db/file_server/all_filepaths.json'

    def pathList2json(paths):
        paths = sorted(paths, key = lambda s: len(s.lstrip('/').split('/')), reverse = True)
        
        tree_path = {}
        for path in paths:
            levels = path.lstrip('/').split('/')
            filename = levels.pop()
            acc = tree_path 
            for i, p in enumerate(levels, start = 1):
                if i == len(levels):
                    acc[p] = acc[p] if p in acc else []
                    if isinstance(acc[p], list):
                        acc[p].append(filename)
                else:
                    acc.setdefault(p, {})
                acc = acc[p]
        return tree_path
    
    def combine_dicts(a, b):
        for k,v in b.items():
            # for k2, v2 in v:
                # print(k2, v2)
            if k in b:
                # print(k, b)
                list(a[k]).extend(v)
            else:
                a[k] = v
        # print(a)
    
    paths = str(stdout.read().decode('utf8')).split()
    # pathsjson = pathList2json(paths).itemgetter(2)
    # print(pathsjson)
    prev_subj = None;
    for path in paths:
        fullpath = path
        if path.split('/')[6].startswith('sub'):
            try:
                filename = path.split('/')[-1]
                session = "ses_" + str(filename.split('_')[1].split('-')[1])
                modality = path.split('/')[8]
                narc_id = filename.split('_')[0].split('sub-S')[-1]
                taskname = filename.split('_')[2]
                runname = filename.split('_')[-2]

                if 'task' in taskname:
                    seriesname = filename.split('_')[3].split('-')[1]
                    taskname = taskname.split('-')[-1]
                    filetype = filename.split('.')[-1]
                    if taskname == 'stopsignal':
                        taskname = 'sst'  
                    if not 'run' in runname:
                        runname = 'run_1' 
            
                    # path = ['/' + '/'.join(path.split('/')[7:])]
                    
                    # print('path: ', path)
                    print('sesname: ', session)
                    print('series :', seriesname)
                    print('modality :', modality)
                    print('taskname: ', taskname)
                    print('filetype: ', filetype)
                
                    update_data = pathList2json(paths)
                    
                    if filetype == 'gz':
                        update_data = { 'tasks': { taskname: { 
                                        'raw_data': {
                                            session: { 
                                                'nifti': {
                                                    seriesname + "_" + "_".join(filename.split('_')[-1:]): fullpath 
                                                    } 
                                            }
                                            }
                                        }}}
                    elif filetype == 'json':
                        update_data = { 'tasks': { taskname: { 
                                        'raw_data': {
                                            session: { 
                                                'json': {
                                                    seriesname + "_" + "_".join(filename.split('_')[-1:]): fullpath 
                                                    } 
                                            }
                                            }
                                        }}}
                    elif filetype == 'tsv':
                        update_data = { 'tasks': { taskname: { 
                                        'raw_data': {
                                            session: { 
                                                'tables': {
                                                    seriesname + "_" + "_".join(filename.split('_')[-1:]): fullpath 
                                                    } 
                                            }
                                            }
                                        }}}
                                                
                    # print(json.dumps(update_data, indent=2, sort_keys=True))
                    mri_data = update_data['tasks']
                    # update_data['tasks']['raw_data'][session]['subjects'].append()
                    print(mri_data)
                    updateArango(collection, narc_id, update_data)
                    print('Updated subjects collection')
                    try: 
                        mri_collection.insert({'_key': taskname})
                        print("Inserted ", taskname, " into MRI_DATA")
                    except: 
                        print("Error inserting new data to MRI_DATA. Document probably exists already.")
                        pass
                    try: 
                        mri_collection.update_match({'_key': taskname}, mri_data)
                        print("Updated MRI_DATA collection")
                    except: print("Couldn't update MRI_DATA collection")  
            except  :
                print(sys.exc_info()[0])

      
        
     