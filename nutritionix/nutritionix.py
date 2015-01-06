import logging
import json
import requests
import urlparse

API_VERSION = "v2"
BASE_URL = "https://apibeta.nutritionix.com/%s/" % (API_VERSION)


class NutritionixClient:

    def __init__(self, application_id=None, api_key=None, debug=False, *arg, **kwarg):
        self.APPLICATION_ID = application_id
        self.API_KEY = api_key
        self.DEBUG = False

        if debug == True:
            self.DEBUG = debug
            logging.basicConfig(level=logging.DEBUG)

    def get_api_version(self, *arg):
        return API_VERSION

    def get_application_id(self, *arg):
        return self.APPLICATION_ID

    def get_api_key(self, *arg):
        return self.API_KEY

    def execute(self, url=None, method='GET', params={}, data={}, headers={}):
        """ Bootstrap, execute and return request object,
                default method: GET
        """

        # Verifies params
        if params.get('limit') != None and params.get('offset') == None:
            raise Exception('Missing offset',
                            'limit and offset are required for paginiation.')

        elif params.get('offset') != None and params.get('limit') == None:
            raise Exception('Missing limit',
                            'limit and offset are required for paginiation.')

        # Bootstraps the request
        method = method.lower()

        headers['X-APP-ID'] = self.APPLICATION_ID
        headers['X-APP-KEY'] = self.API_KEY

        # Executes the request
        if method == "get" or not 'method' in locals():
            r = requests.get(url, params=params, headers=headers)

        elif method == "post":
            r = requests.post(url, params=params, data=data, headers=headers)

        else:
            return None

        # Log response content
        logging.debug("Response Content: %s" % (r.text))

        return r.json()


    #--------------
    # API Methods #
    #--------------

    def autocomplete(self, **kwargs):
        """
        Specifically designed to provide autocomplete functionality for search
        boxes. The term selected by the user in autocomplete will pass to
        the /search endpoint.
        """
        
        # If first arg is String then use it as query
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urlparse.urljoin(BASE_URL, 'autocomplete')

        return self.execute(endpoint, params=params)

    def natural(self, **kwargs):
        """
        Supports natural language queries like "1 cup butter" or "100cal yogurt"
        """

        # If first arg is String then use it as query
        params = {}
        if kwargs:
            params = kwargs

        # Converts 'q' argument as request data
        data = ''
        if params.get('q'):
            data = params.get('q')
            # Removes 'q' argument from params to avoid pass it as URL argument
            del params['q']

        endpoint = urlparse.urljoin(BASE_URL, 'natural')

        return self.execute(endpoint, method="POST", params=params, data=data, headers={'Content-Type': 'text/plain'})

    def search(self, **kwargs):  # TODO: Add advance search filters
        """
        Search for an entire food term like "mcdonalds big mac" or "celery." 
        """

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urlparse.urljoin(BASE_URL, 'search')

        return self.execute(endpoint, params=params)

    def item(self, **kwargs):
        """Look up a specific item by ID or UPC"""

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urlparse.urljoin(BASE_URL, 'item/%s' % (params.get('id')))

        return self.execute(endpoint)

    def brand(self, **kwargs):
        """Look up a specific brand by ID. """

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urlparse.urljoin(BASE_URL, 'brand/%s' % (params.get('id')))

        return self.execute(endpoint)

    def brand_search(self, **kwargs):
        """Look up a specific brand by ID. """

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urlparse.urljoin(BASE_URL, 'search/brands/')

        return self.execute(endpoint, params=params)
