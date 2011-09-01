import os
import sys
import json
from distutils.dir_util import mkpath

MY_DIR = os.path.abspath(os.path.dirname(__file__))

def _make_manifest_text(secrets):
    lines = ["class secrets {"]
    for name, secret in secrets.items():
        lines.append("  $%s = %s" % (name, repr(str(secret))))
    lines.append("}")
    return "\n".join(lines)

def build_secrets_manifest():
    json_filename = os.path.join(MY_DIR, "..", "secrets.json")
    if not os.path.exists(json_filename):
        print "secrets.json not found! please copy secrets.sample.json to "
        print "secrets.json and modify it as necessary."
        sys.exit(1)
    f = open(json_filename, 'r')
    secrets = json.load(f)
    dirname = os.path.join(MY_DIR, "..", "modules", "secrets", "manifests")
    filename = os.path.join(dirname, "init.pp")
    mkpath(dirname)
    open(filename, 'w').write(_make_manifest_text(secrets))
    print "generated %s" % filename

if __name__ == '__main__':
    build_secrets_manifest()
