    function loadPageData() {

    console.log("firebaseUser: " + userIdToken);

            if(userIdToken == null){
                window.location.replace("/login");
            }


            document.getElementById('emailBox').value = localUser['email'];
            document.getElementById('fnameBox').value = localUser['fName'];
            document.getElementById('lnameBox').value = localUser['lName'];
            document.getElementById('dateBox').value = (localUser['joinDate']).substring(0,19);
            document.getElementById('commPrefBox').value = localUser['prefComm'];
        }


    function updateUser(userToken) {
        $.ajax({url:'/api/users/', type:'PUT',
            data: {'fname': document.getElementById('fnameBox').value,
                   'lname': document.getElementById('lnameBox').value,
                    'prefcomm': document.getElementById('commPrefBox').value},
            headers: {'Authorization': 'Bearer ' + userIdToken}
        }).then(function (result) {
            if (result['status'] == "200"){
                document.getElementById('resultBox').value = "User Updated";
            }
            else{
                document.getElementById('resultBox').value = "Update Failed";
            }

        })
    }


