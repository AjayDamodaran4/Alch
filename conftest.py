import pytest
import json, os, allure
from marinaalchemist import AllureReport, ExcelUtils, Config, DockerUtils, GenericUtils, DicomUtils, ExceptionUtils
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
    request.cls.generic_util = GenericUtils()
    request.cls.observation_df = ExcelUtils().excel_to_df(fhir_requirement_path, observation_excel_sheet)
    request.cls.non_observation_df = ExcelUtils().excel_to_df(fhir_requirement_path, non_observation_excel_sheet)
    request.cls.fhir_json = read_fhir_json()
    request.cls.model_output_json = read_model_output_json()
    request.cls.docker_util = DockerUtils()
    request.cls.dicom_util = DicomUtils()
    request.cls.cxr_req = read_cxr_req()
    request.cls.exception_utils = ExceptionUtils()
    yield
    print("test closed!!!")


def read_fhir_json():
    fhir_path = Config().get_value_of_config_key("fhir_json_path")
    with open(fhir_path, 'r') as file: 
        fhir_contents = json.load(file)
    return fhir_contents

def read_cxr_req():
    cxr_req_path = Config().get_value_of_config_key("cxr_req")
    with open(cxr_req_path, 'r') as file: 
        cxr_req = json.load(file)
    return cxr_req

def read_model_output_json():
    model_output_json_path = Config().get_value_of_config_key("model_output_json_path")
    with open(model_output_json_path, 'r') as file: 
        model_output_contents = json.load(file)
    return model_output_contents

# @pytest.fixture(scope="class", params = ["input_path_TC_1","input_path_TC_2","input_path_TC_3","input_path_TC_4","input_path_TC_5",
#                                          "input_path_TC_6","input_path_TC_7","input_path_TC_8"])
@pytest.fixture(scope="class", params = ["input_path_TC_1"])
def container_auto(request):

    input_path_param = request.param
    input_path = Config().get_value_of_test_input_key(input_path_param)
    output_path = GenericUtils().output_folder_generator()
    DockerUtils().container_autorun(input_path=input_path, output_path=output_path)
    DockerUtils().check_container_logs()
    request.cls.fhir_input_path = input_path
    request.cls.fhir_output_path = output_path
    Config().update_value_of_config_key("fhir_json_path",output_path)
    
    # Check if "Annalise-cxr-FHIR.json" is available in the output_path
    fhir_file_path = os.path.join(output_path, "Annalise-cxr-FHIR.json")
    

    if os.path.exists(fhir_file_path):
        request.cls.fhir_contents = GenericUtils().parse_json_file(fhir_file_path)
        
    else:
        # If the JSON file is not available, provide a message
        raise FileNotFoundError(f"Annalise-cxr-FHIR.json not available in the output_path")
    yield
    with allure.step(f"Shutting down the container! Output files are stored at"):
        allure.attach(f"Output manifests for the processed study is stored at path : {request.cls.fhir_output_path}",\
                      f"Output manifests location path", allure.attachment_type.TEXT)
