from arango import ArangoClient
from narc_cluster.db.configs.arango import config as arango

from narc_cluster.db.dbConnect import getCollection


db, collection = getCollection(arango.config['dbName'], arango.config['collection'])

db.analyzers()
db.create_analyzer(
    name='general_analyzer',
    analyzer_type='stem',
    properties={'locale': "en.utf-8"},
    features=[]
)

# Create ArangoSearch view 
db.create_arangosearch_view(
    name='all_fields',
)
# link = {
#     "inclueAllFields": True,
#     "fields": { "analyzers" : [ "text_en" ] }  
# }

# db.update_arangosearch_view(
#     name='all_fields',
#     properties={'links': { 'subjects': link}}
# )

db.aql.execute(
    'FOR s in subjects2 RETURN TOKENS(s, "general_analyzer")'
)
    