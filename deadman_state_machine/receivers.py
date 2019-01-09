import abc
import logging
from urllib.parse import urlparse, urlunparse
from urllib.error import HTTPError, URLError
from urllib import request
from socket import timeout
import json


class Receiver(metaclass=abc.ABCMeta):
    """
    Define an interface for encapsulating the behavior associated with a
    particular receiver.

    Custom receiver lasses must implement this clas in order to be compatible
    with Deadman State Machine
    """

    @abc.abstractmethod
    def send_alert(self):
        pass

    @abc.abstractmethod
    def send_resolve(self):
        pass


class HttpPostJsonReceiver(Receiver):
    """
    Makes an HTTP POST to a specific URL
    """
    def __init__(self, url, headers=None, logger=None, alert_dict=None, resolve_dict=None, timeout=15):
        """
        Initialise receiver

        param url str
        param headers dict
        param logger logger
        param alert_dict dict
        param resolve_dict dict
        param timeout int number of seconds
        """
        self.logger = logger or logging.getLogger(__name__)
        self.set_url(url)
        self.set_headers(headers)
        self.set_alert_dict(alert_dict)
        self.set_resolve_dict(resolve_dict)
        self.set_timeout(timeout)

    def get_url(self):
        """
        Get URL build from a tuple using urllib.parse.urlunparse
        """
        return urlunparse(self.url)

    def set_url(self, url):
        """
        Set URL as a tuple returned by urllib.parse.urlparse
        param url str
        """
        try:
            parsed_tuple = urlparse(url)
        except ValueError as e:
            self.logger.error("Error parsing url in receiver")

        self.url = parsed_tuple

    def get_headers(self):
        return self.headers

    def set_headers(self, headers):
        """
        Sets headers to be added when sending an alert/resolve
        param headers dict
        """
        self.headers = headers

    def get_alert_dict(self):
        return self.alert_dict

    def set_alert_dict(self, alert_dict):
        """
        Sets payload to be added when sending an alert/resolve
        param alert_dict dict
        """
        if not alert_dict:
            alert_dict = {}
        self.alert_dict = alert_dict

    def get_resolve_dict(self):
        return self.resolve_dict

    def set_resolve_dict(self, resolve_dict):
        """
        Sets payload to be added when sending an alert/resolve
        param resolve_dict dict
        """
        if not resolve_dict:
            resolve_dict = {}
        self.resolve_dict = resolve_dict

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        """
        Sets timeout seconds for http client
        param timeout int seconds
        """
        self.timeout = timeout

    def do_post(self, req):
        """
        Makes post request to receiver.
        param req urllib.request.Request
        """
        # append headers
        req.add_header('Content-Type', 'application/json')
        if self.get_headers():
            for header_name, header_value in self.get_headers().items():
                req.add_header(header_name, header_value)

        # make http call
        try:
            self.logger.debug("POST request sent to HttpPostReceiver with data : {}".format(req.data.decode('utf-8')))
            res = request.urlopen(req, timeout=self.get_timeout())
        except (HTTPError, URLError) as e:
            self.logger.error("HTTP error: {}".format(e))
        except timeout as e:
            self.logger.error("Timeout Error: {}".format(e))
        except Exception as e:
            self.logger.error("Unknown error: {}".format(e))

    def send_alert(self):
        """
        Sends an alert POSTing data as json
        """
        try:
            payload_string = json.dumps(self.get_alert_dict())
            payload_bytes = payload_string.encode('utf-8')
        except ValueError as e:
            self.logger.error("Error parsing json payload")

        req = request.Request(self.get_url(), data=payload_bytes)
        self.do_post(req)


    def send_resolve(self):
        """
        Sends a resolve POSTing data as json
        """
        try:
            payload_string = json.dumps(self.get_resolve_dict())
            payload_bytes = payload_string.encode('utf-8')
        except ValueError as e:
            self.logger.error("Error parsing json payload")

        req = request.Request(self.get_url(), data=payload_bytes)
        self.do_post(req)
