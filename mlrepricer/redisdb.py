"""Handling the redis database."""

import os
import subprocess


def server_start():
    """Start the redis server."""
    # this environment should have access to the redis configfile
    subprocess.Popen(["redis-server"], stdout=open(os.devnull, "w"),
                     stderr=subprocess.STDOUT)
