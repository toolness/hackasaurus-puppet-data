#!/usr/bin/env python

import types
import sys
import os
import unittest
import urllib2
import urlparse
import json
import subprocess

from secrets import load_secrets

server = None
secrets = None

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

def try_mysql_login(username, pw, db):
    cmd = 'mysql -u %s -p%s -D %s -e "show tables;"' % (username, pw, db)
    ssh_args = ['ssh', 'root@%s' % server, cmd]
    popen = subprocess.Popen(ssh_args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    out, err = popen.communicate()
    if popen.returncode:
        raise Exception(out)

class TestswarmTests(unittest.TestCase):
    def testDatabaseLoginWorks(self):
        try_mysql_login('testswarm', secrets['testswarm_pw'], 'testswarm')

    def testHomePageIsAccessible(self):
        f = vhostreq('http://swarm.hksr.us/')
        self.assertTrue('Welcome to the TestSwarm' in f.read())

    def testSubmitJobWorks(self):
        f = vhostreq('http://swarm.hksr.us/wsgi/submit_webxray_job.wsgi')
        self.assertEqual(f.read(), "job submitted")

class HtmlpadTests(unittest.TestCase):
    def testHomePageIsAccessible(self):
        f = vhostreq('http://htmlpad.org/')
        self.assertTrue('Welcome to htmlpad.org' in f.read())

    def testStaticFilesDirIsAccessible(self):
        f = vhostreq('http://htmlpad.org/static/js/jquery.min.js')
        self.assertTrue('John Resig' in f.read())

class HackbookTests(unittest.TestCase):
    def testUpdateWorks(self):
        f = vhostreq('http://hackbook.hackasaurus.org/wsgi/update-site')
        for retval in json.loads(f.read()):
            self.assertEqual(retval, 0)
        self.assertEqual(f.code, 200)

    def testHomePageIsAccessible(self):
        f = vhostreq('http://hackbook.hackasaurus.org/')
        self.assertTrue('Hackbook' in f.read())

class HackasaurusTests(unittest.TestCase):
    def testUpdateWorks(self):
        f = vhostreq('http://hackasaurus.org/wsgi/update-site')
        for retval in json.loads(f.read()):
            self.assertEqual(retval, 0)
        self.assertEqual(f.code, 200)

    def testHomePageIsAccessible(self):
        f = vhostreq('http://hackasaurus.org/')
        self.assertTrue('Hackasaurus' in f.read())

    def testRedirectsWork(self):
        e = vhostreq('http://hackasaurus.org/news/')
        self.assertEqual(e.code, 200)
        self.assertEqual(e.geturl(), "http://hackasaurus.org/blog/")

class MysqlTests(unittest.TestCase):
    def testRootLoginWorks(self):
        try_mysql_login('root', secrets['mysql_root_pw'], 'mysql')

class JsbinTests(unittest.TestCase):
    def testDatabaseLoginWorks(self):
        try_mysql_login('jsbin', secrets['jsbin_pw'], 'jsbin')

    def testRootIsAccessible(self):
        e = vhostreq('http://webpad.hackasaurus.org/')
        self.assertEqual(e.code, 200)
        
    def testRewriteRulesWork(self):
        e = vhostreq('http://webpad.hackasaurus.org/js/debug/jsbin.js')
        self.assertEqual(e.code, 200)

class TestProgram:
    def __init__(self, host, module, defaultTest=None,
                 verbosity=1,
                 testRunner=unittest.TextTestRunner,
                 testLoader=unittest.defaultTestLoader):
        global server
        global secrets

        server = host
        secrets = load_secrets(host)

        self.module = module
        self.verbosity = verbosity
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader

        if self.defaultTest is None:
            self.test = self.testLoader.loadTestsFromModule(self.module)
        else:
            self.testNames = (self.defaultTest,)
            self.test = self.testLoader.loadTestsFromNames(self.testNames,
                                                           self.module)

        self.runTests()

    def runTests(self):
        testRunner = self.testRunner(verbosity=self.verbosity)
        self.result = testRunner.run(self.test)
