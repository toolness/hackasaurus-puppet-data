class webxray {
  $site = 'webxray.hackasaurus.org'
  $rootDir = '/var/webxray.hackasaurus.org'
  $staticFilesDir = "$rootDir"

  apache2::vhost { "$site":
    content => template("webxray/apache-site.conf.erb")
  }
  
  file { "$rootDir":
    ensure => directory
  }
}
