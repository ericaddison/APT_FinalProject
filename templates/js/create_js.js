    function loadPageData() {
        document.getElementById('owner').value = localUser['id'];
        document.getElementById('results').style.visibility = "hidden";
    }

    function createConversation(){
        var owner = document.getElementById('owner').value;
        var convName = document.getElementById('convNameBox').value;
        var destDate = document.getElementById('destroyDateBox').value;

        $.ajax({url: '/api/conversations/', type: "POST",
             headers: {'Authorization': 'Bearer ' + userIdToken},
             data: {"owner": owner, "conv_name": convName, "destroy_date": destDate}

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

