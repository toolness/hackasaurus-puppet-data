from fabric.operations import get, put
from fabric.api import task, run, env
from . import secrets

@task
def backup():
    "retrieve an SQL dump of webpad/jsbin data"

    pw = secrets.load_secrets(env['host'])['jsbin_pw']
    run('mysqldump -u jsbin -p%s jsbin > jsbin.sql' % pw)
    get('jsbin.sql', 'jsbin.%(host)s.dump.sql')
    run('rm jsbin.sql')

@task
def restore(filename=None):
    "restore a previous SQL dump of webpad/jsbin data"
    
    if filename is None:
        filename = 'jsbin.%(host)s.dump.sql' % env
    put(filename, 'jsbin.sql')
    pw = secrets.load_secrets(env['host'])['jsbin_pw']
    run('mysql -u jsbin -p%s jsbin < jsbin.sql' % pw)
    run('rm jsbin.sql')
