class htmlpad {
  $site = 'htmlpad.org'
  $etherpad = 'etherpad.mozilla.org:9000'
  $rootDir = '/var/htmlpad'
  $wsgiDir = "$rootDir/wsgi-scripts"
  $staticFilesDir = "$rootDir/static-files"

  apache2::vhost { "$site":
    content => template("htmlpad/apache-site.conf.erb")    
  }

  vcsrepo { "$rootDir":
    ensure => present,
    source => "git://github.com/toolness/htmlpad.git"
  }
}
