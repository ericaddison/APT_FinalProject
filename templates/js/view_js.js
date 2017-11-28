var url = window.location.href;
var convId = url.match(/(\d+)$/)[0];
console.log("convId: " + convId);


function loadPageData(){


    getConversationDetails(convId).then(function(result){
        var convoDetails = document.getElementById('convoDetails');

        if(result[1]) {
            convName = result[0];
            createDate = result[1];
            destroyDate = result[2];
            numUsers = result[3];
            displayText = "<i><b>" + convName + "</b><br>Created: " + createDate + "<br>Expires: " + destroyDate + "<br>User Count: " + numUsers + "</i>";
            document.getElementById('resultBox').value = "Posting Allowed";
        }
        else {
            convName = result[0];
            destroyDate = result[2];
            displayText = "<i><b>" + convName + "</b><br>Expires: " + destroyDate + "</i>";
            document.getElementById('resultBox').value = "Not Allowed to Post";
        }


        convoDetails.innerHTML = displayText});
    window.ChatApp = new ChatApp();
}

function getConversationDetails(conversationId){
    return new Promise(function (resolve, reject) {
        convApiUrl = '/api/conversations/' + conversationId;
        $.ajax(convApiUrl, {headers: {'Authorization': 'Bearer ' + userIdToken}})
            .then(function (result) {
                if(result['conversations']['aliases']){
                    console.log("***User is joined to this conversation");
                    name = result['conversations']['name'];
                    createDate = result['conversations']['createDate'];
                    destroyDate = result['conversations']['destroyDate'];
                    numUsers = result['conversations']['aliases'].length;
                    tableRecord = [name, createDate, destroyDate, numUsers];
                    console.log("tableRecord: " + tableRecord);
                    resolve(tableRecord);

                }
                else {
                    console.log("***User is NOT joined to this conversation");

                    //id = result['conversations']['id'];
                    name = result['conversations']['name'];
                    //createDate = result['conversations']['createDate'];
                    destroyDate = result['conversations']['destroyDate'];
                    //numUsers = result['conversations']['aliases'].length;
                    tableRecord = [name, , destroyDate ];
                    console.log("tableRecord: " + tableRecord);
                    resolve(tableRecord);
                }
                })
        })
}

