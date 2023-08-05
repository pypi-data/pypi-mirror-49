import requests
from urllib import parse
import weakref
from ._util import _formatDuration, _printErrorMessage

class _OncService:
    """
    Provides common configuration and functionality to Onc service classes (children)
    """

    def __init__(self, parent: object):
        # Children all have a copy of config
        self.parent = weakref.ref(parent)
        

    def _doRequest(self, url: str, filters: dict=None):
        """
        Generic request wrapper for making simple web service requests
        @param url:    String full url to request
        @param params: Dictionary of parameters to append to the request
        @return:       JSON object obtained on a successful request
        @throws:       Exception if the HTTP request fails with status 400, as a tuple with
                       the error description and the error JSON structure returned
                       by the API, or a generic exception otherwise
        """
        if filters is None: filters = {}
        timeout = self._config('timeout')
        
        try:
            txtParams = parse.unquote(parse.urlencode(filters))
            self._log('Requesting URL:\n{:s}?{:s}'.format(url, txtParams))
            response = requests.get(url, filters, timeout=timeout)
            
            if response.ok:
                jsonResult = response.json()
            else:
                status = response.status_code
                if status in [400, 401]:
                    _printErrorMessage(response)
                    raise Exception('The request failed with HTTP status {:d}.'.format(status), response.json())
                else:
                    raise Exception('The request failed with HTTP status {:d}.'.format(status), response.text)

            elapsed = response.elapsed.total_seconds()
            self._log('Web Service response time: {:s}'.format(_formatDuration(elapsed)))
        
        except requests.exceptions.Timeout:
            raise Exception('The request ran out of time (timeout: {:d} s)'.format(timeout)) from None
        except Exception:
            raise

        return jsonResult


    def _serviceUrl(self, service: str):
        """
        Returns the absolute url for a given ONC API service
        """
        if service in ['locations', 'deployments', 'devices', 'deviceCategories', 'properties', 'dataProducts', 'archivefiles', 'scalardata', 'rawdata']:
            return '{:s}api/{:s}'.format(self._config('baseUrl'), service)
        
        return ''


    def _log(self, message: str):
        """
        Prints message to console only when self.showInfo is true
        @param message: String
        """
        if self._config('showInfo'):
            print(message)


    def _config(self, key: str):
        """
        Returns a property from the parent (ONC class)
        """
        return getattr(self.parent(), key)