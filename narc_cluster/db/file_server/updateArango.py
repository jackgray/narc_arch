from narc_cluster.db.dbConnect import getCollection
from narc_cluster.db.file_server.crawl_dirs import crawlDirs

def update():
    db, collection = getCollection('MORE', 'MRI_DATA')
    filepathsJSON = crawlDirs()
    collection.insert(filepathsJSON)