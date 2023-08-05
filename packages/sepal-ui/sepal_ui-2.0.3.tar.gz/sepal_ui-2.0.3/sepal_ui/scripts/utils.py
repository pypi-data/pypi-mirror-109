import os
from pathlib import Path
from urllib.parse import urlparse
import string 
import random
import math
import re
import warnings
from unidecode import unidecode
from functools import wraps

import ee
from cryptography.fernet import Fernet

import sepal_ui

def hide_component(widget):
    """
    hide a vuetify based component
    
    Args:
        widget (v.VuetifyWidget): the widget to hide
    """
    
    if isinstance(widget, sepal_ui.sepalwidgets.sepalwidget.SepalWidget):
        widget.hide()
    elif not 'd-none' in str(widget.class_):
        widget.class_ = str(widget.class_).strip() + ' d-none'
        
    return

def show_component(widget):
    """
    show a vuetify based component
    
    Args:
        widget (v.VuetifyWidget): the widget to hide
    """
    
    if isinstance(widget, sepal_ui.sepalwidgets.sepalwidget.SepalWidget):
        widget.show()
    elif 'd-none' in str(widget.class_):
        widget.class_ = widget.class_.replace('d-none', '')
        
    return
    
def create_download_link(pathname):
    """
    Create a clickable link to download the pathname target
    
    Args:
        pathname (str | pathlib.Path): the pathname th download
        
    Return:
        (str): the download link
    """
    
    if type(pathname) == str:
        pathname = Path(pathname)
        
    result_path = Path(pathname).expanduser()
    home_path = Path('~').expanduser()
    
    # will be available with python 3.9
    #download_path = result_path.relative_to(home_path) if result_path.is_relative_to(home_path) else result_path
    download_path = os.path.relpath(result_path,home_path)
    
    link = f'/api/files/download?path=/{download_path}'
    
    return link

def is_absolute(url):
    """
    Check if the given URL is an absolute or relative path
    
    Args:
        url (str): the URL to test
        
    Return:
        (bool): True if absolute else False
    """
    return bool(urlparse(str(url)).netloc)

def random_string(string_length=3):
    """
    Generates a random string of fixed length. 
    
    Args:
        string_length (int, optional): Fixed length. Defaults to 3.
    
    Return:
        (str): A random string
    """
    
    # random.seed(1001)
    letters = string.ascii_lowercase
    
    return ''.join(random.choice(letters) for i in range(string_length))

def get_file_size(filename):
    """
    Get the file size as string of 2 digit in the adapted scale (B, KB, MB....)
    
    Args:
        filename (str | pathlib.Path): the path to the file to mesure
        
    Return:
        (str): the file size in a readable humanly readable
    """
    
    file_size = Path(filename).stat().st_size
    
    if file_size == 0:
        return "0B"
    
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    
    i = int(math.floor(math.log(file_size, 1024)))
    s = file_size / (1024 ** i)
        
    return '{:.1f} {}'.format(s, size_name[i])

def init_ee():
    """
    Initialize earth engine according to the environment. 
    It will use the creddential file if the EE_PRIVATE_KEY env variable exist. 
    Otherwise it use the simple Initialize command (asking the user to register if necessary)
    """
    
    # only do the initialization if the credential are missing
    if not ee.data._credentials:
        
        # if the decrypt key is available use the decript key 
        if 'EE_DECRYPT_KEY' in os.environ:
        
            # read the key as byte 
            key = os.environ['EE_DECRYPT_KEY'].encode()
            
            # create the fernet object 
            fernet = Fernet(key)
            
            # decrypt the key
            json_encrypted = Path(__file__).parent/'encrypted_key.json'
            with json_encrypted.open('rb') as f:
                json_decripted = fernet.decrypt(f.read()).decode()
                
            # write it to a file
            with open('ee_private_key.json', 'w') as f:
                f.write(json_decripted)
                
            # connection to the service account
            service_account = 'test-sepal-ui@sepal-ui.iam.gserviceaccount.com'
            credentials = ee.ServiceAccountCredentials(service_account, 'ee_private_key.json')
            ee.Initialize(credentials)
        
        # if in local env use the local user credential
        else:
            ee.Initialize()
        
    return

def catch_errors(alert, debug=False):
    """
    Decorator to execute try/except sentence
    and catch errors in the alert message.
    If debug is True then the error is raised anyway
    
    Params:
        alert (sw.Alert): Alert to display errors
        debug (bool): Wether to raise the error or not, default to false
    """
    def decorator_alert_error(func):
        @wraps(func)
        def wrapper_alert_error(*args, **kwargs):
            try:
                value = func(*args, **kwargs)
            except Exception as e:
                alert.add_msg(f'{e}', type_='error')
                if debug:
                    raise e
            return value
        return wrapper_alert_error
    return decorator_alert_error

def need_ee(func):
    """
    Decorator to execute check if the object require EE binding.
    Trigger an exception if the connection is not possible. 
    
    Params:
        func (obj): the object on which the decorator is applied
    """
    @wraps(func)
    def wrapper_ee(*args, **kwargs):
        
        # try to connect to ee 
        try: 
            init_ee()
        except Exception as e:
            raise Exception ('This function needs an Earth Engine authentication')
            
        return func(*args, **kwargs)
        
    return wrapper_ee

def loading_button(alert=None, button=None, debug=False):
    """
    Decorator to execute try/except sentence and toggle loading button object.
    Designed to work within the Tile object, or any object that have a self.btn and self.alert set.
    
    Params:
        button (sw.Btn, optional): Toggled button
        alert (sw.Alert, optional): the alert to display the error message
        debug (bool, optional): wether or not the exception should stop the execution. default to False
    """
    
    def decorator_loading(func):
        
        @wraps(func)
        def wrapper_loading(self, *args, **kwargs):
            
            # set btn and alert
            # Change name of variable to assign it again in this scope
            button_ = self.btn if not button else button
            alert_ = self.alert if not alert else alert

            button_.toggle_loading() # Start loading 
            value = None
            try:
                # Catch warnings in the process function
                with warnings.catch_warnings(record=True) as w:
                    value = func(self, *args, **kwargs)
                
                # Check if there are warnings in the function and append them
                # Use append msg due to several warnings could be triggered
                if w: [
                    alert_.append_msg(warning.message.args[0], type_='warning') 
                    for warning in w
                ]
                  
            except Exception as e:
                alert_.add_msg(f'{e}', 'error')
                if debug:
                    button_.toggle_loading() # Stop loading button if there is an error
                    raise e
                    
            button_.toggle_loading() # Stop loading button
            
            return value
        return wrapper_loading
    return decorator_loading


def normalize_str(msg, folder=True):
    """
    Normalize an str to make it compatible with file naming (no spaces, special chars ...etc)
    
    Params:
        msg (str): the string to sanitise
        folder (optional|bool): if the name will be used for folder naming or for display. if display, <'> and < > characters will be kept 
        
    Return:
        (str): the modified str
    """
    
    regex = '[^a-zA-Z\d\-\_]' if folder else '[^a-zA-Z\d\-\_\ \']'
    
    return re.sub(regex, '_', unidecode(msg))
    