import os
import sys
import platform
import subprocess

REQUIRED_PACKAGES = [
    "git",
    "puppet"
    ]

def ensure(assertion, msg):
    if not assertion:
        print "ERROR: %s" % msg
        sys.exit(1)

def prefer(assertion, msg):
    if not assertion:
        print >> sys.stderr, "WARNING: %s" % msg

def run(cmdline, *args, **kwargs):
    print "Running '%s'..." % ' '.join(cmdline)
    sys.stdout.flush()
    sys.stderr.flush()
    return subprocess.check_call(cmdline, *args, **kwargs)
    
if __name__ == '__main__':
    print "Examining system configuration..."

    ensure(os.geteuid() == 0, 'This script must be run as root.')
    prefer(platform.platform().endswith('-Ubuntu-10.10-maverick'),
           'The platform should be Ubuntu 10.10 (maverick).')
    run(['apt-get', 'install'] + REQUIRED_PACKAGES)
    print "TODO: Need to finish this up."
