import webapp2
import json

# [BEGIN jinja2 setup]
from jinja2 import Environment, FileSystemLoader, Template
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
j2_env = Environment(loader=FileSystemLoader('./templates'),
                     trim_blocks=True)
# [END jinja2 setup]


class BaseHandler(webapp2.RequestHandler):
    """Base class for all Hailing-Frequencies web handlers to extend"""

    def get_request_param(self, param_name):
        return self.request.get(param_name)

    def write_response(self, response_text):
        self.response.write(response_text)

    def write_dictionary_response(self, response_dictionary):
        self.write_response(json.dumps(response_dictionary))

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
        self.write_response(j2_env.get_template(path).render(template_values_dict))
