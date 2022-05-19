def narcFromRecord(db, collection, record_id):
    res = collection.find({'record_id': record_id})
    narc_id = res.batch()[0]['_key']
    return narc_id
    
    