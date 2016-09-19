#!/usr/bin/python
"""Supplies the control center for OpenDash."""
#from bluepy import *
from __future__ import print_function
import yaml
# from bluepy.btle import Scanner, DefaultDelegate
from bottle import route, run, template, get, post, request, static_file, error

# @TODO Add cookie based login
# @TODO Fix login/logout using the same functions, yet duplicating the routes stinks
# @TODO Adding dummy object for bluetooth btle.scanEntry to model behaviour
# @TODO Add way to actively scan for bluetooth devices and show the results on the dashboard

#### Bluetooth mock
class Scanner(object):
    """Mock scanner class."""

    def scan(self, duration):
        """Return mock data from a discovered bluetooth device."""
        mock_devices = {
            'mock_device' : {
                'addr' : '08:df:1f:c4:a5:1e',
                'addrType' : 'public',
                'iface' : 0,
                'rssi' : -58,
                'connectable' : True,
                'updateCount' : 1
            }
        }
        return mock_devices


# @TODO try to get this via clever guessing from browser and allow to set via preferences in opendash itself
# currently this is hardcoded, change this to <language name> to test UI in that language, if there is a
# corresponding languagename.yml in the "languages" folder
language = ""

def load_language(lang):
    """Load localized strings."""
    if lang == "" or lang == "default":
        file_handle = open("languages/default.yml")
    else:
        language_filename = "languages/"+lang+".yml"
        file_handle = open(language_filename)
    set_language = yaml.safe_load(file_handle)
    file_handle.close()
    return set_language

current_language = load_language(language)

#### Generic
@route('/js/<filename>')
def js_static(filename):
    """Serve static JS."""
    return static_file(filename, root='./js')

@route('/js/bootstrap/<filename>')
def js_static_bootstrap(filename):
    """Serve static bootstrap JS modules."""
    return static_file(filename, root='./js/bootstrap')

@route('/img/<filename>')
def img_static(filename):
    """Serve static image files."""
    return static_file(filename, root='./img')

@route('/css/<filename>')
def css_static(filename):
    """Serve static css files."""
    return static_file(filename, root='./css')

#### Login
@get('/login')
def show_login():
    """Show login form to the user."""
    return template('login', current_language=current_language, showMenu=False)

@post('/login')
def do_login():
    """Process the login attempt of a user."""
    username = request.forms.get('username')
    password = request.forms.get('password')
    print("Entered: " + username + " and " + password)
    login_check_result = check_login(username, password)
    if login_check_result['check']:
        return template('dashboard', current_language=current_language, showMenu=True)
    else:
        return template('login', current_language=current_language, showMenu=False, invalidateField=login_check_result['error_cause'])

@get('/logout')
def do_logout():
    """Log the user out."""
    return template('login', current_language=current_language, showMenu=False)

#### Template Tests
@route('/dashboard')
def show_dashboard():
    """Show the default dashboard."""
    return template('dashboard', current_language=current_language, showMenu=True)

@route('/testerror/<errortype>')
def show_error(errortype):
    """Show error page for given error type."""
    return show_error_page(errortype)

#### Error pages
@error(404)
def error404(error):
    """Return 404 error page."""
    return show_error('404')

@error(500)
def error500(error):
    """Return 500 error page."""
    return show_error('500')

#### Generic functions
def check_login(username, password):
    """Check if given login is correct."""
    result = dict()
    print("comparing " + username + " and " + password + " against 'test'")
    if username == "test":
        if password == "test":
            result['check'] = True
        else:
            result['check'] = False
            result['error_cause'] = 'inputPassword'
    else:
        result['check'] = False
        result['error_cause'] = 'inputEmail'
    return result

def check_login_cookie(username):
    """Check if client has valid login-cookie."""
    return False

def show_error_page(error_type):
    """Show generic error page based on error type."""
    return template('error', error_type=error_type, current_language=current_language, showMenu=True)

#### Start development server
run(host='localhost', port=8585)
