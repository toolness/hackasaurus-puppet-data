import sys
import os
import imp

from fabric.context_managers import cd
from fabric.utils import abort
from fabric.api import task, env
from fabric.operations import run, put
from fabric.contrib.project import upload_project

from . import testing, jsbin, secrets

ROOT = os.path.abspath(os.path.dirname(__file__))

def path(*x):
    return os.path.join(ROOT, *x)

def import_fabfile(pathname):
    fabfilename = os.path.join(pathname, 'fabfile.py')
    fabfile = open(fabfilename)
    desc = ('.py', 'r', imp.PY_SOURCE)
    modname = os.path.basename(pathname)
    module = imp.load_module(modname, fabfile, fabfilename, desc)
    fabfile.close()
    return module

htmlpad = import_fabfile(path('..', 'htmlpad'))

@task
def configure():
    "configure the Hackasaurus server"

    secrets.build_secrets_manifest(env['host'])
    run('rm -rf /root/deployment')
    run('mkdir /root/deployment')
    with cd('/root/deployment'):
        upload_project(path('..', 'manifests'))
        upload_project(path('..', 'modules'))
        put(path('run-on-server', 'bootstrap.py'), '.')
        run('python bootstrap.py')

@task
def deploy():
    "deploy the entire Hackasaurus server and all its apps"

    configure()
    htmlpad.deploy()

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

    result = testing.run_tests(defaultTest=run, verbosity=2)
    if not result.wasSuccessful():
        abort('some tests failed on %s.' % env['host'])
