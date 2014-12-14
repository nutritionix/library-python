import logging
import json
import requests
import urlparse

API_VERSION = "v2"
BASE_URL = "https://api0.nutritionix.com/%s/" % (API_VERSION)


class NutritionixClient:

    def __init__(self, application_id=None, api_key=None, debug=False, *arg, **kwarg):
        self.APPLICATION_ID = application_id
        self.API_KEY = api_key
        self.DEBUG = False

        if debug == True:
            self.DEBUG = debug
            logging.basicConfig(level=logging.DEBUG)

    def _version(self, *arg):
        return API_VERSION

    def _application_id(self, *arg):
        return self.APPLICATION_ID

    def _api_key(self, *arg):
        return self.API_KEY

    def execute(self, url=None, method='GET', params={}, data={}, headers={}, *arg):
        """ Bootstrap, execute and return request object,
                default method: GET
        """
        method = method.lower()

        headers['X-APP-ID'] = self.APPLICATION_ID
        headers['X-APP-KEY'] = self.API_KEY

        if method == "get" or not 'method' in locals():
            r = requests.get(url, params=params, headers=headers)

        elif method == "post":
            r = requests.post(url, params=params, data=data, headers=headers)

        # TODO: UPDATE, DELETE methods
        elif method == "update":
            pass

        elif method == "delete":
            pass

        else:
            return None

        logging.debug("Response Content: %s" % (r.text))

        return r.json()

    #--------------
    # API Methods #
    #--------------

    def autocomplete(self, description='', **kwargs):
        """
        Specifically designed to provide autocomplete functionality for search
        boxes. The term selected by the user in autocomplete will pass to
        the /search endpoint.
        """
        endpoint = urlparse.urljoin(BASE_URL, 'autocomplete')

        # If first arg is String then use it as description
        if type(description) == str:
            params = {'q': description}

            # Adds optional args to the params dictionary
            for key, value in kwargs.iteritems():
                params[key] = value

        # If first arg is a dictionary then pass it as request params
        elif type(description) == dict:
            params = description
            if kwargs:
                raise Exception('Mixing dictionary argument with others arguments',
                                'You can\'t pass more arguments when using a dictionary as firt argument')

        return self.execute(endpoint, params=params)

    def natural(self, text, **kwargs):
        """
        Supports natural language queries like "1 cup butter" or "100cal yogurt"
        """

        # If first arg is String then use it as text
        if type(text) == str:
            params = {'q': text}

            # Adds optional args to the params dictionary
            for key, value in kwargs.iteritems():
                params[key] = value

        # If first arg is a dictionary then pass it as request params
        elif type(text) == dict:
            params = text
            if kwargs:
                raise Exception('Mixing dictionary argument with others arguments',
                                'You can\'t pass more arguments when using a dictionary as firt argument')

        # Converts 'q' argument as request data
        data = ''
        if params.get('q'):
            data = params.get('q')
            # Removes 'q' argument from params to avoid pass it as URL argument
            del params['q']

        endpoint = urlparse.urljoin(BASE_URL, 'natural')

        return self.execute(endpoint, method="POST", params=params, data=data, headers={'Content-Type': 'text/plain'})

    def search(self, keyword, **kwargs):  # TODO: Add advance search filters
        """
        Search for an entire food term like "mcdonalds big mac" or "celery." 
        """
        endpoint = urlparse.urljoin(BASE_URL, 'search')

        # If first arg is String then use it as keyword
        if type(keyword) == str:
            params = {'q': keyword}

            # Adds optional args to the params dictionary
            for key, value in kwargs.iteritems():
                params[key] = value

        # If first arg is a dictionary then pass it as request params
        elif type(keyword) == dict:
            params = keyword
            if kwargs:
                raise Exception('Mixing dictionary argument with others arguments',
                                'You can\'t pass more arguments when using a dictionary as firt argument')

        return self.execute(endpoint, params=params)

    def item(self, id, **kwargs):  # TODO: Look up by UPC
        """Look up a specific item by ID or UPC"""

        # If first arg is String then use it as id
        if type(id) == str:
            params = {'id': id}

            # Adds optional args to the params dictionary
            for key, value in kwargs.iteritems():
                params[key] = value

        # If first arg is a dictionary then pass it as request params
        elif type(id) == dict:
            params = id

            if kwargs:
                raise Exception('Mixing dictionary argument with others arguments',
                                'You can\'t pass more arguments when using a dictionary as firt argument')

        endpoint = urlparse.urljoin(BASE_URL, 'item/%s' % (params.get('id')))

        return self.execute(endpoint)

    def brand(self, id, **kwargs):
        """Look up a specific brand by ID. """

        # If first arg is String then use it as id
        if type(id) == str:
            params = {'id': id}

            # Adds optional args to the params dictionary
            for key, value in kwargs.iteritems():
                params[key] = value

        # If first arg is a dictionary then pass it as request params
        elif type(id) == dict:
            params = id

            if kwargs:
                raise Exception('Mixing dictionary argument with others arguments',
                                'You can\'t pass more arguments when using a dictionary as firt argument')

        endpoint = urlparse.urljoin(BASE_URL, 'brand/%s' % (params.get('id')))
        return self.execute(endpoint)

    def brand_search(self, keyword, **kwargs):
        """Look up a specific brand by ID. """

        # If first arg is String then use it as keyword
        if type(keyword) == str:
            params = {'q': keyword}

            # Adds optional args to the params dictionary
            for key, value in kwargs.iteritems():
                params[key] = value

        # If first arg is a dictionary then pass it as request params
        elif type(keyword) == dict:
            params = keyword

            if kwargs:
                raise Exception('Mixing dictionary argument with others arguments',
                                'You can\'t pass more arguments when using a dictionary as firt argument')

        endpoint = urlparse.urljoin(BASE_URL, 'search/brands/')
        return self.execute(endpoint, params=params)
