class testswarm::user_creation {

  define swarmuser( $password, $email, $request ) {
    include testswarm

    exec { "add-testswarm-user-$name":
      command => "/usr/bin/curl --header \"Host: $testswarm::site\" -d \"username=$name&password=$password&email=$email&request=$request\" http://127.0.0.1/signup/"
    }
  }

  swarmuser { "$swarmuser":
    password => $secret_swarmuser_pw,
    email => $secret_swarmuser_email,
    request => 'account-for-hackasaurus-projects'
  }
}
