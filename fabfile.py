import os
import sys
import json

from fabric.utils import abort
from fabric.api import task, run, env, local
from fabric.operations import get, put

ROOT = os.path.abspath(os.path.dirname(__file__))

def path(*x):
    return os.path.join(ROOT, *x)

sys.path.insert(0, path('tools'))

import deploy as deployment
import test as testing

secrets = json.load(open(path('secrets.json')))

@task
def deploy():
    "deploy the entire Hackasaurus server"

    if env['host'] is None:
        abort('please specify a host.')
    deployment.deploy(env['host'])

@task
def test(run=None):
    """
    test the Hackasaurus server

    Examples:
    
      fab -H baz.org test                  run all tests on baz.org.
      fab -H baz.org test:MyTestSuite      run suite 'MyTestSuite'.
      fab -H baz.org test:MyTest.testFoo   run MyTest.testFoo.
    """

    if env['host'] is None:
        abort('please specify a host.')
    argv = [sys.argv[0], '--verbose', env['host']]
    if run is not None:
        argv.append(run)
    testing.TestProgram(argv=argv, module=testing)

@task
def jsbin_backup():
    "retrieve an SQL dump of webpad/jsbin data"

    run('mysqldump -u jsbin -p%(jsbin_pw)s jsbin > jsbin.sql' % secrets)
    get('jsbin.sql', 'jsbin.%(host)s.dump.sql')
    run('rm jsbin.sql')

@task
def jsbin_restore(filename=None):
    "restore a previous SQL dump of webpad/jsbin data"
    
    if filename is None:
        filename = 'jsbin.%(host)s.dump.sql' % env
    put(filename, 'jsbin.sql')
    run('mysql -u jsbin -p%(jsbin_pw)s jsbin < jsbin.sql' % secrets)
    run('rm jsbin.sql')
