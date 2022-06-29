debug=True
def log(message):
    if globals()['debug'] == True:
        print('\n', message, '\n')
    elif globals()['debug'] == False:
        pass
    else:
        print("Debugging variable not found. You might be missing log messages!")