    function loadPageData() {

        var url = window.location.href;
        var convId = url.match(/(\d+)$/)[0];
        console.log("convId: " + convId);


        console.log("firebaseUser: " + userIdToken);
            if(userIdToken == null){
                window.location.replace("/login");
            }

            loadThisConversation(userIdToken, convId);
            loadConversationUsers(userIdToken, convId);

            document.getElementById('emailBox').value = localUser['email'];
            document.getElementById('fnameBox').value = localUser['fName'];
            document.getElementById('lnameBox').value = localUser['lName'];
            document.getElementById('dateBox').value = (localUser['joinDate']).substring(0,19);
            document.getElementById('commPrefBox').value = localUser['prefComm'];
        }


/*    name - readonly
    createDate - readonly
    destroyDate
    revealOwner - T/F
    viewAfterExpire - T/F
    aliases... list 0...n.... "Mr. White" Mute[x]
    idPolicy (colors_policy)*/

        function loadThisConversation(userToken, convId) {
            $.ajax('/api/conversations/' + convId, {
                headers: {'Authorization': 'Bearer ' + userIdToken}

                //Create and populate the Conversation Table
            }).then(function (result) {
                conversationArray = result['conversations'];

            })
        }


//No Value to loading this.  Just returns the alias names.
    function loadConversationUsers(userToken, convId) {
        $.ajax('/api/conversations/' + convId + '/users/', {
            headers: {'Authorization': 'Bearer ' + userIdToken}

        //Create and populate the Conversation Table
        }).then(function (result) {
            conversationArray = result['conversations'];


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



