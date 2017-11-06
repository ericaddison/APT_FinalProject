import webapp2


def make_routes(routelist):
    """Establish http routes for the given list of routes containing tuples of the form (route, handler object)"""
    return webapp2.WSGIApplication(routelist, debug=True)
