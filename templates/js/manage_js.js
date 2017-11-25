    function loadPageData() {

    console.log("firebaseUser: " + userIdToken);

            if(userIdToken == null){
                window.location.replace("/login");
            }

            loadAllConversations(userIdToken);

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
//Maybe get/display some more data on each conversation?

                })
            }

            var tab, tr, td, tn, row;
            tableDiv = document.getElementById('conversationTable');

            tab = document.createElement('table');
            tr = document.createElement('tr');
            td = document.createElement('td');
            tn = document.createTextNode('');
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
