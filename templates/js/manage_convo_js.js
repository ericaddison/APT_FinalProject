    function loadPageData() {

        var url = window.location.href;
        var convId = url.match(/(\d+)$/)[0];
        console.log("convId: " + convId);


        console.log("firebaseUser: " + userIdToken);
            if(userIdToken == null){
                window.location.replace("/login");
            }

            loadThisConversation(userIdToken, convId);

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

            document.getElementById('nameBox').value = conversationArray['name'];
            document.getElementById('createDateBox').value = conversationArray['createDate'].substring(0,10);
            document.getElementById('destroyDateBox').value = conversationArray['destroyDate'].substring(0,10);
            document.getElementById('revealOwnerBox').checked = (conversationArray['revealOwner'] === true);
            document.getElementById('viewAfterExpireBox').checked = (conversationArray['viewAfterExpire'] === true);
            document.getElementById('idPolicyBox').value = conversationArray['idPolicy'];

            console.log("checked: " + conversationArray['revealOwner']);


/*            var tab, tr, td, tn, row;
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
            tableDiv.appendChild(tab);*/
        })
    }


        function updateConversation(userToken) {
            var url = window.location.href;
            var convId = url.match(/(\d+)$/)[0];

            $.ajax({url:'/api/conversations/' + convId, type:'PUT',
            data: { 'conv_name': document.getElementById('nameBox').value,
                    'destroy_date': document.getElementById('destroyDateBox').value,
                    'idpolicy_date':document.getElementById('idPolicyBox').value,
                    'view_after_expire':document.getElementById('viewAfterExpireBox').checked,
                    'reveal_owner':document.getElementById('revealOwnerBox').checked },
            headers: {'Authorization': 'Bearer ' + userIdToken}

                //Create and populate the Conversation Table
            }).then(function (result) {
                document.getElementById('resultBox').value = result['conversations'];

            })
        }

