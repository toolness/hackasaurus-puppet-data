from StringIO import StringIO

from fabric.api import *
from fabric.contrib.files import exists
from secrets import load_secrets

PROJ_ROOT = '/var/hackpub.hackasaurus.org'
REPO_URL = "git://github.com/hackasaurus/hackpub.git"

LOCAL_SETTINGS = """\
from settings import *

AWS_ACCESS_KEY_ID = '%(hackpub_aws_access_key_id)s'
AWS_SECRET_ACCESS_KEY = '%(hackpub_aws_secret_access_key)s'

BUCKET_NAME = '%(hackpub_bucket_name)s'
PUBLISH_DOMAIN = '%(hackpub_publish_domain)s'
"""

def run_manage_cmd(cmd):
    with cd(PROJ_ROOT):
        run('python manage.py %s' % cmd)

@task
def deploy():
    if exists(PROJ_ROOT):
        update()
    else:
        clone()
    settings = StringIO(LOCAL_SETTINGS % load_secrets(env['host']))
    put(settings, '%s/settings_local.py' % PROJ_ROOT)
    run_manage_cmd('test')
    run('touch %s/wsgi/hackpub.wsgi' % PROJ_ROOT)

@task
def update():
    with cd(PROJ_ROOT):
        run('git pull')

@task
def clone():
    run('git clone %s %s' % (REPO_URL, PROJ_ROOT))
