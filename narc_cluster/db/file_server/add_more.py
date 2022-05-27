
import sys
import pprint

from file_server.connect import sshConnect
from utils.graphItMRI import graphItMRI
from utils.graphItTasks import graphItTasks

# from ssh_utilities import Connection, SSHPath
'''
REMINDER: make sure you are working in the right db/collection(s). Check config file
'''
def addMoreFiles():
        
    pp = pprint.PrettyPrinter(depth=8, indent=1, compact=False)
    ssh = sshConnect()

    (stdin, stdout, stderr) = ssh.exec_command('find /volume1/narclab/bids/more/nifti -maxdepth 100 -type f') 
# # stdin.write(fileServer.config['password'])

    jsonpath = '/home/jackgray/Code/narc_arch/narc_cluster/db/file_server/all_filepaths.json'
    missed=[]
    collected=[]
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
                session = str(filename.split('_')[1].split('-')[1])
                modality = path.split('/')[8]
                narc_id = filename.split('_')[0].split('sub-S')[-1]
                taskname = filename.split('_')[2]
                runname = filename.split('_')[-2].split('-')[-1]
                parent_path = "/".join(fullpath.split('/')[0:-1])

                if 'task' in taskname:
                    seriesname = filename.split('_')[3].split('-')[1].split('series')[-1]
                    taskname = taskname.split('-')[-1]
                    filetype = filename.split('.')[-1]
                    if taskname == 'stopsignal':
                        taskname = 'sst'  
                    if not 'run' in runname:
                        runname = '1' 
            
                    # path = ['/' + '/'.join(path.split('/')[7:])]
                    
                    print('path: ', parent_path)
                    print('sesname: ', session)
                    print('series :', seriesname)
                    print('modality :', modality)
                    print('taskname: ', taskname)
                    print('filetype: ', filetype)
                
                    update_data = pathList2json(paths)
                    

                    scan_type = "_".join(filename.split('_')[-1:]).split('.')[0]          
  
                    '''
                    GRAPH THE TASKS
                    '''                    
                    # try to insert, if it exists, try to append
                    # try:
                       
                    # except: 
                    #     print("err")
                    graphItTasks(taskname, filename)
                    # missed, collected = graphItMRI(taskname, session, seriesname, scan_type, narc_id, filename, modality, runname, parent_path, missed, collected)
                    # print('Updated subjects collection')
                    # print("MISSED: ", missed, "\nCOLLECTED: ", collected)
                    # try:
                    #     mri_task_vertices.insert(update_data)
                    # except: 
                    #     print("Error inserting data. Maybe it exists, so I'll try to update instead.")
                        
                    #     extant_data = mri_task_vertices.get({"_key": taskname})
                    #     try:
                    #         updated = extant_data[session][seriesname][short_filename]
                    #         for i in updated:
                    #             if len(i) > 0:
                                    
                                
                                                
                    # print(json.dumps(update_data, indent=2, sort_keys=True))
                    # mri_data = update_data['task
                    # update_data['tasks']['raw_data'][session]['subjects'].append()
                    # print(mri_data)
                    # updateArango(collection, narc_id, update_data)
                    # try: 
                    #     mri_collection.insert({'_key': taskname})
                    #     print("Inserted ", taskname, " into MRI_DATA")
                    # except: 
                    #     print("Error inserting new data to MRI_DATA. Document probably exists already.")
                    #     pass
                    # try: 
                    #     mri_collection.update_match({'_key': taskname}, mri_data)
                    #     print("Updated MRI_DATA collection")
                    # except: print("Couldn't update MRI_DATA collection")  
            except  :
                print(sys.exc_info()[0])

      
        
     