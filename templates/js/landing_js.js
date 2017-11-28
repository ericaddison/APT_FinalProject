//JS for the LandingPage goes here.
//See if there's an active user, if so display a list of all conversations with links to visit them.
var conversationArray;
//var convListArray = [['Name', 'CreateDate', 'DestroyDate', 'NumUsers'],
                //['Sample', '1999-01-01 23:59:59', '2999-12-31 23:59:59', '5']];

var convListArray = [['Name']];

var tableDiv  = document.getElementById('conversationTable');

    function loadPageData() {
        loadAllConversations(userIdToken);
    }


    function loadAllConversations(userIdToken) {
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
            tn = document.createTextNode('Join Active Conversation:');
            td.appendChild(tn);
            tr.appendChild(td);
            tab.appendChild(tr);
            for (row = 0; row < conversationArray.length; row++) {
                tr = document.createElement('tr');
                td = document.createElement('td');
                tn = document.createTextNode(conversationArray[row]['name']);
                convLink = document.createElement('a');
                myLink = '/view/' + conversationArray[row]['id'];
                convLink.setAttribute('href', myLink);
                convLink.appendChild(tn);
                td.appendChild(convLink);
                tr.appendChild(td);
                tab.appendChild(tr);
            }
            tableDiv.appendChild(tab);
        })
    }

