
from utils.dbConnect import getVertexCollection, getEdgeCollection, addEdge, getGraph
from configs import arango

def graphItMRI(taskname, session, seriesname, scan_type, narc_id, filename, modality, runname, parent_path, missed, collected):
    arangodb, graph = getGraph(arango.config['db_name'], arango.config['graph_name'])
    subject_vertices = getVertexCollection(graph, arango.config['collection_name'])
    
    mri_task_vertices = getVertexCollection(graph, 'MRI_Data')
    subjectMRIs_edge = getEdgeCollection(graph, 'subjectMRIs_edge', arango.config['collection_name'],'MRI_Data')    
    
    print("Collected edges and vertices.")
    subjects_id = "/".join([arango.config['collection_name'], narc_id])
    mri_key = filename.replace('.', '').replace('-', '').replace('_', '').lower()
    mri_id = "/".join(['MRI_Data', mri_key] )
    
    print('vertex ids: \n', mri_id, subjects_id)
    
    print("\n\nAttempting to insert task mri data:") 
    
    # Inserts data if empty, and errors before overwriting
    
    filetype = filename.split('.')[-1]
    
    print("Attempting to insert MRI data vertex for ", mri_key)
    try:
        graph.insert_vertex('MRI_Data', {"_key": mri_key})
    except: 
        print("\nCould not insert into collection MRI_Data. It may already exist.\n")

    print("Attempting to update MRI_Data vertex")
    try:
        graph.update_vertex({"_id": mri_id, "task": taskname, "modality": modality, "run": runname, "session": session, "type": scan_type, "filetype": filetype, "series": seriesname, "path": parent_path, "filename": filename, 'narc_id': narc_id})
        print("Updated MRI data vertex")
    except:
        print("Could not update MRI data vertex")
    
    
 ###### SUBJECT MODIFICATION   
 
    print("Attempting to insert MRI reference to subject")
    try:
        graph.insert_vertex({"_id": subjects_id, "hasMRIs": [mri_key]})  
        print("\nSuccessfully inserted vertex")
    except: 
        print("Could not insert MRI reference to subject vertex collection. Trying to update...")
        
        # SUBJECT UPDATE
        try:
            extant_subject_data = subject_vertices.get({"_id": subjects_id})
            print("Retrieved extant subject data:")
            print(subject_vertices)
            print("Attempting to update mri reference")
            update_data = [mri_key]
            try:
                for i in extant_subject_data['hasMRIs']:
                    if len(i) > 0:
                        print('hasMRIs:')
                        print(i)
                        update_data.append(i)
                print("Successfully appended mri reference. Trying to update db.")
                print(update_data)
                try:
                    graph.update_vertex({"_id": subjects_id, "hasMRIs": update_data})
                except: 
                    print("Could not update subject vertex.")
            except: 
                print("Error in appending json for ", subjects_id)
        except: 
            print("Could not retrieve extant subject data ", subjects_id)
        
    #
        # print("Updating MRI Tasks with ")
        # except: 
        #     print("Could not insert into collection MRI_Data. It may already exist.")
        
        
            # Download and append the new data, then update (overwrites)
        # print("Retreiving existing data")    
        # extant_mri_data = mri_task_vertices.get({"_id": mri_id})
        # # update_data = insert_data[session][seriesname][short_filename][narc_id][fullpath].append(fullpath)
        # print("\nEXTANT DATA")
        # print(extant_mri_data)

    # graph.update_vertex({"_id": mri_id}, new_data)

    
    # append_data = list(dict.fromkeys(append_data)) # remove duplicates WARNING: may not apply to all cases    
    edge_id = "subjectMRIs_edge" + "/" + mri_key + '-' + narc_id
    print("Trying to link subject and mri data vertices with hasMRIs edge")

    try:
        addEdge(subjectMRIs_edge, mri_id, subjects_id)
        print("Successfully linked ", subjects_id, " with ", mri_id, " via subjectMRIs_edge")
        print("Attempting to add data to edge")
        try:
            graph.update_edge({"_id": edge_id, 'MRIs': mri_key, 'subject': narc_id})
        except:
            print("Could not add data to edge")

    except:
        print("Could not link vertices")
