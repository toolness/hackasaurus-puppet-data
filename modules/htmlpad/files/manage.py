#!/usr/bin/env python

import os

try:
    import htmlpad_dot_org
except ImportError:
    # Activate our virtualenv. (Code taken from the virtualenv docs.)
    root = os.path.dirname(os.path.abspath(__file__))
    activate_this = os.path.join(root, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

from django.core.management import execute_manager

import htmlpad_dot_org.settings_local as settings

if __name__ == "__main__":
    execute_manager(settings)
