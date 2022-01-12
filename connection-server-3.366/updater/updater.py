import os
import subprocess
import sys
import signal
import time
import json
import re
import crypt
import commands
from threading import Thread
from time import sleep
from datetime import timedelta
from flask import Flask, Response, url_for, request, render_template, redirect, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
import requests
import hashlib


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



g_status_mapping_index = {
    "STATUS_READY":             0,
    "STATUS_UPLOADING":         1,
    "STATUS_CHECKING_FILE":     2,
    "STATUS_STOPPING_SERVER":   3,
    "STATUS_CREATING_BACKUP":   4,
    "STATUS_INSTALL":           5,
    "STATUS_SUCCESS":           6,
    "STATUS_FAIL":              7,
    "STATUS_RESTORING_BACKUP":  8,
    "STATUS_REBOOTING_SERVER":  9,
    "STATUS_UNPACKING_FILE":    10,
    "STATUS_REMOVING_DATA":     11,
    "STATUS_DOWNLOADING":       12
}

g_status_mapping_label = {
    0: "Ready for update",
    1: "Uploading file ...",
    2: "Checking uploaded file ...",
    3: "Waiting until CS stop ...",
    4: "Creating backup ...",
    5: "Installing CS ...",
    6: "Installation done",
    7: "Installation failed",
    8: "Restoring backup ...",
    9: "Waiting until CS start ...",
    10: "Unpacking file ...",
    11: "Removing installation files ...",
    12: "Downloading file ..."
}


UPLOAD_FOLDER = '/opt/updater/updater/install'
TEMP_FOLDER = '/opt/updater/temp'
APP_FOLDER = '/opt/updater/updater'

IMM_VERSION_PATH = '/opt/imm/imm_server/web/version'
IMM_OLD_VERSION_PATH = '/opt/imm.old/imm_server/web/version'
UPDATER_VERSION_PATH = '/opt/updater/temp/version'
UPDATER_OLD_VERSION_PATH = '/opt/updater/updater/version'

UPDATER_SERVICE_NAME = 'updater_server'

