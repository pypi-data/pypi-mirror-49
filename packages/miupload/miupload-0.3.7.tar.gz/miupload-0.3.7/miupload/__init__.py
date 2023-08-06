"""
This module provides verification of user's email and password.


"""

import miupload.runningConfiguration as cfg
import requests
import time

name = "miupload"
log = ""

# Check if module is configured and ready.
try:
    if (cfg.configured):
        ready = True
    else:
        ready = False
except:
    ready = False

try:
    if (cfg.base_url):
        base_url = cfg.base_url
    else:
        base_url = "http://sss-data.minerva.community"
except:
    base_url = "http://sss-data.minerva.community"

def get_status():
    """
    For DEBUG. Returns login status and server base_url.
    :return:
    """
    global ready
    global base_url
    print(ready,base_url)
    return ready


def login(email, psw):
    """

    Function checks email password and then saves configuration data for later use.

    :param email:
    :param psw:
    :return:
    """
    global ready
    global base_url
    if (ready):
        Q = input("Module is already configured. Rewrite? (y/n): ")
        if (Q == "y"):
            pass
        else:
            "Answer not recognized. Configuration aborted."
            return None

    print("Contacting data server...")

    r = requests.post(base_url+"/User/validate", data={'email': email, 'psw': psw})
    # FIXME print(r.content)
    if (r.content == b'TRUE'):  # TODO
        print("Verification successful! Saving Configuration...")
        cfg.email = email
        cfg.psw = psw
        cfg.configured = True
        ready = True
    else:
        print("Verification failed! Please check your Minerva email and password. Try again!")
        return False

    print("MiUpload configuration saved successfully!")

def login_gui():
    """
    Ask user to login with prompt for email and password.

    :return:
    """
    return login(input("Enter your Minerva email address: "), input("Enter your activation code/password: "))


def set_server(new_url):
    """
    For DEBUG only. Allows to change server address and redirect communication to alternative server.

    :param url:
    :return:
    """
    global base_url

    cfg.base_url = new_url
    base_url = new_url
    return True


def submit_notebook(assignment = None):
    """

    :param assignment:
    :return:
    """
    global ready
    global base_url
    global log
    if (not ready):
        print("You are not logged in!")
        print("Please run miupload.login_gui()")
        return False
    print("Autosaving notebook...") # save notebook before reading of file
    try:
        from IPython.display import display, Javascript
    except ImportError:
        print("Autosaving failed. Please make sure to save your notebook before submitting notebook.")

    display(Javascript("IPython.notebook.save_notebook()"),
                   include=['application/javascript'])
    time.sleep(3)
    print("Notebook saved.")
    print("Preparing .ipynb upload")
    # Get filename of notebook for uploading
    # Source: https://github.com/jupyter/notebook/issues/1000
    import json
    import os.path
    import re
    import ipykernel
    import requests

    # try:  # Python 3
    #    from urllib.parse import urljoin
    # except ImportError:  # Python 2
    #    from urlparse import urljoin

    # Alternative that works for both Python 2 and 3:
    from requests.compat import urljoin

    try:  # Python 3 (see Edit2 below for why this may not work in Python 2)
        from notebook.notebookapp import list_running_servers
    except ImportError:  # Python 2
        import warnings
        from IPython.utils.shimmodule import ShimWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ShimWarning)
            from IPython.html.notebookapp import list_running_servers

    def get_notebook_name():
        global log
        """
        Return the full path of the jupyter notebook.
        """
        kernel_id = re.search('kernel-(.*).json',
                              ipykernel.connect.get_connection_file()).group(1)
        servers = list_running_servers()
        log += "[DEBUG] Getting Server List\n"
        log += "[DEBUG] Servers:" + repr(servers) + "\n"
        for ss in servers:
            log += "[DEBUG] URL:" + urljoin(ss['url'], 'api/sessions')+ "\n"
            print( str(repr(ss.get('token', ''))))
            log += "[DEBUG] Params:" + str(repr(ss.get('token', '')))+"\n"
            response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                    params={'token': ss.get('token', '')})
            log += "[DEBUG] Response:" + response.text +"\n"
            for nn in json.loads(response.text):
                try:
                    log += "[DEBUG] Kernel:" + str(repr(nn)) + "\n"
                    if nn['kernel']['id'] == kernel_id:
                        relative_path = nn['notebook']['path']
                        return os.path.join(ss['notebook_dir'], relative_path)
                except:
                    log += "[DEBUG] Failed to get kernel:" + repr( nn) + "\n"
                    print("Failed to get filename of notebook from API")
                    print("---> Please copy and paste filename and path of notebook from URL (copy everything after .../notebooks/")
                    relative_path = input("path/filename.ipynb: ")
                    return os.path.join(ss['notebook_dir'], relative_path)
    filename = get_notebook_name()
    files = {'upload_file': open(filename, 'rb')}
    values = {'email': cfg.email, 'assignment': assignment , "debug": log}
    r = requests.post(base_url+"/Notebook/submit", files=files, data=values)
    if (str(r.content, 'utf-8', 'ignore')[0] == "Y"):
        print("Upload successful!")
        print("You can view your submitted notebook on https://nbviewer.jupyter.org/urls/"+base_url.replace("https://","").replace("http://","")+"/uploads/"+str(r.content, 'utf-8', 'ignore')[1:])
        return True
    else:
        print("Upload failed! Error:", str(r.content, 'utf-8', 'ignore'))
        print("Please email your notebook to your peer tutor manualy.")
        return False
