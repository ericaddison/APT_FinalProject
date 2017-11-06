import webapp2


def make_routes(routelist):
    """Establish http routes for the given routelist of tuples containing (route, handler object)"""
    return webapp2.WSGIApplication(routelist, debug=True)
