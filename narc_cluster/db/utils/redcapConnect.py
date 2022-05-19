from redcap import Project
from narc_cluster.db.configs import redcap

############  PyCap Setup ####################
def redcapConnect():  
    URL = redcap.config['api_url']
    TOKEN = redcap.config['api_token']
    proj = Project(URL, TOKEN)
    return proj