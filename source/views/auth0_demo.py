import webapp2
import urllib2
import urllib
import json
from source.config.auth0 import *


MAIN_PAGE_HTML = """\
<html>
  <body>
    <script src="https://cdn.auth0.com/w2/auth0-widget-2.6.min.js"></script>
    <script type="text/javascript">

      var widget = new Auth0Widget({
        domain:         '%s',
        clientID:       '%s',
        callbackURL:    '%s'
      });

    </script>
    <button onclick="widget.signin()">Login</button>
  </body>
</html>
""" % (DOMAIN, CLIENT_ID, CALLBACK_URL)


class Auth0MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)


class Auth0LoginCallback(webapp2.RequestHandler):
    def get(self):
        code = self.request.get("code")
        base_url = "https://{domain}".format(domain=DOMAIN)
        data = urllib.urlencode([('client_id', CLIENT_ID),
                                 ('redirect_uri', CALLBACK_URL),
                                 ('client_secret', CLIENT_SECRET),
                                 ('code', code),
                                 ('grant_type', 'authorization_code')])
        req = urllib2.Request(base_url + "/oauth/token", data)
        response = urllib2.urlopen(req)
        oauth = json.loads(response.read())
        userinfo = base_url + "/userinfo?access_token=" + oauth['access_token']

        response = urllib2.urlopen(userinfo)
        data = response.read()

        ## print user data
        self.response.write(data)