import os
from datetime import datetime

# Remember when mod_wsgi loaded this file so we can track it.
wsgi_loaded = datetime.now()

wsgidir = os.path.dirname(os.path.abspath(__file__))

# Activate our virtualenv. (Code taken from the virtualenv docs.)
activate_this = os.path.join(wsgidir, '..', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# Tell WSGI where to look for settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'htmlpad_dot_org.settings_local'

import django.conf
import django.core.handlers.wsgi
import django.core.management
import django.utils

# Do validate and activate translations like using `./manage.py runserver`.
# http://blog.dscpl.com.au/2010/03/improved-wsgi-script-for-use-with.html
django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)
utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')
command.validate()

# This is what mod_wsgi runs.
django_app = django.core.handlers.wsgi.WSGIHandler()

def application(env, start_response):
    env['wsgi.loaded'] = wsgi_loaded
    env['datetime'] = str(datetime.now())
    return django_app(env, start_response)

# Uncomment this to figure out what's going on with the mod_wsgi environment.
# def application(env, start_response):
# start_response('200 OK', [('Content-Type', 'text/plain')])
# return '\n'.join('%r: %r' % item for item in sorted(env.items()))