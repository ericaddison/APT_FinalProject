
importScripts("https://www.gstatic.com/firebasejs/4.6.2/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/4.6.2/firebase-auth.js");
importScripts("https://www.gstatic.com/firebasejs/4.6.2/firebase-database.js");
importScripts("https://www.gstatic.com/firebasejs/4.6.2/firebase-messaging.js");

var config = {
    apiKey: "AIzaSyAq2ZvX1YatNlTsE6p5sDqZaNCVsEbcGxw",
    authDomain: "hailing-frequencies-2017.firebaseapp.com",
    databaseURL: "https://hailing-frequencies-2017.firebaseio.com",
    projectId: "hailing-frequencies-2017",
    storageBucket: "hailing-frequencies-2017.appspot.com",
    messagingSenderId: "153356807079"
};


firebase.initializeApp(config);

const messaging = firebase.messaging();
