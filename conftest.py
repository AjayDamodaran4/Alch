import pytest
import json
from marinaalchemist import AllureReport, ExcelUtils, Config
from marinaalchemist.utils.generic_utils import GenericUtils
import pandas as pd

fhir_requirement_path = Config().get_value_of_config_key("excel_file_path")
observation_excel_sheet = 'Codes - Obs'
non_observation_excel_sheet = 'Codes - Non Obs'
compose_file = Config().get_value_of_config_key("compose_file_path")


@pytest.fixture(scope="class")
def setup(request):
    print("setup")
    request.cls.allure_util = AllureReport(None)
    request.cls.config = Config()
    request.cls.generic_util = GenericUtils().output_folder_generator()
    request.cls.observation_df = ExcelUtils().excel_to_df(fhir_requirement_path, observation_excel_sheet)
    request.cls.non_observation_df = ExcelUtils().excel_to_df(fhir_requirement_path, non_observation_excel_sheet)
    request.cls.fhir_json = read_fhir_json()
    yield
    print("test closed!!!")


def read_fhir_json():
    fhir_path = Config().get_value_of_config_key("fhir_json_path")
    with open(fhir_path, 'r') as file:  # context manager
        fhir_contents = json.load(file)
    return fhir_contents
