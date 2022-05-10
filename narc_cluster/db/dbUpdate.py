def updateArango(collection, narc_id, update_data):
    collection.update_match(
        {'_key': narc_id},
        update_data
    )
    