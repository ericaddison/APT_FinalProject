    function loadPageData() {

    console.log("firebaseUser: " + userIdToken);

            if(userIdToken == null){
                window.location.replace("/login");
            }

            loadAllConversations(userIdToken);

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
            window.alert("Data updated; refresh page");
        })
    }


    function loadAllConversations(userToken) {
        $.ajax('/api/ownedconversations/', {
            headers: {'Authorization': 'Bearer ' + userIdToken}

        //Create and populate the Conversation Table
        }).then(function (result) {
            conversationArray = result['conversations'];

            for(var x = 0; x < conversationArray.length; x++){
                $.ajax('/api/conversations/' + conversationArray[x]['id'], {
                    headers: {'Authorization': 'Bearer ' + userIdToken}
                }).then(function (result) {
                    console.log("result:" + result);


                })
            }

            var tab, tr, td, tn, row;
            tableDiv = document.getElementById('conversationTable');

            tab = document.createElement('table');
            tr = document.createElement('tr');
            td = document.createElement('td');
            tn = document.createTextNode('Manage My Conversations:');
            td.appendChild(tn);
            tr.appendChild(td);
            tab.appendChild(tr);
            for (row = 0; row < conversationArray.length; row++) {
                tr = document.createElement('tr');
                td = document.createElement('td');
                tn = document.createTextNode(conversationArray[row]['name']);
                convLink = document.createElement('a');
                myLink = '/manage/' + conversationArray[row]['id'];
                convLink.setAttribute('href', myLink);
                convLink.appendChild(tn);
                td.appendChild(convLink);
                tr.appendChild(td);
                tab.appendChild(tr);
            }
            tableDiv.appendChild(tab);
        })
    }
