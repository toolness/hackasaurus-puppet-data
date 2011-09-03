class htmlpad {
  $site = 'htmlpad.org'
  $rootDir = '/var/htmlpad.org'
  $staticFilesDir = "$rootDir/collected-static"
  $wsgiDir = "$rootDir/wsgi"

  apache2::vhost { "$site":
    content => template("htmlpad/apache-site.conf.erb")
  }
}
