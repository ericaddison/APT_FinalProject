from source.framework.BaseHandler import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers


# file handler. Currently just extends BaseHandler and google blobstoreUpload handler
class FileUploadHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    @classmethod
    def nothing(cls):
        print("place-holder")
