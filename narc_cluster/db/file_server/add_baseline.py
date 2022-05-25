import json
import pickle
import pprint
import sys
from copy import deepcopy
# from turtle import update
from file_server.connect import sshConnect
from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
from configs import arango, redcap

# from ssh_utilities import Connection, SSHPath

def addBaselineFiles():
        
    db, collection = getCollection(arango.config['db_name'], arango.config['collection_name'])
    db, mri_collection = getCollection(arango.config['db_name'], 'MRI_DATA')
    
    pp = pprint.PrettyPrinter(depth=8, indent=1, compact=False)
    ssh = sshConnect()

    (stdin, stdout, stderr) = ssh.exec_command('find /volume1/narclab/bids/baseline/restinganatomy/nifti -maxdepth 100 -type f') 
# # stdin.write(fileServer.config['password'])

    jsonpath = '/home/jackgray/Code/narc_arch/narc_cluster/db/file_server/all_filepaths.json'
    
    paths = str(stdout.read().decode('utf8')).split()
    # print(paths)
    # pathsjson = pathList2json(paths).itemgetter(2)
    # print(pathsjson)
    prev_subj = None;
    for path in paths:
        # print(path)
        fullpath = path
        if path.split('/')[-1].startswith('sub') and not "@" in path:
            try:
                filename = path.split('/')[-1]
                session = "ses_" + str(filename.split('_')[1].split('-')[1])
                modality = path.split('/')[-2]
                narc_id = filename.split('_')[0].split('sub-S')[-1]
                taskname = filename.split('_')[2]
                runname = filename.split('_')[-2]

                if 'task' in taskname:
                    if 'series' in taskname:
                        seriesname = filename.split('_')[3].split('-')[1]
                    else:
                        seriesname = None
                    taskname = taskname.split('-')[-1]
                    filetype = filename.split('.')[-1]
                    if taskname == 'stopsignal':
                        taskname = 'sst'  
                    if not 'run' in runname:
                        runname = 'run_1' 
            
                    # path = ['/' + '/'.join(path.split('/')[7:])]
                    
                    # print('path: ', path)
                    # print('sesname: ', session)
                    # print('series :', seriesname)
                    # print('modality :', modality)
                    # print('taskname: ', taskname)
                    # print('filetype: ', filetype)
                
                    # update_data = pathList2json(paths)
                    
                    if filetype == 'gz':
                        ftype = 'nifti'
                    elif filetype == 'tsv':
                        ftype = 'tables'
                    elif filetype == 'json':
                        ftype = 'json'
                    else:
                        print("Unmatched path: ", fullpath)
                        continue
                    
                    if seriesname != None:
                        k = "_".join(seriesname, filename.split('_')[-1:])
                        print(k)
                    
                    else: 
                        k = "_".join(filename.split('_')[-1:])
                    update_data = { 'tasks': { taskname: { 
                                    'raw_data': {
                                        ftype: { 
                                            session: {
                                                k: fullpath 
                                                } 
                                            }
                                        }
                                    }}}
                                                               
                    # print(json.dumps(update_data, indent=2, sort_keys=True))
                    
                    # updateArango(collection, narc_id, update_data)
                    
                    # After adding to subjects, add scans by taskname to separate collection
                    mri_data = update_data['tasks']
                    mri_data.update({'_key': taskname})
                    print(mri_data)
                    print('Updated subjects collection')
                    try: 
                        mri_collection.insert(mri_data)
                        print("Inserted ", taskname, " into ", mri_collection)
                    except: 
                        print("Error inserting new data to ", mri_collection, ". Document probably exists already.")
                        pass
                    try: 
                        mri_collection.update_match({'_key': taskname}, mri_data)
                        print("Updated collection ", mri_collection)
                    except: print("Couldn't update collection ", mri_collection)  
            except  :
                pass
                print("ERROR: ", sys.exc_info()[0])
                print(fullpath)
                