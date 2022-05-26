import os 

for _, _, files in os.walk('.'): 
    if "OnshapeAPIKey.py" in files: 
        exec(open('OnshapeAPIKey.py').read())
        break 

print(access)
print(secret)