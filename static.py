import os
import subprocess
import time

CURRENT_DIRECTORY = os.getcwd()
directories = os.listdir()

ANGULAR_PROJECT_PATH = os.path.join(CURRENT_DIRECTORY , 'angular-flask')
ANGULAR_DIST_PATH = os.path.join(ANGULAR_PROJECT_PATH, 'dist/angular-flask')
FLASK_STATIC_PATH = os.path.join(CURRENT_DIRECTORY, 'static')
FLASK_TEMPLATES_PATH = os.path.join(CURRENT_DIRECTORY, 'templates')

subprocess.call(('cd ' + FLASK_STATIC_PATH + ' && rm -rf *.js *.ico'), shell=True)
subprocess.call(('cd ' + FLASK_TEMPLATES_PATH + ' && rm -rf *.html'), shell=True)

# ng build
# subprocess.call(('cd ' + ANGULAR_PROJECT_PATH + ' && ng build --base-href /static/'), shell=True)

try:
    files = os.listdir(ANGULAR_DIST_PATH)
    static_files = ''
    html_files = ''

    for file in files:
        if '.js' in file or '.js.map' in file or '.ico' in file:
            static_files += (file + ' ')
        if '.html' in file:
            html_files += (file + ' ')

    if len(static_files) > 0:
        subprocess.call(('cd ' + ANGULAR_DIST_PATH + ' && cp ' + static_files + FLASK_STATIC_PATH), shell=True)
    if len(html_files) > 0:
        subprocess.call(('cd ' + ANGULAR_DIST_PATH + ' && cp ' + html_files + FLASK_TEMPLATES_PATH), shell=True)

except Exception as e:
    print('Error ', e)

