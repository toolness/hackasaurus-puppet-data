#!/usr/bin/env python

import sys
import time
import subprocess

# TODO: This violates DRY, as it's duplicated in the
# puppet manifest.
RECRUITMENT_FORM_DIR = '/var/hackasaurus.org/recruitment-forms'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s <server-name>" % sys.argv[0]
        sys.exit(1)
    server = sys.argv[1]

    backup_filename = time.strftime('recruitment-forms-%Y-%m-%d.tgz')
    backup_file = open(backup_filename, 'wb')
    ssh_args = ['ssh', 'root@%s' % server]

    subprocess.check_call(
        ssh_args +  ['tar -zcv %s' % RECRUITMENT_FORM_DIR],
        stdout=backup_file
        )

    backup_file.close()

    print "Created %s." % backup_filename
