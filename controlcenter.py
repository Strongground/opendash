#!/usr/bin/python
"""Supplies the control center for OpenDash."""
#from bluepy import *
from __future__ import print_function
from bottle import route, run, template, get, post, request

# peripheral = blte.Peripheral()
# if perhipheral:
#     print "Created perhipheral"

# target_name = "My Phone"
# target_address = None
#
# nearby_devices = bluetooth.discover_devices()
#
# for bdaddr in nearby_devices:
#     if target_name == bluetooth.lookup_name( bdaddr ):
#         target_address = bdaddr
#         break
#
# if target_address is not None:
#     print "found target bluetooth device with address ", target_address
# else:
#     print "could not find target bluetooth device nearby"

#### Login page

@route('/')
def index():
    """Show index page."""
    return '<h1>Index Page</h1>'

@route('/<action>/<name>')
def doAction(action, name):
    """Do action if defined as possible action."""
    allowed_actions = {
        'greet',
        'curse',
        'woo'
    }
    if action in allowed_actions:
        return template('<h2>{{name}} shall be {{action}}ed!</h2>', name=name, action=action)
    else:
        return template('<h2>Sorry, the action "{{action}}" could not be found!</h2>', action=action)

@get('/login')
def show_login():
    """Show login form to the user."""
    if not check_login_cookie:
        return '''
            <form action="/login" method="post">
                Username: <input name="username" type="text" />
                Password: <input name="password" type="password" />
                <input value="Login" type="submit" />
            </form>
        '''

@post('/login')
def do_login():
    """Process the login attempt of a user."""
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p style='color: green; font-weight: bold;'>You are successfully logged in!</p>"
    else:
        return "<p style='color: red; font-weight: bold;'>Login failed.</p>"


#### Generic functions
def check_login(username, password):
    """Check if given login is correct."""
    if username == "noel" and password == "root":
        return True
    else:
        return False

def check_login_cookie(username):
    """Check if has valid login-cookie."""
    pass

#### Start development server
run(host='localhost', port=8585)
