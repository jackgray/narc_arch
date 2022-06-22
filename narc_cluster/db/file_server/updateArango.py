from db.utils.dbConnect import getCollection
from db.file_server.add_more import crawlDirs

def update():
    db, collection = getCollection('MORE', 'MRI_DATA')
    filepathsJSON = crawlDirs()
    collection.insert(filepathsJSON)