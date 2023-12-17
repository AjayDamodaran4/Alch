import pytest
from marinaalchemist import DockerUtils


@pytest.mark.usefixtures('setup')
class BaseClass(object):
    config = None
    logger = None
    allure_util = None
    fhir_json = None
    fhir_excel = None
    url_util = None
    generic_util = None
    observation_df = None
    non_observation_df = None

    def __init__(self):
        self.docker_utils = DockerUtils()
