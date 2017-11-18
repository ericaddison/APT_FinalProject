    function loadPageData() {

            loadAllConversations(userIdToken);

            document.getElementById('emailBox').value = localUser['email'];
            document.getElementById('fnameBox').value = localUser['fName'];
            document.getElementById('lnameBox').value = localUser['lName'];
            document.getElementById('dateBox').value = localUser['joinDate'];
            document.getElementById('commPrefBox').value = localUser['prefComm'];
        }


    function loadAllConversations(userToken) {
        $.ajax('/api/conversations/', {
            headers: {'Authorization': 'Bearer ' + userIdToken}

        //Create and populate the Conversation Table
        }).then(function (result) {
            conversationArray = result['conversations'];

            var tab, tr, td, tn, row;
            tableDiv = document.getElementById('conversationTable');

            tab = document.createElement('table');
            tr = document.createElement('tr');
            td = document.createElement('td');
            tn = document.createTextNode('Conv ID');
            td.appendChild(tn);
            tr.appendChild(td);
            td = document.createElement('td');
            tn = document.createTextNode('Conv Name');
            td.appendChild(tn);
            tr.appendChild(td);
            tab.appendChild(tr);
            for (row = 0; row < conversationArray.length; row++) {
                tr = document.createElement('tr');
                td = document.createElement('td');
                tn = document.createTextNode(conversationArray[row]['id']);
                td.appendChild(tn);
                tr.appendChild(td);
                td = document.createElement('td');
                tn = document.createTextNode(conversationArray[row]['name']);
                td.appendChild(tn);
                tr.appendChild(td);
                tab.appendChild(tr);
            }
            tableDiv.appendChild(tab);
        })
    }


