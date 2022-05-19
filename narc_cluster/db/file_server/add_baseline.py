import json
import pickle
import pprint
from copy import deepcopy
# from turtle import update
from narc_cluster.db.file_server.connect import sshConnect
from narc_cluster.db.utils.dbConnect import getCollection
from narc_cluster.db.utils.dbUpdate import updateArango

# from ssh_utilities import Connection, SSHPath

def addBaselineProject():
    
    db, collection = getCollection('MORE', 'subjects3')
    
    pp = pprint.PrettyPrinter(depth=8, indent=1, compact=False)
    ssh = sshConnect()

    (stdin, stdout, stderr) = ssh.exec_command('find /volume1/narclab/baseline -maxdepth 100 -type f') 
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
        if path.split('/')[6].startswith('sub'):
            try:
                filename = path.split('/')[-1]
                sesname = filename.split('_')[1]
                modality = path.split('/')[8]
                narc_id = filename.split('_')[0].split('sub-S')[-1]
                taskname = filename.split('_')[2]
                if 'task' in taskname:
                    seriesname = filename.split('_')[3].split('-')[1]
                    taskname = taskname.split('-')[-1]
                else:
                    seriesname = taskname.split('-')[-1]
                # print(narc_id)
                # print(narc_id)]
                path = ['/' + '/'.join(path.split('/')[7:])]
                # print(path)
                print('sesname: ', sesname)
                print('series :', seriesname)
                print('modality :', modality)
                print('taskname: ', taskname)
            
                update_data = pathList2json(paths)
                # print(update_data['volume1'])
                
                # if narc_id == prev_subj:
                    # update_data = dict(list(prev_data.items() + list(update_data.items())))
                    # update_data = combine_dicts(deepcopy(prev_data), deepcopy(update_data))
                    # print(update_data)
                    # print(prev_data)
                update_data = { 'mri_data': { 'sessions': { sesname: { 'modality': { modality: { 'series': { seriesname: update_data['volume1']['narclab']['bids']['more']['nifti']['sub-S' + narc_id][sesname][modality] }}}}}}}
                print(update_data)
                # update_data['mri_data'][sesname][modality] += prev_data['mri_data'][sesname][modality]
                    #     print(i)
                    # try:
                    #     update_data = combine_dicts(update_data, prev_data)
                    # print(update_data)
                    # except:
                    #     pass
                # updateArango(collection, narc_id, update_data)

                prev_data = update_data
                prev_subj = narc_id
            except:
                print("index out of range")

            # print("PREV: ", prev_data)
          
        # print(json.dumps(jayson, indent=1, sort_keys=True))
    
    # jstring = json.loads(jayson)
    # for k, v in jayson.items():
    #     # print('\n\n1ST------------------------------------')
    #     # print(k, v)
    #     for second, sv in jayson[k].items():
    #         print('\n2ND-----------------------------------')
    #         # print(k,v)
    #         print()
    #         print(second, sv)

    
    
    # pp.pprint(jayson)            
    # jayson = {}
    # for f in all_filepaths:
    #     print('\n', f)
    #     path_parts = f.split('/')[3:]
    #     path_parts.reverse()
    #     for path_part in path_parts:
    #         print(path_part)
    #         if len(path_part) == 0:
    #             jayson[path_part] = 0
    #         else:
    #             outer = {}
    #             outer[path_part] = jayson
    #             jayson = outer;
    #     # print(jayson)
        
            
        
    # update_data = { 'file_references'}
    
    # # jayson = json.dumps(all_filepaths, indent = 4)
    # # print(jayson)
    

