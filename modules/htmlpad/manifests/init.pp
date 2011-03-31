class htmlpad {
  $site = 'htmlpad.org'
  $etherpad = 'etherpad.mozilla.org:9000'
  $rootDir = '/var/htmlpad'
  $apacheDir = '/etc/apache2'
  $wsgiDir = "$rootDir/wsgi-scripts"
  $staticFilesDir = "$rootDir/static-files"

  package { 'libapache2-mod-wsgi':
    ensure => present,
    before => File["$apacheDir/sites-available/$site"],
  }

  service { 'apache2':
    ensure => running,
    enable => true,
    hasrestart => true,
    hasstatus => true,
  }

  file { "$apacheDir/sites-available/$site":
    ensure => file,
    owner => 'root',
    group => 'root',
    content => template("htmlpad/apache-site.conf.erb"),
    notify => Service['apache2'],
  }

  file { "$apacheDir/sites-enabled/001-$site":
    ensure => link,
    target => "$apacheDir/sites-available/$site"
  }
  
  vcsrepo { "$rootDir":
    ensure => present,
    source => "git://github.com/toolness/htmlpad.git"
  }
}
