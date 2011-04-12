class htmlpad {
  $site = 'htmlpad.org'
  $etherpad = 'etherpad.mozilla.org:9000'
  $rootDir = '/var/htmlpad.org'
  $repoDir = "$rootDir/htmlpad"
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
  }

  file { "$rootDir/manage.py":
    source => "puppet:///modules/htmlpad/manage.py"
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
    command => "$rootDir/bin/python setup.py develop",
    cwd => "$repoDir",
    require => [ Exec['htmlpad-virtualenv'], Vcsrepo["$repoDir"] ]
  }

  exec { 'collect-staticfiles':
    command => "$rootDir/bin/python $rootDir/manage.py collectstatic --noinput",
    require => [ File["$rootDir/manage.py"], Exec['install-htmlpad'] ]
  }

  apache2::vhost { "$site":
    content => template("htmlpad/apache-site.conf.erb")    
  }

  vcsrepo { "$repoDir":
    ensure => present,
    source => "git://github.com/toolness/htmlpad.git"
  }
}
