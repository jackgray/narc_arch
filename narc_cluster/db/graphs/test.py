from narc_cluster.db.dbConnect import getGraph, getEdgeDef, getVertexCollection, getEdgeCollection

db, graph = getGraph('MORE', 'more_graph')

drugs_vertices = getVertexCollection(graph, 'drugs')

ud_group_edges = getEdgeCollection(graph, 'UD_group_edge', 'subjects', 'drugs')

def addEdge(edge_collection, from_vertex, to_vertex):
    edge_key = from_vertex.split('/')[1] + '-' + to_vertex.split('/')[1]
    edge_collection.insert({
        '_key': edge_key,
        '_from': from_vertex,
        '_to': to_vertex
    })