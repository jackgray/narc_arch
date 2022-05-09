from arango import ArangoClient

from narc_cluster.db.configs.arango import config as arango

client = ArangoClient()
db = client.db(arango['db_name'], username=arango['sys_dbName'], password=arango['root_passwd'])

subjects = db.collection('subjects3')

subjects.keys()
    
def wratCalc(total, version, age, _key, output):   
    
    if version == 'blue':
        grade_eq = []
    if version == 'tan':
        grade_eq = []
        
    if age != 'null' and total in range(0, 57):
        ## AGE SCORE ##
        if age < 17:
            score = -999
        if age in range(17, 19):
            score = 'age1719'
        if age in range(20, 24):
            score = total.split()
        if age in range(25, 34):
            score = total.split()
        if age in range(35, 44):
            score = total.split()
        if age in range(45,54):
            score = total.split()
        if age in range(55, 64):
            score = total.split()
        ## GRADE EQUIVALENT ##
        if grade_eq == 'preschool' or 'k':
            wrat_ge = 0
        elif grade_eq == 'HS':
            wrat_ge = 12
        elif grade_eq == 'post-HS':
            wrat_ge = 13
        else:
            wrat_ge = grade_eq
        txt_ge = str('(' + grade_eq + ')')
        
    else:
        score = -999
        wrat_ge = -999
        txt_ge = '(?)'
            
    if output == 1:
        wratCalc = score 
    elif output == 2:
        wratCalc = wrat_ge
    elif output == 3:
        wratCalc == txt_ge
        
        
            
    
    