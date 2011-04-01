class hackasaurus {
  $site = 'hackasaurus.org'
  $rootDir = '/var/hackasaurus.org'
  $wsgiDir = "$rootDir/wsgi-scripts"
  $staticFilesDir = "$rootDir/static-files"
  $recruitmentFormsDir = "$rootDir/recruitment-forms"

  apache2::vhost { "$site":
    content => template("hackasaurus/apache-site.conf.erb")
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
