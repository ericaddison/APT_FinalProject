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



    function populateTable (record) {
        return new Promise(function (resolve, reject) {
            convApiUrl = '/api/conversations/' + record['id'];
            $.ajax(convApiUrl, {headers: {'Authorization': 'Bearer ' + userIdToken}})
                .then(function (result) {
                    id = result['conversations']['id'];
                    name = result['conversations']['name'];
                    createDate = result['conversations']['createDate'];
                    destroyDate = result['conversations']['destroyDate'];
                    numUsers = result['conversations']['aliases'].length;
                    tableRecord = [name, createDate, destroyDate, numUsers];
                    console.log("tableRecord: " + tableRecord);
                    convListArray.push(tableRecord);  // Don't push to the array here, instead append the data to the table directly.,
                    resolve(tableRecord);
                })
        })
    }


    function createTable(dataArray, tableId) {
        console.log("createTable() start; array: " + dataArray);
        tableDiv = document.getElementById(tableId);
        var table = document.createElement('table');
        var tableBody = document.createElement('tbody');
        dataArray.forEach(function (rowData) {
            var row = document.createElement('tr');
            rowData.forEach(function (cellData) {
                var cell = document.createElement('td');
                cell.appendChild(document.createTextNode(cellData));
                row.appendChild(cell);
            });
            tableBody.appendChild(row);
        });
        table.appendChild(tableBody);
        tableDiv.appendChild(table);
    }

