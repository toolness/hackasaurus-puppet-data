class hackasaurus {
  $site = 'hackasaurus.org'
  $rootDir = '/var/hackasaurus.org'
  $staticFilesDir = "$rootDir"

  apache2::vhost { "$site":
    content => template("hackasaurus/apache-site.conf.erb")
  }
}
