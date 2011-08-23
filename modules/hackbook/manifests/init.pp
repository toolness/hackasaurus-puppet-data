class hackbook {
  $site = 'hackbook.hackasaurus.org'
  $rootDir = '/var/hackbook'
  $wsgiDir = "$rootDir/wsgi-scripts"
  $staticFilesDir = "$rootDir/build"

  apache2::vhost { "$site":
    content => template("hackbook/apache-site.conf.erb"),
    require => Exec["update-$site"]
  }

  vcsrepo { "$rootDir":
    ensure => present,
    source => "git://github.com/hackasaurus/hackbook.git"
  }

  file { "$rootDir":
    require => Vcsrepo["$rootDir"],
    recurse => true,
    owner => 'www-data',
    group => 'www-data'
  }
  
  exec { "update-$site":
    command => "/usr/bin/curl --header \"Host: $site\" http://127.0.0.1/wsgi/update-site",
    require => [File["$rootDir"], Vcsrepo["$rootDir"]]
  }
}
