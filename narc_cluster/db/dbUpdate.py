def updateArango(collection, record_id, update_data):
    collection.update_match(
        {'record_id': record_id},
        update_data
    )
    