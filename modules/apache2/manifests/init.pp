class apache2 {
  package { 'libapache2-mod-wsgi':
    ensure => present,
  }

  service { 'apache2':
    ensure => running,
    enable => true,
    hasrestart => true,
    hasstatus => true,
  }

  define vhost($content) {
    include apache2

    $apacheDir = '/etc/apache2'

    file { "$apacheDir/sites-available/$name":
      ensure => file,
      owner => 'root',
      group => 'root',
      content => $content,
      notify => Service['apache2'],
      require => Package['libapache2-mod-wsgi'],
    }

    file { "$apacheDir/sites-enabled/001-$name":
      ensure => link,
      target => "$apacheDir/sites-available/$name",
      notify => Service['apache2'],
    }
  }
}
