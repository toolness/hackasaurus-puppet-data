#!/usr/bin/env python

import os
import sys
import subprocess

SSH_CMD = 'ssh'

MY_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s <server-name>" % sys.argv[0]
        sys.exit(1)
    server = sys.argv[1]
    subprocess.check_call(
        ['scp', 'setup_server.py', 'root@%s:' % server],
        cwd=MY_DIR
    )
    subprocess.check_call(
        ['ssh', 'root@%s' % server, "python setup_server.py"]
    )
