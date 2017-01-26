"""OpenDash Control Center server. Per deafult it automatically makes itself available via http on port 8585. Per default it also triggers at least one bluetooth device search.

Most importantly, it serves the ControlCenter application and
web GUI to configure it. Without further configuration it will
do nothing!
It also does some initialization, checks and already searches for
bluetooth devices in the area and temporarily adds them to the
internal database to allow the user to later name and accept them.
It also allows to run only some of the contained functions
via parametrization:

-v : Enable verbose mode
-s : Trigger initial search for DashAgents on startup. Note: This search can be
triggered again by the web GUI.
-o : Create new database regardless of a existing one.
-D : Start development server on localhost:8585
"""

from __future__ import print_function
# from pprint import pprint
import argparse
import controlcenter
from bottle import run

def start():
    """The main function to start the OpenDash server."""
    ## Define CLI arguments
    parser = argparse.ArgumentParser(description='OpenDash Control Center server. Per default it automatically makes itself available via http on port 8585. Per default it also triggers at least one bluetooth device search.')
    parser.add_argument('-v', '--verbose',  action='store_true', dest='verbose',  help='start with verbose mode enabled')
    parser.add_argument('-s', '--scan',     action='store_true', dest='scan',     help='enable initial scan for bluetooth devices on startup')
    parser.add_argument('-o', '--override', action='store_true', dest='override', help='ignore existing database and create new one. IMPORTANT! This will overwrite existing databases of the same name!')
    parser.add_argument('-D', '--Debug',    action='store_true', dest='debug',    help='start control center in development mode. This does expose the server on port 8585 and enables debug printouts in the code as well as mockup environments for certain classes and modules. See README for details.')
    args = parser.parse_args()
    control_center = controlcenter.ControlCenter(debug_mode=args.debug, verbose=args.verbose, force_shelf_creation=args.override, scan_mode=args.scan)

    if args.debug:
        #### Start development server
        debug()
        run(host='localhost', port=8585)
    else:
        #### Start test production server
        run(host='0.0.0.0', port=80)

start()
