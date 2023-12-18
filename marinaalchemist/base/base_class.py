import pytest



@pytest.mark.usefixtures('setup')
class BaseClass(object):
    config = None
    logger = None
    allure_util = None
    fhir_json = None
    fhir_excel = None
    url_util = None
    docker_util = None
    generic_util = None
    observation_df = None
    non_observation_df = None

