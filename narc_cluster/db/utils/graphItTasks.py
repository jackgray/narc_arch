
from utils.dbConnect import getVertexCollection, getEdgeCollection, addEdge, getGraph
from configs import arango

def graphItTasks(taskname, filename):
    arangodb, graph = getGraph('NARC_DEV', arango.config['graph_name'])
    task_vertices = getVertexCollection(graph, 'Task_Data')
    
    mri_task_vertices = getVertexCollection(graph, 'MRI_Data')
    taskMRIs_edge = getEdgeCollection(graph, 'taskMRIs_edge', arango.config['collection_name'],'MRI_Data')    
    
    print("Collected edges and vertices.")
    task_key = taskname
    
    task_id = "/".join(['Task_Data', taskname])
    mri_key = filename.replace('.', '').replace('-', '').replace('_', '').lower()
    mri_id = "/".join(['MRI_Data', mri_key] )
    
    print('vertex ids: \n', task_id, mri_id)
    
    print("\n\nAttempting to insert task / mri data:") 
    
    # Inserts data if empty, and errors before overwriting
        
    print("Attempting to insert Task data vertex for ", task_key)
    try:
        graph.insert_vertex('Task_Data', {"_key": task_key})
    except: 
        print("\nCould not insert into collection MRI_Data. It may already exist.\n")


    print("Attempting to update Task_Data vertex")
    try:
        extant_task_data = task_vertices.get({"_id": task_id})
        print("Retrieved extant task data:")
        print(extant_task_data)
        update_task_data = [mri_key]
        try:
            for i in extant_task_data['hasMRIs']:
                if len(i) > 0:
                    print('hasMRIs:')
                    print(i)
                    update_task_data.append(i)
            print("Successfully appended mri reference. Trying to update db.")
            print(update_task_data)
            try:
                graph.update_vertex({"_id": task_id, "hasMRIs": update_task_data})
                print("Successfully updated Task data vertex")
            except: 
                print("Could not update subject vertex.")
        except: 
            print("Error in appending json for ", extant_task_data)
    except:
            print("Could not retrieve extant subject data")
    
    # append_data = list(dict.fromkeys(append_data)) # remove duplicates WARNING: may not apply to all cases    
    edge_id = "taskMRIs_edge" + "/" + task_key + '-' + mri_id
    print("Trying to link subject and mri data vertices with hasMRIs edge")

    try:
        addEdge('taskMRIs_edge', task_key, mri_id)
        print("Successfully linked ", task_id, " with ", mri_id, " via taskMRIs_edge")
        print("Attempting to add data to edge")
        try:
            graph.update_edge({"_id": edge_id, 'hasMRIs': mri_key})
        except:
            print("Could not add data to edge")

    except:
        print("Couldn't link vertices")