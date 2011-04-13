class apache2 {
  $apacheDir = '/etc/apache2'

  package { 'libapache2-mod-wsgi':
    ensure => present,
  }

  service { 'apache2':
    ensure => running,
    enable => true,
    hasrestart => true,
    hasstatus => true,
  }

  # Don't let the default site interfere with our
  # virtual hosts.
  file { "$apacheDir/sites-enabled/000-default":
    ensure => absent,
    notify => Service['apache2'],
    require => Package['libapache2-mod-wsgi'],
  }

  define vhost($content) {
    include apache2

    file { "$apache2::apacheDir/sites-available/$name":
      ensure => file,
      owner => 'root',
      group => 'root',
      content => $content,
      notify => Service['apache2'],
      require => Package['libapache2-mod-wsgi'],
    }

    file { "$apache2::apacheDir/sites-enabled/001-$name":
      ensure => link,
      target => "$apache2::apacheDir/sites-available/$name",
      notify => Service['apache2'],
    }
  }
}
