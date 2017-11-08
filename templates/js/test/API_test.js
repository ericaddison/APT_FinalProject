console.log("???")
$(document).ready(function(){


    // create a state string and encode it
    // Encode the String
    var string = 'abc123'
    var encodedString = btoa(string);

    var aud = "https://hailing-frequencies-2017.appspot.com/"
    var clientID = "JhKTQ3FyHLTEY3PPsQ6MQ8OXsUXuNXEN"
    var redirect_uri = "http://localhost:8080/api/callback"

    var authUrl = "https://hailing-frequencies.auth0.com/authorize?scope="
    authUrl += "&audience=" + encodeURIComponent(aud)
    authUrl += "&response_type=code"
    authUrl += "&client_id=" + encodeURIComponent(clientID)
    authUrl += "&redirect_uri=" + encodeURIComponent(redirect_uri)

    $("body").append("<a href=\""+authUrl+"\">Authorize API with auth0</a>")


});