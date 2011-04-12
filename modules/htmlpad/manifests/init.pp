class htmlpad {
  $site = 'htmlpad.org'
  $etherpad = 'etherpad.mozilla.org:9000'
  $rootDir = '/var/htmlpad.org'
  $repoDir = "$rootDir/htmlpad"
  $python = "$rootDir/bin/python"
  $sitePackagesDir = "$rootDir/lib/python2.6/site-packages"
  $projectDir = "$sitePackagesDir/htmlpad_dot_org"
  $staticFilesDir = "$rootDir/static"
  $wsgiDir = "$rootDir/wsgi"

  package { 'python-virtualenv':
    ensure => present,
  }

  file { "$projectDir":
    ensure => directory,
    recurse => true,
    source => "puppet:///modules/htmlpad/htmlpad_dot_org",
    require => Exec['htmlpad-virtualenv']
  }

  file { "$wsgiDir":
    ensure => directory,
    recurse => true,
    source => "puppet:///modules/htmlpad/wsgi",
    require => Exec['htmlpad-virtualenv']
  }

  file { "$rootDir/manage.py":
    source => "puppet:///modules/htmlpad/manage.py",
    require => Exec['htmlpad-virtualenv']
  }

  file { "$projectDir/settings_local.py":
    content => template("htmlpad/settings_local.py.erb"),
    require => File["$projectDir"],
  }

  exec { 'htmlpad-virtualenv':
    command => "/usr/bin/virtualenv $rootDir",
    require => Package['python-virtualenv'],
  }

  exec { 'install-htmlpad':
    command => "$python setup.py develop",
    cwd => "$repoDir",
    require => [ Exec['htmlpad-virtualenv'], Vcsrepo["$repoDir"] ]
  }

  exec { 'collect-htmlpad-staticfiles':
    command => "$python manage.py collectstatic --noinput",
    cwd => "$rootDir",
    require => [ File["$rootDir/manage.py"], Exec['install-htmlpad'] ]
  }
  
  exec { 'run-htmlpad-tests':
    command => "$python manage.py test",
    cwd => "$rootDir",
    require => [ Exec['collect-htmlpad-staticfiles'] ]
  }

  apache2::vhost { "$site":
    content => template("htmlpad/apache-site.conf.erb")    
  }

  vcsrepo { "$repoDir":
    ensure => present,
    source => "git://github.com/toolness/htmlpad.git"
  }
}
