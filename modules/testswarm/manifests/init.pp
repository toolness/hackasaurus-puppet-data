class testswarm {
  include mysql
  include apache2

  $site = "swarm.hksr.us"
  $rootDir = "/var/$site"
  $db = "testswarm"
  $user = $db
  $pw = "change_me"

  package { 'curl':
    ensure => present
  }

  package { 'libapache2-mod-php5':
    ensure => present,
    notify => Service['apache2']
  }

  package { 'php5-mysql':
    ensure => present,
  }

  mysql::db { "$db":
    user => $user,
    password => $pw
  }
  
  vcsrepo { "$rootDir":
    ensure => "present",
    source => "https://github.com/jquery/testswarm.git"
  }
  
  exec { "install-testswarm-schema":
    unless => "/usr/bin/mysql $db -u$user -p$pw -e \"SELECT COUNT(*) FROM clients\"",
    command => "/bin/cat $rootDir/config/testswarm.sql $rootDir/config/useragents.sql | /usr/bin/mysql $db -u$user -p$pw",
    require => [ Mysql::Db["$db"], Vcsrepo["$rootDir"] ]
  }

  file { "$rootDir/config.ini":
    content => template("testswarm/config.ini.erb")
  }
  
  file { "$apache2::apacheDir/mods-enabled/rewrite.load":
    ensure => link,
    target => "../mods-available/rewrite.load",
    notify => Service['apache2']
  }

  apache2::vhost { "$site":
    content => template("testswarm/apache-site.conf.erb"),
  }
  
  cron { "testswarm-wipe":
    command => "/usr/bin/curl -s --header \"Host: $site\" http://127.0.0.1/?state=wipe > /dev/null",
    user => "www-data",
    require => Package['curl']
  }
  
  define swarmuser( $password, $email, $request ) {
    include testswarm
    
    exec { "add-testswarm-user-$name":
      command => "/usr/bin/curl --header \"Host: $testswarm::site\" -d \"username=$name&password=$password&email=$email&request=$request\" http://127.0.0.1/signup/",
      require => Package['curl']
    }
  }

  swarmuser { 'hackasaurus':
    password => 'change_me',
    email => 'change_me@changeme.com',
    request => 'account-for-hackasaurus-projects'
  }
}
