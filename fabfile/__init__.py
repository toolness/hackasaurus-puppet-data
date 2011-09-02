import sys

from fabric.utils import abort
from fabric.api import task, env

from . import deployment, testing, jsbin

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
