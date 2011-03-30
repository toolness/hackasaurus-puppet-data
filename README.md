This is an attempt to concisely define and document the server configuration for [Hackasaurus][] sites using [Puppet Best Practices][].

The Puppet files in this repository assume a bare Ubuntu maverick server (10.10) that has Git and Puppet installed.

If these prerequisites are satisfied, and if your SSH key can be used to access the remote server as root, then you can run `tools/deploy.py` to deploy Hackasaurus applications to the remote server.

## Local Configuration ##

Currently, a virtual hosting configuration is used for the htmlpad.org domain.
You may need to edit your local `/etc/hosts` file accordingly.

  [Hackasaurus]: http://hackasaurus.org
  [Puppet Best Practices]: http://projects.puppetlabs.com/projects/puppet/wiki/Puppet_Best_Practice
