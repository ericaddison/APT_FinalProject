var url = window.location.href;
var convId = url.match(/(\d+)$/)[0];
console.log("convId: " + convId);


function loadPageData(){



    var convoDetails = document.getElementById('convoDetails');
    getConversationDetails(convId).then(function(result){
        convName = result[0];
        createDate = result[1];
        destroyDate = result[2];
        numUsers = result[3];

        displayText = "<i><b>" + convName + "</b><br>Created: " + createDate + "<br>Expires: " + destroyDate + "</i>";

        convoDetails.innerHTML = displayText});
    window.ChatApp = new ChatApp();



}

function getConversationDetails(conversationId){
    return new Promise(function (resolve, reject) {
        convApiUrl = '/api/conversations/' + conversationId;
        $.ajax(convApiUrl, {headers: {'Authorization': 'Bearer ' + userIdToken}})
            .then(function (result) {
                id = result['conversations']['id'];
                name = result['conversations']['name'];
                createDate = result['conversations']['createDate'];
                destroyDate = result['conversations']['destroyDate'];
                numUsers = result['conversations']['aliases'].length;
                tableRecord = [name, createDate, destroyDate, numUsers];
                console.log("tableRecord: " + tableRecord);
                resolve(tableRecord);
                })
        })
}