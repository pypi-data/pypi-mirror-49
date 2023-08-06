from argparse import ArgumentParser
import json

from . import *
from . import _load_server_config

parser = ArgumentParser(description='Server-side of error_report library.')
parser.add_argument('--hostname', type=str, default="",
                    help='hostname to open the port on')
parser.add_argument('--port', type=int, default=1234,
                    help='port number to open (default = 1234)')
parser.add_argument('-k','--keys', nargs='*', default = [],
                    help='Keys into the report dictionaries; corresponding '
                         'values will be used as directory names to organize '
                         'reports.')
parser.add_argument('-s', '--save_config', action="store_true",
                    help="Save options provided on command line to "
                         "~/.pyerrorreport/config.json, becoming the new "
                         "default.")

args = parser.parse_args()
argdict = args.__dict__.copy()

del argdict['save_config']

config = _load_server_config()

# This is redundant with the logic inside start_server, but we need it to
# show the right hostname and port when we print the "starting server" message
if config:
    config.update(argdict)
    print("Config loaded from ~/.pyerrorreport/config.json")

if args.save_config:
    from . import _default_config_path
    _default_config_path.parent.mkdir(parents=True, exist_ok=True)
    _default_config_path.write_text(json.dumps(config))


print(f"Starting server on {config['hostname'] or '*'}:{config['port']}")
start_server(**config)
