
    function loadPageData() {
        document.getElementById('owner').value = localUser['id'];
        document.getElementById('results').style.visibility = "hidden";

    }

    function createConversation(){
        var owner = document.getElementById('owner').value;
        var convName = document.getElementById('convNameBox').value;
        var destDate = document.getElementById('destroyDateBox').value;
        var rawPassword = document.getElementById('passwordBox').value;
        var hashedPassword = null;
        // Doesn't work yet... "requirejs is not defined"
        //if(rawPassword) {
        //        requirejs(['bcrypt'], function(bcrypt){
        //            const saltRounds = 10;
        //            bcrypt.hash(rawPassword, saltRounds, function(err, hash) {
        //            hashedPassword = hash;
        //            });
        //        })
        //}

        //REFERENCE:  To check a password:
        //bcrypt.compare(myPlaintextPassword, hash, function(err, res) {
             // if (res == true)...
        //});


        $.ajax({url: '/api/conversations/', type: "POST",
             headers: {'Authorization': 'Bearer ' + userIdToken},
             data: {"owner": owner, "conv_name": convName, "password": hashedPassword, "destroy_date": destDate}

            }).then(function(result){
                //do stuff with the result
                if(result['status'] == '200'){
                    document.getElementById('resultBox').value = "Success";
                }
                else{
                    document.getElementById('resultBox').value = "Failure";

                }
                document.getElementById('results').style.visibility = "visible";

            })


    }

