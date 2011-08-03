class htmlpad {
  $site = 'htmlpad.org'
  $etherpad = 'etherpad.mozilla.org:9000'
  $rootDir = '/var/htmlpad.org'
  $repoDir = "$rootDir/src/htmlpad"
  $python = "$rootDir/bin/python"
  $sitePackagesDir = "$rootDir/lib/python$python_version/site-packages"
  $staticFilesDir = "$rootDir/static"
  $wsgiDir = "$rootDir/wsgi"

  package { 'python-virtualenv':
    ensure => present,
  }

  # The directory structure here avoids using recurse on dirs
  # that will have lots of files installed into them, so that
  # puppet isn't slowed down hashing a bunch of files that it
  # won't need to consult again.

  file { "$rootDir":
    ensure => directory,
  }

  file { "$rootDir/manage.py":
    ensure => file,
    source => "puppet:///modules/htmlpad/htmlpad.org/manage.py",
  }

  file { "$rootDir/wsgi":
    ensure => directory,
    require => File["$rootDir"]
  }
    
  file { "$rootDir/wsgi/htmlpad.wsgi":
    ensure => file,
    source => "puppet:///modules/htmlpad/htmlpad.org/wsgi/htmlpad.wsgi",
    require => File["$rootDir/wsgi"]
  }

  file { "$rootDir/src":
    ensure => directory,
    require => File["$rootDir"]
  }

  file { "$rootDir/src/htmlpad_dot_org":
    ensure => directory,
    recurse => true,
    source => "puppet:///modules/htmlpad/htmlpad.org/src/htmlpad_dot_org",
    require => File["$rootDir/src"]
  }
    
  file { "$rootDir/src/htmlpad_dot_org/settings_local.py":
    content => template("htmlpad/settings_local.py.erb"),
    require => File["$rootDir/src/htmlpad_dot_org"],
  }

  exec { 'htmlpad-virtualenv':
    unless => "/usr/bin/stat $rootDir/bin/python",
    command => "/usr/bin/virtualenv $rootDir",
    require => [ Package['python-virtualenv'], File["$rootDir"] ]
  }

  file { "$sitePackagesDir/htmlpad_dot_org":
    ensure => link,
    target => "$rootDir/src/htmlpad_dot_org",
    require => Exec['htmlpad-virtualenv']
  }

  vcsrepo { "$repoDir":
    ensure => present,
    source => "git://github.com/toolness/htmlpad.git",
    require => File["$rootDir/src"]
  }

  exec { 'install-htmlpad':
    command => "$python setup.py develop",
    cwd => "$repoDir",
    require => [ Exec['htmlpad-virtualenv'], Vcsrepo["$repoDir"] ]
  }

  exec { 'collect-htmlpad-staticfiles':
    command => "$python manage.py collectstatic --noinput",
    cwd => "$rootDir",
    require => [ Exec['install-htmlpad'],
                 File["$rootDir/src/htmlpad_dot_org/settings_local.py"],
                 File["$sitePackagesDir/htmlpad_dot_org"] ]
  }
  
  exec { 'run-htmlpad-tests':
    command => "$python manage.py test",
    cwd => "$rootDir",
    require => Exec['collect-htmlpad-staticfiles']
  }

  apache2::vhost { "$site":
    content => template("htmlpad/apache-site.conf.erb"),
    require => Exec['run-htmlpad-tests']
  }
}
