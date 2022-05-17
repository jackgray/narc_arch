from narc_cluster.db.dbConnect import getGraph, getEdgeDef, getVertexCollection, getEdgeCollection

def test():
    db, graph = getGraph('MORE', 'more_graph')

    drugs_vertices = getVertexCollection(graph, 'drugs')
    enrollmentGroup_vertices = getVertexCollection(graph, 'enrollment_group')
    

    ud_group_edges = getEdgeCollection(graph, 'UD_group_edge', 'subjects', 'drugs')

