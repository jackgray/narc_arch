from redcap import Project
from configs import redcap

############  PyCap Setup ####################
def redcapConnect():  
    URL = redcap.config['api_url']
    TOKEN = redcap.config['more_token']
    proj = Project(URL, TOKEN)
    return proj