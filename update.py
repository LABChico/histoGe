import os
success = False
try:
	os.system('git pull & pip3 install -r requirements.txt')
    
except:
    pass
else:
    success = True

if success == False: 
    try:
        os.system('git pull & pip install -r requirements.txt')
    except:
        print('ERROR: update cannot be performed. Please update manually.')
