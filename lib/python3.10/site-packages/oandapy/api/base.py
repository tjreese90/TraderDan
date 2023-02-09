import json

import requests
from requests.exceptions import Timeout, ReadTimeout, ConnectionError as RequestsConnectionError

from ..exceptions import EnvironmentNotFound, ServerError
from ..validators import validate_status_code
from ..factories import ResponseFactory


class RequestsTransport:
    def __init__(self, headers):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def make_request(self, method_name, endpoint, **kwargs):
        method = getattr(self.session, method_name.lower())
        return method(endpoint, **kwargs)


class Core:
    """
    Core Abstract object.
    Attributes:
        url_bases: URLs from OANDA environments
        api_version: OANDA's API Version
        timeout: Request timeout
        token: OANDA's API Access token
        transport: Transport class to able to use Requests or AioHTTP(AsyncIO)
    """
    api_version = 'v3'
    base_urls = {
        'live': 'https://api-fxtrade.oanda.com',
        'practice': 'https://api-fxpractice.oanda.com',
    }
    stream_urls = {
        'live': 'https://stream-fxtrade.oanda.com',
        'practice': 'https://stream-fxpractice.oanda.com',
    }

    def __init__(self, environment, access_token, timeout=3, **kwargs):
        """
        Args:
            environment (str): Provides the environment for OANDA's API.
            access_token (str): Specifies the access token.
            timeout (int): Set the request timeout. Default is 3
        """
        self.environment = environment
        self.base_url = self._get_base_url(environment)
        self.timeout = timeout
        self.token = access_token
        self.transport = RequestsTransport(headers=self.get_default_headers())

    def _get_base_url(self, environment, stream=False):
        """
        Get URL BASE of OANDA's API
        Args:
            environment (str):
            stream (boll):
        Returns:
             URL with oanda's API
        """
        url_base = self.base_urls.get(environment)
        if stream:
            url_base = self.stream_urls.get(environment)

        if not url_base:
            raise EnvironmentNotFound("Environment '{0}' does not exist!".format(environment))
        return "/".join((url_base, self.api_version))

    def get_default_headers(self, datetime_format="RFC3339"):
        """Get the required headers to access the API
        Returns:
             dict: Authorization and Content Type
        """
        return {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json',
            "Accept-Datetime-Format": datetime_format
        }

    def make_request(self, method_name, endpoint, stream=False, **kwargs):
        """Requests data from Oanda API.
        Args:
            endpoint (str): URL for Oanda API endpoint.
            method_name (str): Specifies the method to be used on the request.
            stream (str): Set request as Streamer URL
        Optional:
            params (dict, optional): Specifies parameters to be sent with the
            request.

        Returns:
            response: Requests response object.
        """
        base_url = self._get_base_url(self.environment, stream=stream)

        full_url = "/".join((base_url, endpoint))
        try:
            response = self.transport.make_request(
                method_name, full_url, timeout=self.timeout, stream=stream, **kwargs
            )
        except (Timeout, ReadTimeout, RequestsConnectionError) as exc:
            raise ServerError() from exc

        is_valid, exception_class = validate_status_code(
            response.status_code, response.json()
        )
        if not is_valid:
            raise exception_class

        return response

    def create(self, endpoint, data):
        """Do a POST without need to pass all arguments to make a request
        Args:
            endpoint (str): URL for Oanda API endpoint.
            data (dict, list of tuples): Data to send in the body of the request.

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        response = self.make_request('POST', endpoint, data=json.dumps(data))
        return ResponseFactory(response, endpoint)

    def update(self, endpoint, data, partial=False):
        """Do a update (PUT/PATCH) without need to pass all arguments to make a request
        Args:
            endpoint (str): URL for Oanda API endpoint.
            data (dict, list of tuples): Data to send in the body of the request.
            partial (bool): To specify whether the update will change everything
                            or just a few attributes. Default is False

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        method = 'PATCH' if partial else 'PUT'
        response = self.make_request(method, endpoint, data=json.dumps(data))
        return ResponseFactory(response, endpoint)

    def search(self, endpoint, stream=False, **kwargs):
        """Do a GET to make a search without need
           to pass all arguments to make a request.
        Args:
            endpoint (str): URL for Oanda API endpoint.
            stream (str): Set request as Streamer URL
        Kwargs(Optional):
            params (dict): Specifies parameters to be sent with the request.

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        params = kwargs.pop('params', {})
        response = self.make_request('GET', endpoint, stream=stream, params=params)
        return ResponseFactory(response, endpoint)

    class Meta:
        abstract = True
