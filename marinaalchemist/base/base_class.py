import pytest



@pytest.mark.usefixtures('setup')
class BaseClass(object):
    config = None
    logger = None
    allure_util = None
    fhir_json = None
    model_output_json = None
    fhir_excel = None
    url_util = None
    docker_util = None
    generic_util = None
    fhir_util = None
    dicom_util = None
    observation_df = None
    non_observation_df = None
    fhir_input_path = None
    fhir_output_path = None
    fhir_contents = None
    exception_utils = None
    