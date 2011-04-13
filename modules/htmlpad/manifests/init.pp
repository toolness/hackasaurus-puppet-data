class htmlpad {
  $site = 'htmlpad.org'
  $etherpad = 'etherpad.mozilla.org:9000'
  $rootDir = '/var/htmlpad.org'
  $repoDir = "$rootDir/src/htmlpad"
  $python = "$rootDir/bin/python"
  $sitePackagesDir = "$rootDir/lib/python2.6/site-packages"
  $staticFilesDir = "$rootDir/static"
  $wsgiDir = "$rootDir/wsgi"

  package { 'python-virtualenv':
    ensure => present,
  }

  file { "$rootDir":
    ensure => directory,
    recurse => true,
    source => "puppet:///modules/htmlpad/htmlpad.org",
  }

  file { "$rootDir/src/htmlpad_dot_org/settings_local.py":
    content => template("htmlpad/settings_local.py.erb"),
    require => File["$rootDir"],
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
    source => "git://github.com/toolness/htmlpad.git"
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
