from pymongo import MongoClient
from db.configs import mongo

def mongoTest():
    db = MongoClient(mongo.config['endpoint']).more


    db.collection.createIndex(
        { "$**" : 1 },
        { "wildcardProjection": { 
            "task.ses_1": 1,
             "task.ses_2" : 1,
             "assessment.asi.drug.heroin": 1
             }
        }
    ) 
    
    # db.subjects.find_many({})
    data = db.subjects.find({'task': {'$**': 'asi'}}, {})

    print(data)
    db.collection.createIndex( { "$**": "text" } )