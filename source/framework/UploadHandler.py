from source.framework.BaseHandler import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers


class FileUploadHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    """Web handler to handle file uploads"""
    @classmethod
    def nothing(cls):
        print("place-holder")
