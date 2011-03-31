This is an attempt to concisely define and document the server configuration for [Hackasaurus][] sites using [Puppet Best Practices][].

Deployment is assumed to target a bare Ubuntu maverick server (10.10). All other dependencies are automatically installed by the various configuration files in this repository.

If your SSH key can be used to access the remote server as root, then you can run `tools/deploy.py` to deploy Hackasaurus applications to the remote server.

## Local Configuration ##

Virtual hosting configurations are used for the domains of Hackasaurus sites. To make development and testing easy, each site can also be accessed at its normal domain suffixed with .dev.

For example, if you want to access htmlpad.org on your development server, you can add an entry for htmlpad.org.dev to your `/etc/hosts` file.

  [Hackasaurus]: http://hackasaurus.org
  [Puppet Best Practices]: http://projects.puppetlabs.com/projects/puppet/wiki/Puppet_Best_Practice
