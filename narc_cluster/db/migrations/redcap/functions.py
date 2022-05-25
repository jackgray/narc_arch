def hasComplete(key):
    if 'complete' in key:
        k = 'complete' 
        assessment = key.split("_")[-2]
        return k, assessment 