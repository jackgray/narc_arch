from arango import ArangoClient
    
def wratCalc(raw_score, version, age):   
    # print('RAWSCORE: ', raw_score)
    
    # WRAT tables -- lists must be isotropic
    if version == 'blue':
        age2024 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 52, 54, 56, 58, 60, 62, 64, 67, 69, 71, 73, 75, 77, 79, 82, 84, 86, 88, 90, 92, 94, 97, 99, 101, 103, 105, 107, 109, 112, 114, 116, 118, 120, 122]
        age2534 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 52, 54, 56, 58, 60, 62, 64, 67, 69, 71, 73, 75, 77, 79, 82, 84, 86, 88, 90, 92, 94, 97, 99, 101, 103, 105, 107, 109, 112, 114, 116, 118, 120]
        age3544 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 51, 53, 55, 57, 60, 62, 64, 66, 68, 70, 72, 75, 77, 79, 81, 83, 85, 87, 90, 92, 94, 96, 98, 100, 102, 105, 107, 109, 111, 113, 115, 117]
        age4554 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 51, 53, 55, 58, 60, 62, 64, 66, 68, 70, 73, 75, 77, 79, 81, 83, 85, 88, 90, 92, 94, 96, 98, 100, 103, 105, 107, 109, 111, 113, 115, 118]
        age5564 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 46, 48, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119]
        grade_eq = ['preschool','preschool','preschool','preschool','preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'k', 'k', 'k', 'k', 'k', 'k',  1, 1,  1,  1,  1, 2,  2,  2,  2,  2,  3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 8, 8, 'HS',  'HS',  'HS',  'HS',  'HS',  'HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS',  'post-HS']
    
    if version == 'tan':
        age1719 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 52, 54, 56, 59, 61, 63, 66, 68, 70, 73, 75, 77, 79, 82, 84, 86, 89, 91, 93, 96, 98, 100, 103, 105, 107, 109, 112, 114, 116, 119, 121, 123, 126, 128]
        age2024 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 46, 48, 51, 53, 55, 58, 60, 62, 64, 67, 69, 71, 74, 76, 78, 81, 83, 85, 88, 90, 92, 94, 97, 99, 101, 104, 106, 108, 111, 113, 115, 118, 120, 122, 124]
        age2534 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 52, 54, 56, 59, 61, 63, 66, 68, 70, 73, 75, 77, 79, 82, 84, 86, 89, 91, 93, 96, 98, 100, 103, 105, 107, 109, 112, 114, 116, 119, 121, 123]
        age3544 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 46, 49, 51, 53, 56, 58, 60, 63, 65, 67, 70, 72, 74, 76, 79, 81, 83, 86, 88, 90, 93, 95, 97, 100, 102, 104, 106, 109, 111, 113, 116, 118, 120]
        age4554 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 52, 54, 56, 58, 61, 63, 65, 68, 70, 72, 75, 77, 79, 82, 84, 86, 88, 91, 93, 95, 98, 100, 102, 105, 107, 109, 112, 114, 116, 118, 121]
        age5564 = ['below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 'below_45', 45, 47, 49, 51, 53, 55, 57, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121]
        grade_eq = ['preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'preschool', 'k', 'k', 'k', 'k', 'k', 'k', 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 7, 8, 'HS', 'HS', 'HS', 'HS', 'HS', 'HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS', 'post-HS']
    
    if age != 'null' and raw_score in range(0, 57):
        # print(age)
        ## AGE SCORE ##
        if age < 17:
            std_score = -999
        elif age in range(17, 19):
            std_score = age1719[raw_score]
        elif age in range(20, 25):
            std_score = age2024[raw_score]
        elif age in range(25, 35):
            std_score = age2534[raw_score]            
        elif age in range(35, 45):
            std_score = age3544[raw_score]
        elif age in range(45,55):
            std_score = age4554[raw_score]
        elif age in range(55, 65):
            std_score = age5564[raw_score]
        else:
            print('age: ', age)
            # print('\n\nage out of range: ', age)
            std_score = 'error'
        ## GRADE EQUIVALENT ##
        grade_eq = str(grade_eq[raw_score])
        print("grade_eq: ", grade_eq)
        if grade_eq == 'preschool' or grade_eq == 'k':
            grade_score = 0
        elif grade_eq == 'HS':
            grade_score = 12
        elif grade_eq == 'post-HS':
            grade_score = 13
        else: 
            grade_score = int(grade_eq)
        print("grade_score: ", grade_score)
    else:
        std_score = -999
        grade_score = -999
    
    return { 'battery': { 'wrat': { 'standard_score': std_score, 'grade_score': grade_score, 'version': version }}}
 
        
            
    
    