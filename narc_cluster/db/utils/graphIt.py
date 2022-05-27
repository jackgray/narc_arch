
from utils.dbConnect import getVertexCollection, getEdgeCollection, addEdge


def graphIt(graph, subjectsCollectionName, narc_id, toCollectionName, to_key, edgeCollection, add_field1, key, add_field2, value, missed, collected):
    subjColl = getVertexCollection(graph, subjectsCollectionName)
    print(edgeCollection)
    toColl = getVertexCollection(graph, toCollectionName)
    edgeColl = getEdgeCollection(graph, edgeCollection, subjectsCollectionName, toCollectionName)
    from_id = "/".join([subjectsCollectionName, narc_id])
    to_id = "/".join([toCollectionName, to_key])
    
    try:
        toColl.insert({"_key": to_key})
    except: 
        print("Could not insert into collection ", toCollectionName, ". It may already exist.")
    
    print("Retreiving existing data")    
    extant_to_data = toColl.get({"_id": to_id})
    print(extant_to_data)
    
    
    append_data = [narc_id]
    try:
        for i in extant_to_data[add_field1][value]:
            print('test')
            if len(i) > 0:
                print('test2')
                print(i)
                append_data.append(i)
                collected.append(i)
    except: 
        print("No existing data found to append to.")
        missed.append(i)
    
    append_data = list(dict.fromkeys(append_data)) # remove duplicates WARNING: may not apply to all cases
    
    graph.update_vertex({"_id": to_id, add_field1: key, add_field2: { value: append_data }})
    
    try:
        addEdge(edgeColl, from_id, to_id)
        print("Successfully linked ", from_id, " with ", to_id, " via ", edgeCollection)
        collected.append(to_id)
    except:
        print("Couldn't link vertices ", from_id, " and ", to_id, " with ", edgeCollection, ". Edge might already exist")
        missed.append(to_id)
        pass