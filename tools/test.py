#!/usr/bin/env python

import types
import sys
import os
import unittest
import urllib2
import urlparse

server = None

def vhostreq(url):
    parts = urlparse.urlparse(url)
    newurl = urlparse.urlunparse((parts.scheme,
                                  server,
                                  parts.path,
                                  parts.params,
                                  parts.query,
                                  parts.fragment))
    req = urllib2.Request(newurl)
    req.add_header('Host', parts.netloc)
    try:
        return urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        return e

class HtmlpadTests(unittest.TestCase):
    def testHomePageIsAccessible(self):
        f = vhostreq('http://htmlpad.org/')
        self.assertTrue('Welcome to htmlpad.org' in f.read())

    def testStaticFilesDirIsAccessible(self):
        f = vhostreq('http://htmlpad.org/static-files/jquery.js')
        self.assertTrue('John Resig' in f.read())

class HackasaurusTests(unittest.TestCase):
    def testHomePageIsAccessible(self):
        f = vhostreq('http://hackasaurus.org/')
        self.assertTrue('Hackasaurus' in f.read())

    def testWSGIDirIsAccessible(self):
        e = vhostreq('http://hackasaurus.org/wsgi/recruit-me')
        self.assertEqual(e.code, 405)

class TestProgram:
    """A command-line program that runs a set of tests. Taken
    from unittest and modified.
    """
    USAGE = """\
Usage: %(progName)s [options] <server> [test] [...]

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output

Examples:
  %(progName)s srv                              - run default set of tests
  %(progName)s srv MyTestSuite                   - run suite 'MyTestSuite'
  %(progName)s srv MyTestCase.testSomething      - run MyTestCase.testSomething
  %(progName)s srv MyTestCase                    - run all 'test*' test methods
                                               in MyTestCase
"""
    def __init__(self, module='__main__', defaultTest=None,
                 argv=None, testRunner=unittest.TextTestRunner,
                 testLoader=unittest.defaultTestLoader):
        if type(module) == type(''):
            self.module = __import__(module)
            for part in module.split('.')[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.verbosity = 1
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.progName = os.path.basename(argv[0])
        self.parseArgs(argv)
        self.runTests()

    def usageExit(self, msg=None):
        if msg: print msg
        print self.USAGE % self.__dict__
        sys.exit(2)

    def parseArgs(self, argv):
        global server
        import getopt
        try:
            options, args = getopt.getopt(argv[1:], 'hHvq',
                                          ['help','verbose','quiet'])
            for opt, value in options:
                if opt in ('-h','-H','--help'):
                    self.usageExit()
                if opt in ('-q','--quiet'):
                    self.verbosity = 0
                if opt in ('-v','--verbose'):
                    self.verbosity = 2
            if len(args) == 0:
                raise getopt.error("You must provide a server name.")
            server = args[0]
            args = args[1:]
            if len(args) == 0 and self.defaultTest is None:
                self.test = self.testLoader.loadTestsFromModule(self.module)
                return
            if len(args) > 0:
                self.testNames = args
            else:
                self.testNames = (self.defaultTest,)
            self.createTests()
        except getopt.error, msg:
            self.usageExit(msg)

    def createTests(self):
        self.test = self.testLoader.loadTestsFromNames(self.testNames,
                                                       self.module)

    def runTests(self):
        if isinstance(self.testRunner, (type, types.ClassType)):
            try:
                testRunner = self.testRunner(verbosity=self.verbosity)
            except TypeError:
                # didn't accept the verbosity argument
                testRunner = self.testRunner()
        else:
            # it is assumed to be a TestRunner instance
            testRunner = self.testRunner
        result = testRunner.run(self.test)
        sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    TestProgram()
