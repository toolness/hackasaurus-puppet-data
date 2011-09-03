class repositories {
  $rootDir = "/var/repositories"
  
  vcsrepo { "$rootDir/django":
    ensure => "present",
    source => "https://github.com/django/django.git",
    require => File["$rootDir"]
  }

  file { "$rootDir":
    ensure => directory,
  }
}
