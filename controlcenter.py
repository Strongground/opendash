#!/usr/bin/python
"""Supplies the control center functionalities for OpenDash."""
from __future__ import print_function
# from pprint import pprint
import yaml
# from bluepy.btle import Scanner, DefaultDelegate
from bottle import Bottle, template, request, response, static_file, redirect, debug
import bluetooth
import agent_shelf

# @TODO Implement workflow: "First search for bluetooth devices. Then choose which are DashAgents based on device name - automatically pair."
# @TODO Add a additional naming layer in the UI so a DashAgent's MAC address can be bound to a -preferebly unique- name given by the user
# @TODO Write some high-level wrappers for Selenium to do things like "Find element with <ID> on page <X> and do <ACTION>" inside controlcenter.py
# @TODO Add some kind of plugin system so you can add a "Amazon" plugin which defines some common URLs and then the user only has to add credentials and define which DashAgent should buy what product on Amazon
# @TODO Add some kind of action management where an action can be bound to a DashAgent (effectively it's MAC address/unique ID)
# @TODO If receive a POST from actions_overview, validate which form was posted (attribute "form_type") and if "create_action" call the appropiate method "actions_create_new(action_object)".

class ControlCenter(object):
    """This is the main class of DashControl. It handles DashAgent calls and serves the GUI to administrate them and the actions bound to them."""

    def __init__(self, verbose, force_shelf_creation, scan_mode):
        """Inititalize control center."""
        self._app = Bottle()
        self.verbose = verbose
        self.force_shelf_creation = force_shelf_creation
        self.scan_mode = scan_mode
        # self.debug_mode = debug_mode
        self.shelf_manager = agent_shelf.AgentShelfManager('agent_shelf')
        self.bluetooth_manager = bluetooth.BluetoothManager(shelf_manager=self.shelf_manager)
        self._route()

    ### route method
    def _route(self):
        # framework
        self._app.route('/js/<filename>', method="GET", callback=self.js_static)
        self._app.route('/js/bootstrap/<filename>', method="GET", callback=self.js_static_bootstrap)
        self._app.route('/img/<filename>', method="GET", callback=self.img_static)
        self._app.route('/css/<filename>', method="GET", callback=self.css_static)
        self._app.route('/fonts/bootstrap/<filename>', method="GET", callback=self.fonts_static_bootstrap)
        self._app.route('/fonts/<filename>', method="GET", callback=self.fonts_static)
        # content
        self._app.route('/', method="GET", callback=self.index)
        self._app.route('/login', method="GET", callback=self.show_login)
        self._app.route('/login', method="POST", callback=self.do_login)
        self._app.route('/logout', method="GET", callback=self.do_logout)
        self._app.route('/dashboard', method="GET", callback=self.show_dashboard)
        self._app.route('/dashboard/get_actions_from/<agent_id>', method="GET", callback=self.get_actions_from_agent)
        self._app.route('/dashboard/add_mock_action/<action_string>/to/<agent_id>', method="GET", callback=self.add_action_to_agent)
        self._app.route('/dashboard/change_name_of/<agent_id>/to/<name>', method="GET", callback=self.change_name_of_agent)
        self._app.route('/dashboard/get_mock_agents', method="GET", callback=self.get_mock_agents)
        self._app.route('/actions_overview', method="GET", callback=self.show_actions)
        self._app.route('/actions_overview', method="POST", callback=self.handle_form)
        self._app.route('/testerror/<errortype>', method="POST", callback=self.show_error)
        self._app.error(code=500)(self.error500)
        self._app.error(code=404)(self.error404)

    #### Helper methods
    def check_login(self, username, password):
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

    def check_login_cookie(self, username):
        """Check if client has valid login-cookie."""
        return False

    def show_error_page(self, error_type):
        """Return generic error page based on error type."""
        return template('error', error_type=error_type, current_language=self.get_language_from_client(), showMenu=True)

    def has_login_cookie(self):
        """Check if the user is logged in and redirects to original target."""
        login_cookie = request.get_cookie('opendash-stayloggedin')
        test = (login_cookie and login_cookie == 'true')
        return bool(test)

    def get_language_from_client(self):
        """Attempt to get the language from the client to set UI language."""
        language_name = 'default'
        accept_language_header = request.headers.get('HTTP_ACCEPT_LANGUAGE')
        if accept_language_header and 'de' in accept_language_header:
            language_name = 'german'
        return self.load_language_file(language_name)

    def load_language_file(self, lang):
        """Load localized strings."""
        if lang == '' or lang == 'default':
            file_handle = open('languages/default.yml')
        else:
            language_filename = 'languages/'+lang+'.yml'
            file_handle = open(language_filename)
        language_file = yaml.safe_load(file_handle)
        file_handle.close()
        return language_file

    def start(self, debug_mode):
        """Default start for server."""
        print('Run start()')
        if debug_mode:
            print('In Debug mode')
            #### Start development server
            debug(True)
            self._app.run(host='localhost', port=8585)
        else:
            print('In Production mode')
            #### Start test production server
            self._app.run(host='0.0.0.0', port=80)

    #### Route Methods
    def index(self):
        """Redirect non-specific."""
        redirect('/login')

    def js_static(self, filename):
        """Serve static JS."""
        return static_file(filename, root='./js')

    def js_static_bootstrap(self, filename):
        """Serve static bootstrap JS modules."""
        return static_file(filename, root='./js/bootstrap')

    def img_static(self, filename):
        """Serve static image files."""
        return static_file(filename, root='./img')

    def css_static(self, filename):
        """Serve static css files."""
        return static_file(filename, root='./css')

    def fonts_static_bootstrap(self, filename):
        """Serve icon webfonts from bootstrap."""
        return static_file(filename, root='./fonts/bootstrap')

    def fonts_static(self, filename):
        """Serve webfonts."""
        return static_file(filename, root='./fonts')

    #### Login
    def show_login(self):
        """Return login form to the user."""
        if self.has_login_cookie():
            redirect('/dashboard')
        else:
            return template('login', current_language=self.get_language_from_client(), showMenu=False)

    def do_login(self):
        """Process the login attempt of a user."""
        username = request.forms.get('username')
        password = request.forms.get('password')
        remember = request.forms.get('remember-login')
        login_check_result = self.check_login(username, password)
        if login_check_result['check']:
            # Success
            if remember:
                max_age = 60 * 60 * 24 * 30 # a month
            max_age = 60 * 60 # an hour
            response.set_cookie('opendash-stayloggedin', 'true', max_age=max_age)
            redirect('/dashboard')
        else:
            # Error
            return template('login', current_language=self.get_language_from_client(), showMenu=False, invalidateField=login_check_result['error_cause'])

    def do_logout(self):
        """Redirect user to the login page, delete login cookies."""
        response.set_cookie('opendash-stayloggedin', 'false')
        redirect('/login')

    #### Dashboard
    def show_dashboard(self):
        """Return the default dashboard."""
        if self.has_login_cookie():
            return template('dashboard', current_language=self.get_language_from_client(), showMenu=True, currentpage='dashboard')
        else:
            redirect('/login')

    def get_actions_from_agent(self, agent_id):
        """Return all actions associated with the agent, whose ID is given."""
        actions = self.shelf_manager.get_agents()[str(agent_id)]['actions']
        action_list_html = ''
        number_of_actions = len(actions)
        if number_of_actions > 0:
            for action in actions:
                action_list_html += '<tr>'
                action_list_html += '<td>' + str(action) + '</td>'
                action_list_html += '<td>' + self.shelf_manager.get_agents()[str(agent_id)]['actions'][action] + '</td>'
                action_list_html += '</tr>'
        return action_list_html

    def add_action_to_agent(self, agent_id, action_string):
        """Add a single string to the action array of the agent, whose ID is given."""
        self.shelf_manager.agent_add_mock_action(agent_id, action_string)
        redirect('/dashboard')

    def change_name_of_agent(self, agent_id, name):
        """Change the name of one the agent, whose ID is given."""
        current_name = self.shelf_manager.get_agent(agent_id)['custom_name']
        new_name = str(name)
        if str(new_name) != current_name:
            self.shelf_manager.agent_change_name(agent_id, new_name)
        redirect('/dashboard')

    def get_mock_agents(self):
        """Return all paired agents from shelve and return HTML containing them."""
        list_of_agents = self.shelf_manager.get_agents()
        number_of_agents = len(list_of_agents)
        agent_list_html = ''
        if number_of_agents > 0:
            for agent in list_of_agents:
                agent_name = list_of_agents[agent]['custom_name']
                agent_list_html += '<div class="agent">'
                agent_list_html += '<h4>' + agent_name + '</h4>'
                agent_list_html += '<p>' + self.get_language_from_client()['agent_address'] + ': ' + list_of_agents[agent]['addr'] + '</p>'
                agent_list_html += '<button id="edit_actions" data-toggle="modal" data-target="#agent_edit_actions" data-agent-id="'+agent+'" class="btn btn-default" type="button" name="'+self.get_language_from_client()['agent_edit_actions']+'"><span class="glyphicon glyphicon-pencil"></span> '+self.get_language_from_client()['agent_edit_actions']+'</button>'
                agent_list_html += '<button id="change_name" data-toggle="modal" data-current_name="'+agent_name+'" data-agent-id="'+agent+'" data-target="#agent_edit_name" class="btn btn-default" type="button" name="'+self.get_language_from_client()['agent_edit_name']+'"><span class="glyphicon glyphicon-erase"></span> '+self.get_language_from_client()['agent_edit_name']+'</button>'
                agent_list_html += '</div>'
        return agent_list_html

    #### 'Manage Actions' Panel
    def show_actions(self):
        """Return the action overview template."""
        return template('actions_overview', current_language=self.get_language_from_client(), showMenu=True, list_of_actions=self.shelf_manager.actions_show_all(), currentpage='actions')

    def handle_form(self):
        """Handle the sent form."""
        form_type = request.forms.get('form_type')
        action_uid = request.forms.get('action_uid')
        if form_type == 'create_action':
            action = {
                'custom_name':          request.forms.get('new_action_name'),
                'plugin':               request.forms.get('plugin'),
                'extended_parameters':  request.forms.get('extended-params')
            }
            self.shelf_manager.actions_create_new(action)
            redirect('/actions_overview')
        elif form_type == 'edit_action':
            self.shelf_manager.update_attributes(action_uid, request.forms)
        elif form_type == 'open_modal':
            return template('actions_overview', current_language=self.get_language_from_client(), showMenu=True, list_of_actions=self.shelf_manager.actions_show_all(), currentpage='actions', open_modal='edit_action', action_uid=action_uid)

    #### Error pages
    def show_error(self, errortype):
        """Return error page for given error type."""
        return self.show_error_page(errortype)

    def error404(self, httperror):
        """Return 404 error page."""
        return self.show_error('404')

    def error500(self, httperror):
        """Return 500 error page."""
        return self.show_error('500')
