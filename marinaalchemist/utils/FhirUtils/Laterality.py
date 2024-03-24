import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils
"""
TO DO
1. try new logic similar to probability
2. what if no laterality is present in FHIR. say the findings presnet in FHIR.json are out of OPT-CLI_002 laterality group.

"""

class Laterality(object):
    
    def __init__(self):
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()
        self.fda_findings = ["pleural_effusion", "pneumothorax", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax", "RDES254", "RDES230", "RDES228"]
        self.group_findings =["RDES225","RDES44"]
        self.laterality_mismatch = []
        
    def expected_laterality_component(self, observation_name, model_output_contents):
        laterality_dict = model_output_contents['cxr_value']['study_laterality']['findings'][observation_name]['values']
        laterality = max(laterality_dict, key=laterality_dict.get)
        laterality_value = max(laterality_dict.values()) * 100
        
        expected_laterality_component = {
                                            "code": {
                                                "coding": [
                                                {
                                                    "system": "http://snomed.info/sct",
                                                    "code": self.cxr_req.get('laterality_codes',{}).get(self.cxr_req.get(laterality, None)),
                                                    "display": self.cxr_req.get(laterality, None)
                                                }
                                                ]
                                            },
                                            "valueQuantity": {
                                                "value": laterality_value,
                                                "unit": "percent",
                                                "system": "http://unitsofmeasure.org",
                                                "code": "%"
                                            }
                                            }
        
        return expected_laterality_component

    def find_component_index_for_laterality(self,components):
        """
        Find the index of the dictionary in the components list that contains a value from the test list.

        Args:
        - components (list): A list of dictionaries to search through.
        - laterality_details (list): A list of values to search for.

        Returns:
        - int: The index of the dictionary containing a value from the laterality_details list, or -1 if no match is found.
        """
        
        laterality_details = ['right', 'right lateral', 'left', 'left lateral', 'bilateral', '24028007', '7771000', '51440002']

    # Iterate through each dictionary in the components
        for index, value in enumerate(components):
            # Iterate through the 'coding' list within the 'code' key of the dictionary
            for coding in value.get("code", {}).get("coding", []):
                if coding.get("display") is not None or coding.get("code") is not None:
                    # Check if the 'display' value is present in the test list
                    if coding.get("display").lower() in laterality_details or coding.get("code").lower() in laterality_details:
                        # If a match is found, return the index of the dictionary
                        return index
    
    # If no match is found, return -1
        return -1
    
    
    
    def extract_fhir_laterality_component(self,fhir_contents, observation_name, observation):
        if observation_name == "246501002":
            pass
        else:
            observation_components = fhir_contents["contained"][observation]["component"]
            laterality_component_index = self.find_component_index_for_laterality(observation_components)
            laterality_component_fhir = observation_components[laterality_component_index]
            return laterality_component_fhir
        
        
    
    def assert_laterality(self, fhir_contents, model_output_contents, observation_name, observation):
        expected_laterality_component = self.expected_laterality_component(observation_name, model_output_contents)
        fhir_laterality_component = self.extract_fhir_laterality_component(fhir_contents, observation_name, observation)
        for expected, actual in zip(expected_laterality_component.items(), fhir_laterality_component.items()):
            try:
                assert expected == actual, f"Laterality item {actual} does not match with requirement {expected} for {observation_name} observation"
            except AssertionError:
                self.laterality_mismatch.append(observation_name)
                print(f"Laterality item {actual} does not match with requirement {expected} for {observation_name} observation")
            


    def verify_laterality(self,fhir_contents=None, model_output_contents=None,system=None):
        if fhir_contents is None or model_output_contents is None or system is None:
            print("arguments connot be None")
            pytest.fail("arguments cannot be None for verify_laterality")
        args_lower = [arg.lower() for arg in system]
        
        
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        
        valid_args = {"row", "us"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")

        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")

        laterality_absence = []
        observation_not_found = []
        laterality_presence = []
        excel_util = ExcelUtils()
        opt_cli_laterality = excel_util.opt_cli_laterality()
        
        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002":
                continue
            else:
                observation_components = fhir_contents["contained"][observation]["component"]
            
            if region_ROW and not region_US:
                if observation_name in opt_cli_laterality:
                    try:
                        assert self.find_component_index_for_laterality(observation_components) != -1
                        self.assert_laterality(fhir_contents, model_output_contents, observation_name, observation)
                        print(f"laterality details match as per requirement for {observation_name} observation.")
                    except AssertionError:
                        laterality_absence.append(observation_name)
                        continue
                    
                else:
                    try:
                        assert any(observation_name == key or observation_name == value for key, value in self.cxr_mappings.items())
                    except AssertionError:
                        observation_not_found.append(observation_name)
                        continue
                    
                    
                    try:
                        assert self.find_component_index_for_laterality(observation_components) == -1
                        print(f"Laterality details not present in {observation_name} observation. This is expected behaviour.")
                    except AssertionError:
                        print(f"FAIL: Laterality details are available in {observation_name} observation which is not expected.")
                        laterality_presence.append(observation_name)

            # US region scenarios should be handled. Did not handle now since model_output.json not available for US region
            elif region_US and not region_ROW:
                if observation_name not in (self.fda_findings + self.group_findings):
                    self.assert_laterality(fhir_contents, model_output_contents, observation_name, observation)
                else:
                    try:
                        assert self.find_component_index_for_laterality(observation_components) == -1
                    except AssertionError:
                        print(f"Laterality details are available in {observation_name} observation which is not expected.")
        
        
        
        
        if observation_not_found or self.laterality_mismatch or laterality_absence or laterality_presence:
            error_messages = []

            if observation_not_found:
                error_messages.append(f"Observation code from FHIR.json not found in CXR supported observation coding system for following observations: {observation_not_found}")
            if self.laterality_mismatch:
                error_messages.append(f"Laterality Qualifier from FHIR.json does not match with requirement for following observations: {self.laterality_mismatch}")    
            if laterality_absence:
                error_messages.append(f"Laterality Qualifier is not available in FHIR.json for following observations: {laterality_absence}")    
            if laterality_presence:
                error_messages.append(f"Laterality Qualifier is present for following observations: {laterality_presence} which is not expected. These observation doesnt belong to OPT-CLI-002 laterality group") 
            
            if error_messages:
                print("\n".join(error_messages))
                return False
        else:
            return True
            



