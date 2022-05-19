    
def wasiCalc(raw_score, age):   
    
    # WASI tables -- lists must be isotropic
    ss_eq = [1,1,2,2,2,3,3,3,3,4,4,4,5,5,5,6,6,6,6,7,7,7,8,8,8,9,9,9,9,10,10,10,11,11,11,12,12,12,12,13,13,13,14,14,14,15,15,15,15,16,16,16,17,17,17,18,18,18,18,19,19]

    if age != 'null' and raw_score >= 0:
        # print(age)
        ## AGE SCORE ##
        if age < 17:
            tscore = -999
        # really 17-19, etc, but range does not include last digit
        elif age in range(17, 20):
            tscore_arr = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67]
        elif age in range(20, 25):
            tscore_arr = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69] 
        elif age in range(25, 30):
            tscore_arr = [20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70]           
        elif age in range(30, 35):
            tscore_arr = [20, 20, 20, 20, 20, 20, 20, 22, 24, 25, 27, 29, 30, 32, 34, 36, 37, 39, 41, 43, 45, 47, 49, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72]
        elif age in range(35,45):
            tscore_arr = [20, 20, 20, 20, 21, 22, 24, 25, 27, 29, 30, 32, 34, 36, 37, 39, 40, 42, 44, 46, 47, 48, 49, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72] 
        elif age in range(45, 55):
            tscore_arr = [20, 21, 23, 24, 25, 27, 28, 30, 31, 33, 34, 36, 38, 39, 41, 42, 44, 45, 47, 49, 50, 52, 53, 54, 56, 58, 59, 61, 63, 65, 67, 69]  
        elif age in range(55, 65):
            tscore_arr = [23, 24, 26, 27, 28, 30, 31, 33, 34, 36, 37, 39, 41, 42, 44, 45, 47, 49, 50, 52, 53, 55, 57, 58, 59, 61, 62, 64, 66, 68, 70, 72]
        elif age in range(65,70):
            tscore_arr = [25, 26, 28, 29, 30, 32, 34, 35, 37, 38, 40, 41, 43, 44, 46, 48, 49, 51, 52, 54, 55, 57, 59, 60, 62, 63, 65, 67, 69, 71, 73, 75]
        else:
            tscore_arr = ['error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error', 'error']
        print('age: ', age)
        print('raw score: ', raw_score)
        print('len: ', len(tscore_arr))
        tscore = tscore_arr[raw_score-1] # python indexes go from [0:n-1]
        
        if raw_score == 0:
            tscore = 20
            if age > 54:
                tscore = 22
        
        ss_index = tscore - 20
        scaled_score = ss_eq[ss_index]
        
    else:
        tscore = -999
        scaled_score = -999
    
    return { 'assessment': { 'wasi': { 't_score': tscore, 'scaled_score': scaled_score }}}