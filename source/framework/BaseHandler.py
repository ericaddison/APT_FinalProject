import webapp2
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
import json

# a base class for all request handlers in our app
class BaseHandler(webapp2.RequestHandler):

    def get_request_param(self, param_name):
        return self.request.get(param_name)

    def write_response(self, response_text):
        self.response.write(response_text)

    def write_dictionary_response(self, response_dictionary):
        self.response.write(json.dumps(response_dictionary))

    def get_request_parameter_dictionary(self):
        return self.request.params

    def set_content_text_plain(self):
        self.response.content_type = 'text/plain'

    def set_content_text_json(self):
        self.response.content_type = 'application/json'

    def set_content_text_html(self):
        self.response.content_type = 'text/html'

    def redirect(self, url):
        super(BaseHandler, self).redirect(url)

    def get_current_url(self):
        return self.request.url

    def render_template(self, path, template_values_dict):
        self.write_response(template.render(path, template_values_dict))


# file handler. Currently just extends BaseHandler and google blobstoreUpload handler
class FileUploadHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    @classmethod
    def nothing(cls):
        print("place-holder")
