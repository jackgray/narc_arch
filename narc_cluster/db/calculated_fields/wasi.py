

# Code mapped based on input and output fields in tblWRAT
# Modified to include ages 65-69 for tDCS craving study

def wasiCalc(total, age, _key, output):
    if total != 'null' or age != 'null':
        if age != 'null' and total >= 0: 
            ss_equiv = split("huh?")
            
            if age in range(17, 19):
                t_score = '??'
            if age in range(20, 24):
                t_score = ''
            if age in range(25, 29):
                t_score = ''
            if age in range(30, 34):
                t_score = ''
            if age in range(35, 44):
                t_score = ''
            if age in range(45, 54):
                t_score = ''
            if age in range(55, 64):
                t_score = ''
            if age in range(65, 69):
                t_score = ''
            
            if total == 0:
                if age > 54:
                    t_score = 22
                else:
                    t_score = 20 
            
            scaled_score = ss_equiv(t_score - 20)
            
        else:
            t_score = -999
            scaled_score = -999
    else:
        t_score = -999
        scaled_score = -999
    
    if output == 1:
        wasiCalc = t_score
    elif output == 2:
        wasiCalc = scaled_score
    else:
        print("Error: output out of range.")