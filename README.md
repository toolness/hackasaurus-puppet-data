This is an attempt to concisely define and document the server configuration for [Hackasaurus][] sites using [Puppet Best Practices][].

Deployment is assumed to target a bare Ubuntu natty server (11.04). All other dependencies are automatically installed by the various configuration files in this repository.

## Prerequisites ##

You'll need [Fabric][].

In order to deploy and test, you'll also need to set up `ssh` such that
it's possible to access the remote server as root, e.g. by setting up
a public key. (Unfortunately, the deploy and test commands don't currently
delegate to Fabric/paramiko for this.)

## Usage ##

To deploy Hackasaurus applications to a remote server, run:

    fab -H yourserver.org deploy
    
To run integration tests on a remote server, run:

    fab -H yourserver.org test

Run `fab -l` for more commands, and `fab -d <command>` for detailed help
on a particular command.

## Secrets ##

All passwords and other secrets for Hackasaurus applications are stored in 
`secrets.json`. Feel free to change this as necessary.

## Local Configuration ##

Virtual hosting configurations are used for the domains of Hackasaurus sites. To make development and testing easy, each site can also be accessed at its normal domain suffixed with .dev.

For example, if you want to access htmlpad.org on your development server, you can add an entry for htmlpad.org.dev to your `/etc/hosts` file.

  [Fabric]: http://fabfile.org
  [Hackasaurus]: http://hackasaurus.org
  [Puppet Best Practices]: http://projects.puppetlabs.com/projects/puppet/wiki/Puppet_Best_Practice
