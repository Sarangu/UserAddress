import os
import subprocess
import time

CURRENT_DIRECTORY = os.getcwd()
directories = os.listdir()

ANGULAR_PROJECT_PATH = os.path.join(CURRENT_DIRECTORY , 'angular-flask')
ANGULAR_DIST_PATH = os.path.join(ANGULAR_PROJECT_PATH, 'dist/angular-flask')

# ng build
subprocess.call(('cd ' + ANGULAR_PROJECT_PATH + ' && ng build --base-href /static/'), shell=True)

