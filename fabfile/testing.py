#!/usr/bin/env python

import types
import sys
import os
import unittest
import urllib2
import urlparse
import json

from fabric.api import env
from fabric.operations import run
from fabric.context_managers import hide
from secrets import load_secrets

def vhostreq(url):
    parts = urlparse.urlparse(url)
    newurl = urlparse.urlunparse((parts.scheme,
                                  env['host'],
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

def try_mysql_login(username, secret_name, db):
    pw = load_secrets(env['host'])[secret_name]
    cmd = 'mysql -u %s -p%s -D %s -e "show tables;"' % (username, pw, db)
    with hide('running', 'stdout'):
        run(cmd)

class HackpubTests(unittest.TestCase):
    def testMetadata404Works(self):
        e = vhostreq('http://hackpub.hackasaurus.org/metadata/nonexistent')
        self.assertEqual(e.headers['Access-Control-Allow-Methods'],
                         "OPTIONS, GET, POST")
        self.assertEqual(e.read(), 'not found: /metadata/nonexistent')
        self.assertEqual(e.code, 404)

class TestswarmTests(unittest.TestCase):
    def testDatabaseLoginWorks(self):
        try_mysql_login('testswarm', 'testswarm_pw', 'testswarm')

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
        try_mysql_login('root', 'mysql_root_pw', 'mysql')

class JsbinTests(unittest.TestCase):
    def testDatabaseLoginWorks(self):
        try_mysql_login('jsbin', 'jsbin_pw', 'jsbin')

    def testRootIsAccessible(self):
        e = vhostreq('http://webpad.hackasaurus.org/')
        self.assertEqual(e.code, 200)
        
    def testRewriteRulesWork(self):
        e = vhostreq('http://webpad.hackasaurus.org/js/debug/jsbin.js')
        self.assertEqual(e.code, 200)

def run_tests(defaultTest=None, verbosity=1,
              testRunner=unittest.TextTestRunner,
              testLoader=unittest.defaultTestLoader):
    me = sys.modules[__name__]
    if defaultTest is None:
        test = testLoader.loadTestsFromModule(me)
    else:
        testNames = (defaultTest,)
        test = testLoader.loadTestsFromNames(testNames, me)

    return testRunner(verbosity=verbosity).run(test)
