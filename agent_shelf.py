#!/usr/bin/python
"""
This module provides high-level wrapper functions for the shelf containing all DashAgents.

It exposes several functions that can be used to return all entries of paired DashAgents and the data assigned to them, as well as
adding and modifying actions assigned to DashAgents.
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
            self.database = shelve.open(database_name)
        except Exception as e:
            print('Error opening shelf: '+str(e))
            raise

    @classmethod
    def close_db(cls):
        """Close the currently open shelve database."""
        try:
            self.database.close()
            return True
        except Exception as e:
            print('Error closing shelf: '+str(e))
            raise

    def store(self, key, value):
        """Use to store a generic value into a given key into the agent shelve database."""
        try:
            self.database[str(key)] = value
            return True
        except Exception as e:
            print('Error writing data '+ str(value) +' to key '+ str(key) +' into shelf: '+str(e))
            raise

    def store_agent(self, device):
        """Handle the data of a recently found DashAgent and add some additional data."""
        try:
            number_of_entries = len(self.database.keys())
            device['uuid'] = (number_of_entries + 1)
            device['custom_name'] = ('Dash Agent '+str(number_of_entries + 1))
            device['actions'] = {}
            self.database[str(device['addr'])] = device
            return True
        except Exception as e:
            print('Error storing agent: '+str(e))
            raise

    def get_agent(self, agent_id):
        """Retrive agent from shelf by UUID."""
        for address, attributes in self.database.items():
            if attributes.get('uuid', -1) == agent_id:
                return self.database[address]

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
            return pprint(self.database[key])
        except Exception as e:
            print('Error showing database entry: '+str(e))
            raise

    def get_address(self, agent_id):
        """Get the 'address' attribute of a given agent."""
        try:
            agent = self.get_agent(agent_id)
            return agent['addr']
        except Exception as e:
            print('Error getting agent attribute: '+str(e))
            raise

    def get_actions(self, agent_id):
        """Get the 'address' attribute of a given agent."""
        try:
            agent = self.get_agent(agent_id)
            return agent['actions']
        except Exception as e:
            print('Error getting agent attribute: '+str(e))
            raise

    def add_action(self, agent_id, action_id):
        """Add a action to a given agent based on UUID."""
        pass

    def change_name(self, agent_id, name):
        """Change the name of a given agent based on UUID."""
        pass
