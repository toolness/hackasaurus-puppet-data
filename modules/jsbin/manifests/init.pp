class jsbin {
  $site = "webpad.hackasaurus.org"
  $rootDir = "/var/$site"
  $wwwDir = "$rootDir/www"
  $db = "jsbin"
  $user = $db
  $pw = "change_me"

  include mysql
  include apache2

  mysql::db { "$db":
    user => $user,
    password => $pw
  }

  vcsrepo { "$wwwDir":
    ensure => "present",
    source => "https://toolness@github.com/hackasaurus/jsbin.git",
    require => File["$rootDir"]
  }

  exec { "install-jsbin-schema":
    command => "/bin/cat $wwwDir/build/jsbin.sql | /usr/bin/mysql $db -u$user -p$pw",
    require => [ Mysql::Db["$db"], Vcsrepo["$wwwDir"] ]
  }

  file { "$wwwDir/config.php":
    content => template("jsbin/config.php.erb"),
    require => Vcsrepo["$wwwDir"]
  }

  apache2::vhost { "$site":
    content => template("jsbin/apache-site.conf.erb"),
  }

  file { "$rootDir":
    ensure => directory,
    require => [ Package['php5-mysql'],
                 File["$apache2::apacheDir/mods-enabled/rewrite.load"] ]
  }
}

