import os
import json
from distutils.dir_util import mkpath

ROOT = os.path.abspath(os.path.dirname(__file__))

def path(*x):
    return os.path.join(ROOT, *x)

def load_secrets(host=None):
    secrets = json.load(open(path('..', 'secrets.json')))
    if host is not None:
        host_filename = path('..', 'secrets.%s.json' % host)
        if os.path.exists(host_filename):
            secrets.update(json.load(open(host_filename)))
    return secrets

def _make_manifest_text(secrets):
    lines = ["class secrets {"]
    for name, secret in secrets.items():
        lines.append("  $%s = %s" % (name, repr(str(secret))))
    lines.append("}")
    return "\n".join(lines)

def build_secrets_manifest(host=None):
    dirname = path("..", "modules", "secrets", "manifests")
    filename = os.path.join(dirname, "init.pp")
    mkpath(dirname)
    secrets = load_secrets(host)
    open(filename, 'w').write(_make_manifest_text(secrets))
    print "generated %s" % filename

if __name__ == '__main__':
    build_secrets_manifest()
