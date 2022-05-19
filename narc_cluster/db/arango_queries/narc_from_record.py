from narc_cluster.db.dbConnect import dbConnect
from narc_cluster.db.dbUpdate import updateArango

def narcFromRecord(record_id):
    db, collection = dbConnect()

    # cursor = db.aql.execute(
    #     'FOR subject IN subjects3 \
    #         RETURN { narc_id: subject._key, total: subject.battery.wasi.total, age: subject.age }',
    #     batch_size=1
    # )
    
    narc_id = collection.keys({'record_id': record_id})
    return narc_id
    
    