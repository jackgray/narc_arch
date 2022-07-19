from redcap import Project
from configs.redcap import config

############  PyCap Setup ####################
def redcapConnect(project):  
    more_proj = Project(config['api_url'], config['more_token'])
    sexdiff_proj = Project(config['api_url'], config['sexdiff_token'])
    mssm_proj = Project(config['api_url'], config['mssm_token'])
    baseline_proj = Project(config['api_url'], config['baseline_token'])
    
    if project == 'more':
        return more_proj
    elif project == 'sexdiff':
        return sexdiff_proj
    elif project == 'mssm':
        return mssm_proj
    elif project == 'baseline':
        return baseline_proj
    else:
        return print("Project not found. Try 'sexdiff, sex diff, sex differences, more, or baseline")