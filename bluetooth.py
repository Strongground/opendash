#!/usr/bin/python
"""
This module provides high-level wrapper functions for bluepy bluetooth handling of DashAgents.

It exposes several functions that can be used to find nearby devices, pair with them and communicate the status and data of DashAgents to the shelve database.
It also exposes several mock versions of the aforementioned functions that return simulated values relevant to the handling of bluetooth devices in OpenDash.
"""
from __future__ import print_function
from pprint import pprint
from time import sleep
from random import randint
import agent_shelf

shelf_manager = agent_shelf.AgentShelfManager('agent_shelf')

# @TODO:
# This module should expose a function to start the pairing process and return the number of newly found devices.
# The paired devices and actions that are connected with each should be written to a local database (use shelve).
# + First step: Scan with ScanDelegate
# + Then handle discoveries by checking the commonName of each ScanEntry
# + If ScanEntry.commonName is "DashAgent", pair with it:
# + Create peripheral out of the ScanEntry
# + Save the paired peripherals into list and render it into dashboard

# + If user wants to add action to one of the DashAgents, he is required to first create the action,
# then press the button of the DashAgent once to assign it
# + Meaning: Functions should be exposed to listen for UUID of paired DashAgents and assign Actions to them.
# + If in "action assign listening mode" the function should assign action to DashAgent:
# + listen_for_uuid() (generalized, listen and return some signal if paired uuid is received)
# ++ (maybe mock this via bottle request? dashboard/send-uuid?uuid=55:19:0b:64:e9:3f)
# ++ is_paired(uuid):boolean check if given device is paired according to shelve (maybe even by bluepy? look up!)
# ++ if "action assign listening mode" is active:
# ++ otherwise:

#### Bluetooth scanner class
# class ScanDelegate(DefaultDelegate):
#     """Scan class."""
#
#     def __init__(self):
#         """Initialize the bluepy default delegate."""
#         DefaultDelegate.__init__(self)
#
#     @classmethod
#     def handleDiscovery(cls, dev, isNewDev, isNewData):
#         """Handle every found device."""
#         if isNewDev:
#             #print("Discovered device", dev.addr)
#             pass
#         elif isNewData:
#             #print("Received new data from", dev.addr)
#             pass

class MockScanner(object):
    """Mock scanner class."""

    @classmethod
    def scan(cls, duration, number_of_results, number_of_dash_agents):
        """Behave as if scanning for bluetooth devices, returning mock devices.

        Optionally containing DashAgents.
        """
        results = range(0, number_of_results)
        hits = range(0, number_of_dash_agents)
        for i in results:
            results[i] = create_random_bluetooth_device()
        for _ in hits:
            results[randint(0, number_of_dash_agents)] = create_random_bluetooth_device(create_dash_agent=True)
        if duration > 0:
            sleep(duration)
        return results

# def pair_with_agents(device):
#     """Pair with a ScanEntry that has been identified as DashAgent."""
#     if is_dash_agent(device):
#         paired_device = bluepy.Peripheral(deviceAddress = device)
#         return paired_device

#### helper functions
def create_random_bluetooth_device(create_dash_agent=False):
    """Return random device that optionally is a dash agent."""
    if create_dash_agent:
        common_name = "DashAgent"
    else:
        common_name = "RandomDevice"
    return {
        'addr' : str(create_random_mac_address()), # e.g. 08:df:1f:c4:a5:1e
        'addrType' : 'public',
        'iface' : 0,
        'rssi' : get_random_signal_strength(),
        'connectable' : True,
        'updateCount' : 1,
        'commonName' : common_name
    }

def create_random_mac_address():
    """Return a random mac address for test purposes."""
    mac = [randint(0x00, 0x7f), randint(0x00, 0x7f), randint(0x00, 0x7f), randint(0x00, 0x7f), randint(0x00, 0xff), randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def get_random_signal_strength():
    """Return a limited random negative int."""
    ssi = randint(30, 60)* -1
    return ssi

def connect_mock_nearby_agents(time, amount, dash_agents=0):
    """Behave as if scanning for bluetooth devices nearby and return [amount] random mock device results."""
    scanner = MockScanner()
    nearby_devices = scanner.scan(float(time), int(amount), int(dash_agents))
    paired_devices = 0
    for device in nearby_devices:
        # print(' ')
        # print('checking device:')
        # pprint(device)
        if is_dash_agent(device):
            # print('device is a DashAgent! Attempt to pair with it...')
            paired_devices += bool(pair_with_mock_agents(device))
    return paired_devices

def pair_with_mock_agents(device):
    """Behave as if pairing with a found dash agent. Write the device information into shelve."""
    #someobscurepairingcode(device)
    # print('Pairing simulated')
    shelf_manager.store_agent(device)
    # print('DashAgent written to shelve')
    return True

# def getNearbyDevices(time):
#     """Invoke Scanner and scan for devices."""
#     scanner = Scanner().withDelegate(ScanDelegate())
#     nearby_devices = scanner.scan(float(time))
#     return nearby_devices

def is_dash_agent(device):
    """Check if the device has a certain common name."""
    return bool(device['commonName'] == "DashAgent")

## Get nearby devices, one of them a DashAgent, and pair with it
# shelf_manager.show_entry('53:0b:5c:71:9e:82')
# connect_mock_nearby_agents(time=0, amount=5, dash_agents=1)
# shelf_manager.show_content()
