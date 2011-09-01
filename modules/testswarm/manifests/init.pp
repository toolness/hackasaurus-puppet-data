class testswarm {
  $site = "swarm.hksr.us"
  $rootDir = "/var/$site"
  $wsgiDir = "$rootDir/wsgi"
  $wwwDir = "$rootDir/www"
  $db = "testswarm"
  $user = $db
  $pw = $secret_testswarm_pw
  $swarmuser = "hackasaurus"
  $jobCheckoutDir = "$wwwDir/jobs"
  
  stage { "post_main": require => Stage["main"] }
  class { "testswarm::environment_setup": stage => main }
  class { "testswarm::user_creation": stage => post_main }
}