ALLOWED_EXTENSIONS = {'gz'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


# config
app.config.update(
    ENV = 'development',
    DEBUG = True,
    TESTING = True,
    SECRET_KEY = 'elkoep'
)


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def handler(signal, frame):
    print('CTRL-C pressed!')
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "name"
        self.password = "password"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


g_logfile = ""

g_status = {
    "file_uploaded": False,
    "file_error": "",
    "file_name": "",
    "status": g_status_mapping_index["STATUS_READY"],
    "error": False,
    "msg": "",
    "backup_version": "",
    "current_version": "",
    "update": False,
    "version": "",
}


ELKO_UPDATE_SERVER_URL = "http://217.197.144.56:4434/cs/files/fw.info.json"


def load_log_file():
    log = ""
    try:
        with open("%s/log/output.log" % APP_FOLDER, "r") as f:
            log = f.read()
    except:
        pass
    return log
    

def save_log_file():
    try:
        with open("%s/log/output.log" % APP_FOLDER, "w") as f:
            f.write(g_logfile)
    except:
        pass


def threaded_function_install(filename):
    global g_logfile
    global g_status
    
    g_logfile = ""

    filename = filename.replace(".tar.gz", "")
    
    g_status["status"] = g_status_mapping_index["STATUS_STOPPING_SERVER"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("bash %s/update.sh %s 1" % (APP_FOLDER, filename), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line
        
    sleep(60)

    g_status["status"] = g_status_mapping_index["STATUS_CREATING_BACKUP"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("bash %s/update.sh %s 2" % (APP_FOLDER, filename), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line
    
    sleep(1)  
        
    g_status["status"] = g_status_mapping_index["STATUS_UNPACKING_FILE"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("bash %s/update.sh %s 4" % (APP_FOLDER, filename), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line
    
    sleep(1)
    
    g_status["status"] = g_status_mapping_index["STATUS_INSTALL"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("echo -ne '\n' | bash %s/update.sh %s 5" % (APP_FOLDER, filename), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line

    sleep(1)
        
    g_status["status"] = g_status_mapping_index["STATUS_REMOVING_DATA"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("bash %s/update.sh %s 6" % (APP_FOLDER, filename), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line
        
    sleep(1)

    g_status["status"] = g_status_mapping_index["STATUS_REBOOTING_SERVER"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    g_logfile += "All done \r\n"
    save_log_file()

    sleep(5)

    commands.getstatusoutput("sudo reboot")
      

def threaded_function_backup():
    global g_logfile
    global g_status
    
    g_logfile = ""
    
    g_status["status"] = g_status_mapping_index["STATUS_STOPPING_SERVER"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("bash %s/update.sh %s 1" % (APP_FOLDER, "imm"), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line
        
    sleep(60)
        
    g_status["status"] = g_status_mapping_index["STATUS_RESTORING_BACKUP"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    p = subprocess.Popen("bash %s/update.sh %s 3" % (APP_FOLDER, "imm"), shell=True, stdout=subprocess.PIPE)
    for line in p.stdout:
        g_logfile += line
    
    sleep(1)

    g_status["status"] = g_status_mapping_index["STATUS_REBOOTING_SERVER"]
    g_logfile += "%s \r\n" % g_status_mapping_label[g_status["status"]]
    g_logfile += "All done \r\n"
    save_log_file()

    sleep(5)

    commands.getstatusoutput("sudo reboot")
      
      
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
@app.route('/logfile', methods=['GET'])
@login_required
def updater_logfile():
    return app.response_class(g_logfile, mimetype='text/plain')
    
    
@app.route('/status', methods=['GET'])
@login_required
def updater_status():

    try:
        with open("%s" % IMM_OLD_VERSION_PATH, 'r') as f:
            g_status["backup_version"] = f.read()
    except:
        g_status["backup_version"] = ""

    try:
        with open("%s" % IMM_VERSION_PATH, 'r') as f:
            g_status["current_version"] = f.read()
    except:
        g_status["current_version"] = ""

    g_status["update"] = False
        
    try:
        with open("%s" % UPDATER_OLD_VERSION_PATH, "r") as f:
           version_old = f.read()
           g_status["version"] = version_old
    except:
        g_status["version"] = ""
        
    return app.response_class(json.dumps(g_status), mimetype='application/json')


def download_file(url):
    filename = url.split('/')[-1]
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return filename


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

    
@app.route('/', methods=['GET', 'POST'])
@login_required
def updater_main():
    global g_status
    global g_logfile
    
    if request.method == 'POST':
        
        if "btn_upload" in request.values and 'file' in request.files:
            if g_status["status"] == g_status_mapping_index["STATUS_READY"]:
                g_status["status"] = g_status_mapping_index["STATUS_UPLOADING"]
                try:
                    file = request.files['file']

                    if file.filename == '':
                        g_status["file_uploaded"] = False
                        g_status["file_error"] = "No file selected"
                        g_status["file_name"] = ""

                    elif file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)

                        g_status["file_uploaded"] = True
                        g_status["file_error"] = ""
                        g_status["file_name"] = filename

                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    else:
                        g_status["file_uploaded"] = False
                        g_status["file_error"] = "File not allowed"
                        g_status["file_name"] = ""
                except:
                    g_status["file_uploaded"] = False
                    g_status["file_error"] = "Cannot upload installation file"
                    g_status["file_name"] = ""
                g_status["status"] = g_status_mapping_index["STATUS_READY"]

        if "btn_download" in request.values and 'file' in request.files:
            if g_status["status"] == g_status_mapping_index["STATUS_READY"]:
                g_status["status"] = g_status_mapping_index["STATUS_DOWNLOADING"]
                try:
                    file_info = requests.get("http://217.197.144.56:4434/cs/files/fw.info.json", timeout=5).json()

                    file_url = file_info["file"]
                    file_hash = file_info["hash"]
                    file_version = file_info["version"]

                    filename = download_file(file_url)

                    if md5(filename) == file_hash:
                        g_status["file_uploaded"] = True
                        g_status["file_error"] = ""
                        g_status["file_name"] = filename
                    else:
                        g_status["file_uploaded"] = False
                        g_status["file_error"] = "Wrong file HASH"
                        g_status["file_name"] = ""
                except:
                    g_status["file_uploaded"] = False
                    g_status["file_error"] = "Cannot download installation file"
                    g_status["file_name"] = ""
                g_status["status"] = g_status_mapping_index["STATUS_READY"]

        if "btn_start_update" in request.values:
            if g_status["status"] == g_status_mapping_index["STATUS_READY"] and g_status["file_name"]:
                thread_install = Thread(target = threaded_function_install, args=(g_status["file_name"],))
                thread_install.start()
            
        if "btn_restore_backup" in request.values:
            if g_status["status"] == g_status_mapping_index["STATUS_READY"]:
                if os.path.isfile("%s" % IMM_OLD_VERSION_PATH):
                    thread_backup = Thread(target = threaded_function_backup)
                    thread_backup.start()
            
        if "btn_log_clear" in request.values:
            g_logfile = ""
            save_log_file()
            
        if "btn_log_download" in request.values:
            return app.response_class(load_log_file(), mimetype='text/plain', headers={"Content-disposition": "attachment; filename=output.log"})
            
        if "btn_restart_service" in request.values:
            p = subprocess.Popen("/etc/init.d/%s restart" % UPDATER_SERVICE_NAME, shell=True, stdout=subprocess.PIPE)
            sleep(5)
            
    return render_template('index.html')

    
@app.route('/login', methods=['GET', 'POST'])
def login(address=None, interval=None):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']    

        login_success = False
        
        if username == "admin" or username == "imm":
            stored_hash = ''
            try:
                p = subprocess.Popen(["sudo", "python", "-c", "import spwd; p=spwd.getspnam('imm'); print p.sp_pwd"], stdout=subprocess.PIPE)
                stored_hash = p.communicate()[0].strip()
            except Exception as e:
                print e

            if stored_hash:
                salt_pattern = re.compile(r"\$.*\$.*\$")
                salt = salt_pattern.match(stored_hash).group()
                generated_hash = crypt.crypt(password, salt)
                if generated_hash == stored_hash:
                    login_success = True

        if login_success:
            id = 1
            user = User(id)
            login_user(user)
            return redirect('/')
        else:
            return abort(401)
    else:
        return render_template('login.html')

        
# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
        
        
# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return redirect('/')
        
   
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
   
   
if __name__ == '__main__':
    g_logfile = load_log_file()
    app.run(host='0.0.0.0', debug=True, port=8081)
    
    