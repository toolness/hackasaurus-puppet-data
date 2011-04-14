#!/usr/bin/env python

import os
import sys
import subprocess
import urllib
import urllib2

import MySQLdb

# The number of commits to search back through
NUM = 3

# The maximum number of times you want the tests to be run.
MAX_RUNS = 5

# The name of the job that will be submitted
# (pick a descriptive, but short, name to make it easy to search)

# Note: The string {REV} will be replaced with the current
#       commit number/hash.
JOB_NAME = ('Web X-Ray Goggles Commit <a href="http://github.com/'
            'hackasaurus/webxray/commit/%(rev)s">%(short_rev)s</a>')

# The browsers you wish to run against. Options include:
#  - "all" all available browsers.
#  - "popular" the most popular browser (99%+ of all browsers in use)
#  - "current" the current release of all the major browsers
#  - "gbs" the browsers currently supported in Yahoo's Graded Browser Support
#  - "beta" upcoming alpha/beta of popular browsers
#  - "mobile" the current releases of mobile browsers
#  - "popularbeta" the most popular browser and their upcoming releases
#  - "popularbetamobile" the most popular browser and their upcoming releases 
#    and mobile browsers
BROWSERS = "popularbeta"

SUITE_NAME = "main"
SUITE_URL = "%(relative_url_base)s/%(short_rev)s/test/"

PROJECT_NAME = "webxray"
GIT_REPO = "https://github.com/hackasaurus/webxray.git"

def debug_app(func):
    def wrapper(env, start):
        try:
            return func(env, start)
        except Exception, e:
            import traceback
            tb = traceback.format_exc()
            start('200 OK', [('Content-Type', 'text/plain')])
            return [tb]
    return wrapper

#@debug_app
def application(env, start_response):
    conn = MySQLdb.connect(host=env['swarm_db_host'],
                           user=env['swarm_db_user'],
                           passwd=env['swarm_db_pass'],
                           db=env['swarm_db_name'])

    cursor = conn.cursor()
    cursor.execute("select auth from users where name = %s",
                   (env['swarm_job_user'],))
    auth_token = cursor.fetchone()[0]

    submit_job(base_checkout_dir=env['swarm_checkout_dir'],
               web_root_dir=env['swarm_web_root_dir'],
               user=env['swarm_job_user'],
               auth_token=auth_token,
               host=env['swarm_host'])

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['job submitted']

def build_suites():
    return [os.path.join('test', 'index.html')]

def get_latest_revs(repo_dir, gitcmd='git', num=NUM):
    git = subprocess.Popen(
        [gitcmd, 'log', '-%d' % num, '--reverse',
         "--pretty=format:%H"],
        cwd=repo_dir,
        stdout=subprocess.PIPE
        )
    if git.wait():
        raise Exception('git returned error!')
    return git.stdout.read().split()

def export_tree(repo_dir, rev, export_dir, gitcmd='git', tarcmd='tar'):
    os.mkdir(export_dir)
    git = subprocess.Popen(
        [gitcmd, 'archive', rev],
        cwd=repo_dir,
        stdout=subprocess.PIPE
        )
    subprocess.check_call(
        [tarcmd, '-x', '-C', export_dir],
        stdin=git.stdout
        )

def submit_job(base_checkout_dir, user, auth_token, host, web_root_dir):
    if not base_checkout_dir.startswith(web_root_dir):
        raise AssertionError("base checkout dir should be under web root")
    project_job_dir = os.path.join(base_checkout_dir, PROJECT_NAME)
    relative_url_base = project_job_dir[len(web_root_dir):]
    if os.path.exists(project_job_dir):
        subprocess.check_call(['git', 'pull'], cwd=project_job_dir)
    else:
        subprocess.check_call(['git', 'clone', GIT_REPO, project_job_dir])

    for rev in get_latest_revs(project_job_dir):
        short_rev = rev[:20]
        export_dir = os.path.join(project_job_dir, short_rev)
        if not os.path.exists(export_dir):
            export_tree(project_job_dir, rev, export_dir)
            retval = subprocess.call([sys.executable, 'go.py', 'compile'],
                                     cwd=export_dir)
            if retval != 0:
                # TODO: Shoot, maybe this build is broken. We should keep
                # trying other revisions, though, so don't bail. We might
                # want to log a failure at some point though.
                pass
            args = {
                'state': 'addjob',
                'output': 'dump',
                'user': user,
                'max': str(MAX_RUNS),
                'job_name': JOB_NAME % locals(),
                'browsers': BROWSERS,
                'auth': auth_token,
                'suites[]': SUITE_NAME,
                'urls[]': SUITE_URL % locals()
            }
            req = urllib2.Request("http://127.0.0.1/")
            req.add_header("Host", host)
            f = urllib2.urlopen(req, urllib.urlencode(args))
            f.read()
