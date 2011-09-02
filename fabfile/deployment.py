#!/usr/bin/env python

import os
import sys
import subprocess

from . import secrets

MY_DIR = os.path.dirname(__file__)

def deploy(server):
    secrets.build_secrets_manifest()

    # We're going to have to use tar here instead of git archive,
    # as git archive doesn't deal with submodules and the
    # third-party git-archive-all.sh script doesn't seem to
    # support OS X.
    tarfile = subprocess.Popen(
        ['tar', 'zcv', '--exclude', '.git*', '.'],
        cwd=os.path.join(MY_DIR, '..'),
        stdout=subprocess.PIPE
        )

    ssh_args = ['ssh', 'root@%s' % server]
    subprocess.check_call(ssh_args +  ['cat > payload.tgz'],
                          stdin=tarfile.stdout)
    remote_cmds = [
        'rm -rf /var/hackasaurus-puppet-data',
        'rm -rf /root/hackasaurus-puppet-data',
        'mkdir /root/hackasaurus-puppet-data',
        'cd /root/hackasaurus-puppet-data',
        'tar -xvf /root/payload.tgz',
        'rm /root/payload.tgz',
        '/bin/chown root.root /root/hackasaurus-puppet-data',
        '/bin/chmod 0700 /root/hackasaurus-puppet-data',
        'cd /root',
        'mv hackasaurus-puppet-data /var',
        'cd /var/hackasaurus-puppet-data',
        'python fabfile/setup_server.py'
        ]
    result = subprocess.call(ssh_args + [';'.join(remote_cmds)])
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s <server-name>" % sys.argv[0]
        sys.exit(1)
    server = sys.argv[1]

    if deploy(server) != 0:
        print "Deployment failed."
        sys.exit(1)
