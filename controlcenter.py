#!/usr/bin/python
"""Supplies the control center for OpenDash."""
from __future__ import print_function
from pprint import pprint
import yaml
# from bluepy.btle import Scanner, DefaultDelegate
from bottle import route, run, template, get, post, request, response, static_file, error, redirect
import bluetooth

# @TODO Implement workflow: "First search for bluetooth devices. Then choose which are DashAgents based on device name - automatically pair."
# @TODO Add a additional naming layer in the UI so a DashAgent's MAC address can be bound to a -preferebly unique- name given by the user
# @TODO Add some kind of no-SQL file based database to the project to store agents, configurations etc.
# @TODO Write some high-level wrappers for Selenium to do things like "Find element with <ID> on page <X> and do <ACTION>" inside controlcenter.py
# @TODO Add some kind of plugin system so you can add a "Amazon" plugin which defines some common URLs and then the user only has to add credentials and define which DashAgent should buy what product on Amazon
# @TODO Add some kind of action management where an action can be bound to a DashAgent (effectively it's MAC address)
# @TODO Encapsulate the whole Bluetooth logic into module.

#### Generic functions and helpers
def check_login(username, password):
    """Check if given login is correct."""
    result = dict()
    if username == "test":
        if password == "test":
            result['check'] = True
        else:
            result['check'] = False
            result['error_cause'] = 'inputPassword'
    else:
        result['check'] = False
        result['error_cause'] = 'inputUsername'
    return result

def check_login_cookie(username):
    """Check if client has valid login-cookie."""
    return False

def show_error_page(error_type):
    """Show generic error page based on error type."""
    return template('error', error_type=error_type, current_language=get_language_from_client(), showMenu=True)

def has_login_cookie():
    """Check if the user is logged in and redirects to original target."""
    login_cookie = request.get_cookie('opendash-stayloggedin')
    test = (login_cookie and login_cookie == 'true')
    return bool(test)

def get_language_from_client():
    """Attempt to get the language from the client to set UI language."""
    language_name = 'default'
    accept_language_header = request.headers.get('HTTP_ACCEPT_LANGUAGE')
    if accept_language_header and 'de' in accept_language_header:
        language_name = 'german'
    return load_language_file(language_name)

def load_language_file(lang):
    """Load localized strings."""
    if lang == "" or lang == "default":
        file_handle = open("languages/default.yml")
    else:
        language_filename = "languages/"+lang+".yml"
        file_handle = open(language_filename)
    language_file = yaml.safe_load(file_handle)
    file_handle.close()
    return language_file

#### Routes
@route('/')
def index():
    """Redirect non-specific."""
    redirect('/login')

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

@route('/fonts/bootstrap/<filename>')
def fonts_static_bootstrap(filename):
    """Serve icon webfonts from bootstrap."""
    return static_file(filename, root='./fonts/bootstrap')

@route('/fonts/<filename>')
def fonts_static(filename):
    """Serve webfonts."""
    return static_file(filename, root='./fonts')

#### Login
@get('/login')
def show_login():
    """Show login form to the user."""
    if has_login_cookie():
        redirect('/dashboard')
    else:
        return template('login', current_language=get_language_from_client(), showMenu=False)

@post('/login')
def do_login():
    """Process the login attempt of a user."""
    username = request.forms.get('username')
    password = request.forms.get('password')
    remember = request.forms.get('remember-login')
    login_check_result = check_login(username, password)
    if login_check_result['check']:
        # Success
        if remember:
            max_age = 60 * 60 * 24 * 30 # a month
        max_age = 60 * 60 # an hour
        response.set_cookie('opendash-stayloggedin', 'true', max_age=max_age)
        redirect('/dashboard')
    else:
        # Error
        return template('login', current_language=get_language_from_client(), showMenu=False, invalidateField=login_check_result['error_cause'])

@route('/logout')
def do_logout():
    """Redirect user to the login page, delete login cookies."""
    response.set_cookie('opendash-stayloggedin', 'false')
    redirect('/login')

#### Dashboard
@route('/dashboard')
def show_dashboard():
    """Show the default dashboard."""
    if has_login_cookie():
        return template('dashboard', current_language=get_language_from_client(), showMenu=True)
    else:
        redirect('/login')

@route('/dashboard/get_actions_from/<agent_id>')
def get_actions_from_agent(agent_id):
    """Return all actions associated with the agent, whose ID is given."""
    actions = bluetooth.shelf_manager.get_agents()[str(agent_id)]['actions']
    return pprint(actions)

@route('/dashboard/change_name_of/<agent_id>/to/<name>')
def change_name_of_agent(agent_id, name):
    """Change the name of one the agent, whose ID is given."""
    current_name = bluetooth.shelf_manager.get_agent(agent_id)['custom_name']
    new_name = str(name)
    if str(new_name) != current_name:
        bluetooth.shelf_manager.change_name(agent_id, new_name)
    redirect('/dashboard')

@route('/dashboard/get_mock_agents')
def get_mock_agents():
    """Return all paired agents from shelve and return HTML containing them."""
    #bluetooth.connect_mock_nearby_agents(time=4, amount=5, dash_agents=0)
    list_of_agents = bluetooth.shelf_manager.get_agents()
    number_of_agents = len(list_of_agents)
    agent_list_html = ''
    iterator = 0

    if number_of_agents > 0:
        agent_list_html += '<div class="agents">'
        for dummy in list_of_agents:
            iterator += 1
            agent_name = list_of_agents[str(iterator)]['custom_name']
            agent_list_html += '<div class="agent">'
            agent_list_html += '<h4>' + agent_name + '</h4>'
            agent_list_html += '<p>' + get_language_from_client()['agent_address'] + ': ' + list_of_agents[str(iterator)]['addr'] + '</p>'
            agent_list_html += '<button id="edit_actions" data-toggle="modal" data-target="#agent_edit_actions" class="btn btn-default" type="button" name="'+get_language_from_client()['agent_edit_actions']+'"><span class="glyphicon glyphicon-pencil"></span> '+get_language_from_client()['agent_edit_actions']+'</button>'
            agent_list_html += '<button id="change_name" data-toggle="modal" data-current_name="'+agent_name+'" data-agent-id="'+str(iterator)+'" data-target="#agent_edit_name" class="btn btn-default" type="button" name="'+get_language_from_client()['agent_edit_name']+'"><span class="glyphicon glyphicon-erase"></span> '+get_language_from_client()['agent_edit_name']+'</button>'
            agent_list_html += '</div>'
        agent_list_html += '</div>'
    return agent_list_html

#### Template Tests
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

#### Start development server
run(host='localhost', port=8585)

#### Start test production server
# run(host='0.0.0.0', port=80)
