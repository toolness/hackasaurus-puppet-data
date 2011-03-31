class hackasaurus {
  $site = 'hackasaurus.org'
  $rootDir = '/var/hackasaurus.org'
  $apacheDir = '/etc/apache2'
  $wsgiDir = "$rootDir/wsgi-scripts"
  $staticFilesDir = "$rootDir/static-files"
  $recruitmentFormsDir = "$rootDir/recruitment-forms"

  file { "$apacheDir/sites-available/$site":
    ensure => file,
    owner => 'root',
    group => 'root',
    content => template("hackasaurus/apache-site.conf.erb"),
    notify => Service['apache2'],
  }

  file { "$apacheDir/sites-enabled/001-$site":
    ensure => link,
    target => "$apacheDir/sites-available/$site",
    notify => Service['apache2'],
  }
  
  vcsrepo { "$rootDir":
    ensure => present,
    source => "git://github.com/hackasaurus/hackasaurus.org.git"
  }

  file { "$recruitmentFormsDir":
    ensure => directory,
    owner => 'www-data',
    group => 'www-data',
    require => Vcsrepo["$rootDir"],
  }
}
