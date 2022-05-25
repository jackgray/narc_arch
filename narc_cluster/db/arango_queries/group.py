from utils.dbConnect import getCollection
from utils.dbUpdate import updateArango
from configs.arango import config

def groupQuery():
    db, collection = getCollection(config['db_name'], config['collection_name'])
    querystring = 'FOR s IN ' + config['collection_name'] + ' FILTER s.group != null \
        RETURN { narc_id: s._key, group: s.group }'
    resp_cursor = db.aql.execute(querystring, batch_size=1)
    
    return resp_cursor
   
    
    