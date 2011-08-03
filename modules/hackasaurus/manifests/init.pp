class hackasaurus {
  $site = 'hackasaurus.org'
  $rootDir = '/var/hackasaurus.org'
  $staticFilesDir = "$rootDir/static-files"

  apache2::vhost { "$site":
    content => template("hackasaurus/apache-site.conf.erb")
  }

  vcsrepo { "$rootDir":
    ensure => present,
    source => "git://github.com/hackasaurus/hackasaurus.org.git"
  }

  file { "$rootDir":
    require => Vcsrepo["$rootDir"],
    recurse => true,
    owner => 'www-data',
    group => 'www-data'
  }
}
