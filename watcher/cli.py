"""
watcher

Usage:
  watcher run --config-yml=<config-yml>

Options:
  --config-yml=<config-yml>      Path to file with watcher configs.
"""
import io
from docopt import docopt

import yaml

from watcher import __version__
from watcher import watcher


def main():
    args = docopt(__doc__, version=__version__)

    if args["run"]:
        config_file = args["--config-yml"]

        watcher.run(config_file)

