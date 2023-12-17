import requests
from .config_reader import Config


class CoreAPIUtils(object):

    def __init__(self):
        self.config = Config()

    def get_api_request(self, url, param=None):
        """
        Method to perform GET request.
        :param url: URL for GET request.
        :return:  Returns the response of GET request.
        """
        try:
            head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            if param is None:
                response = requests.get(url, headers=head)
                return response
            elif param is not None:
                response = requests.get(url, headers=head, params=param)
                return response
        except Exception as exc:
            # self.exception_util.generic_exception("Error occurred during api get", exc)
            raise

    def post_api_request(self, url, api_data):
        """
        Method for POST api request.
        :param url: URL for POST request.
        :param api_data: API data that is required to POST
        :return: Returns the response from the POST request.
        """
        try:
            head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(url=url, data=api_data, headers=head)
            return response
        except Exception as exc:
            # self.exception_util.generic_exception("Error occurred during api post ", exc)
            raise

