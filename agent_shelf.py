#!/usr/bin/python
"""
This module provides high-level wrapper functions for the shelves containing all data.

It exposes several functions that can be used to return all entries of paired DashAgents and the data assigned to them, as well as
adding and modifying these. It also contains functions to work with functions.
"""
from __future__ import print_function
from pprint import pprint
import shelve

class AgentShelfManager(object):
    """This class wraps all the required functions to communicate with the local shelve database storing DashAgents."""

    database = None

    def __init__(self, database_name):
        """Open a shelve database on init of this class."""
        try:
            self.database = shelve.open(database_name, writeback=True)
        except Exception as e:
            print('Error opening shelf: '+str(e))
            raise

    @classmethod
    def close_db(cls):
        """Close the currently open shelve database."""
        try:
            cls.database.close()
            return True
        except Exception as e:
            print('Error closing shelf: '+str(e))
            raise

    def store_agent(self, device):
        """Handle the data of a recently found DashAgent and add some additional data."""
        try:
            index = str(len(self.database['agents'])+1)
            device['custom_name'] = ('Dash Agent '+index)
            device['actions'] = {}
            self.database['agents'][index] = device
            return True
        except Exception as e:
            print('Error storing agent: '+str(e))
            raise

    def get_agents(self):
        """Return all agents from shelf as dict."""
        try:
            return dict(self.database['agents'])
        except Exception as e:
            print('Error getting agents: '+str(e))
            raise

    def get_agent(self, agent_id):
        """Get a specific agent from shelf and return as dict."""
        try:
            return dict(self.database['agents'][str(agent_id)])
        except Exception as e:
            print('Error getting agent with id '+str(agent_id)+': '+str(e))
            raise

    def show_content(self):
        """Use for debugging purposes, shows the whole content of the database in legible manner."""
        try:
            return pprint(self.database)
        except Exception as e:
            print('Error showing database content: '+str(e))
            raise

    def show_entry(self, key):
        """Use for debugging purposes, shows the content of one particular entry of the database in legible manner."""
        try:
            return pprint(self.database[str(key)])
        except Exception as e:
            print('Error showing database entry: '+str(e))
            raise

    def agent_add_action(self, agent_id, action_id):
        """Add a action to a given agent based on UUID."""
        try:
            index = str(len(self.database['agents'][str(agent_id)]['actions']))
            self.database['agents'][str(agent_id)]['actions'][index] = action_id
            self.database.sync()
        except Exception as e:
            print('Error adding action '+str(action_id)+' to agent_shelf entry '+str(agent_id)+': '+str(e))

    def agent_add_mock_action(self, agent_id, action_string):
        """Use for debugging purposes; Add a string to given agents actions array."""
        try:
            index = str(len(self.database['agents'][str(agent_id)]['actions']))
            self.database['agents'][str(agent_id)]['actions'][index] = str(action_string)
            self.database.sync()
        except Exception as e:
            print('Error adding action '+str(action_string)+' to agent_shelf entry '+str(agent_id)+': '+str(e))

    def agent_change_name(self, agent_id, name):
        """Change the name of a given agent based on UUID."""
        try:
            self.database['agents'][str(agent_id)]['custom_name'] = str(name)
            self.database.sync()
        except Exception as e:
            print('Error changing name of agent_shelf entry '+str(agent_id)+' to '+str(name)+': '+str(e))

    def actions_show_all(self):
        """Return all actions that are existing in the database."""
        try:
            return dict(self.database['actions'])
        except Exception as e:
            print('Error listing all actions: '+str(e))

    def actions_create_new(self, action_object):
        """Create a new action."""
        try:
            index = str(len(self.database['actions']) + 1)
            self.database['actions'][index] = action_object
        except Exception as e:
            print('Error creating new action: '+str(e))
