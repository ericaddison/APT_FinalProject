$(document).ready(function(){

var clientID = "JhKTQ3FyHLTEY3PPsQ6MQ8OXsUXuNXEN"
var clientSecret = "B9hr8uMQTD514hlYRNBYDlVEtdkJyZiEylY838RJOjsP23OlLppMDYY_1lu0Brxn"
var authCode = $('meta[name="authcode"]').attr('code')
var redirect_uri = "http://localhost:8080/api/callback"

var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://hailing-frequencies.auth0.com/oauth/token",
  "method": "POST",
  "headers": {
    "content-type": "application/json"
  },
  "processData": false,
  "data": "{\"grant_type\":\"authorization_code\",\"client_id\": \"" + clientID + "\",\"client_secret\": \""+ clientSecret +"\",\"code\": \""+authCode+"\",\"redirect_uri\": \""+redirect_uri+"\"}"
}

$.ajax(settings).done(function (response) {
  console.log(response);
  access_token = response.access_token
  $("body").append(response)
});


$("#api_button").click(function(){

    var settings = {
      "async": true,
      "url": "/api/users/",
      "method": "GET",
      "headers": {
        "content-type": "application/json",
        "authorization": "Bearer " + access_token
      }
    }

    $.ajax(settings).done(function (response) {
      console.log(response);
    });


})


});