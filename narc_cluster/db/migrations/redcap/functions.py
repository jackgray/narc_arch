def hasComplete(key):
    if 'complete' in key:
        k = 'complete' 
        assessment = key.split("_")[-2]
        return k, assessment 
    
def combine_dicts(a, b):
    for k,v in b.items():
        # for k2, v2 in v:
            # print(k2, v2)
        if k in b:
            # print(k, b)
            list(a[k]).extend(v)
        else:
            a[k] = v

def pathList2json(paths):
    paths = sorted(paths, key = lambda s: len(s.lstrip('/').split('/')), reverse = True)
    
    tree_path = {}
    for path in paths:
        levels = path.lstrip('/').split('/')
        filename = levels.pop()
        acc = tree_path 
        for i, p in enumerate(levels, start = 1):
            if i == len(levels):
                acc[p] = acc[p] if p in acc else []
                if isinstance(acc[p], list):
                    acc[p].append(filename)
            else:
                acc.setdefault(p, {})
            acc = acc[p]
    return tree_path