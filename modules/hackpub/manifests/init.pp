class hackpub {
  $site = 'hackpub.hackasaurus.org'
  $rootDir = '/var/hackpub.hackasaurus.org'
  $wsgiDir = "$rootDir/wsgi"

  apache2::vhost { "$site":
    content => template("hackpub/apache-site.conf.erb")
  }
}
