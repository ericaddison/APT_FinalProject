  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyAq2ZvX1YatNlTsE6p5sDqZaNCVsEbcGxw",
    authDomain: "hailing-frequencies-2017.firebaseapp.com",
    databaseURL: "https://hailing-frequencies-2017.firebaseio.com",
    projectId: "hailing-frequencies-2017",
    storageBucket: "hailing-frequencies-2017.appspot.com",
    messagingSenderId: "153356807079"
    };

  firebase.initializeApp(config);


    var firebaseUser;
    var localUser;
    var localUserId;
    var userIdToken;

      function initApp () {
        return new Promise(function(resolve, reject){
        firebase.auth().onAuthStateChanged(function(user) {
          if (user) {
            // User is signed in.
              firebaseUser = user;
            var displayName = user.displayName;
            var email = user.email;
            var emailVerified = user.emailVerified;
            var photoURL = user.photoURL;
            var uid = user.uid;
            var providerData = user.providerData;

            user.getIdToken().then(function(accessToken) {
                userIdToken = accessToken;
              document.getElementById('sign-in-status').textContent = 'Signed in as ' + displayName + " <" + email + ">";
              document.getElementById('sign-in').textContent = 'Sign out';
              document.getElementById('account-details').textContent = JSON.stringify({
                displayName: displayName,
                email: email,
                emailVerified: emailVerified,
                photoURL: photoURL,
                uid: uid,
                accessToken: accessToken,
                providerData: providerData

              }, null, '  ');
            });
            resolve();
          } else {
            // User is signed out.
            document.getElementById('sign-in-status').textContent = 'Not Signed In';
            document.getElementById('sign-in').textContent = 'Sign In';
            document.getElementById('account-details').textContent = 'null';
            reject();
          }
        },
            function(error) {
          console.log(error);}

        )}
        )}


        function userDataLoaded(){
          return new Promise(function(resolve, reject) {
              console.log("***userDataLoaded()");
              resolve();
          })
        }





      window.addEventListener('load', function() {
                initApp().then(function (){
                    $.ajax({url:'/api/users/', type: "GET", headers: {'Authorization': 'Bearer ' + userIdToken}
                    }).then(function (result) {
                        if(result) {
                            localUser = result['user'];
                            localUserId = localUser['id'];
                            userDataLoaded().then(loadPageData());
                        }
                        })
                    })
                });

