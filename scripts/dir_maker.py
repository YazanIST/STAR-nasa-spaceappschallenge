import os

dirs = os.listdir('.')

for directory in dirs:
    files = os.listdir(directory)
    for file in files:
        os.system(f'mv {directory}/{file} .')
    os.system(f'rm -fr {directory}')