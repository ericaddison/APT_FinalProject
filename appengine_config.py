# appengine_config.py
from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
vendor.add('lib/jwt')
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))