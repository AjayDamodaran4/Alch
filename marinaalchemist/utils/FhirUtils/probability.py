import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils

"""
TO DO

check negative scenarios for verify_probability method.

"""




class Probability_Qualifier(object):
    
    def __init__(self): 
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()    
        self.fda_findings = ["pleural_effusion", "pneumothorax", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax", "RDES254", "RDES230", "RDES228"]
        self.group_findings =["RDES225","RDES44"]
    
    def find_component_index_for_probability(self,components):
        """
        Find the index of the dictionary in the components list that contains a value from the test list.

        Args:
        - components (list): A list of dictionaries to search through.
        - probability_details (list): A list of values to search for.

        Returns:
        - int: The index of the dictionary containing a value from the probability_details list, or -1 if no match is found.
        """
        
        probability_details = ['Probably', 'probably', 'Finding Probability', 'RID33', '2931005', '90090302']

    # Iterate through each dictionary in the components
        for index, value in enumerate(components):
            # Iterate through the 'coding' list within the 'code' key of the dictionary
            for coding in value.get("code", {}).get("coding", []):
                # Check if the 'display' value is present in the test list
                if coding.get("display") in probability_details:
                    # If a match is found, return the index of the dictionary
                    return index
    
    # If no match is found, return -1
        return -1
    
    

           
    def verify_probability(self,fhir_contents=None,system=None):
        args_lower = [arg.lower() for arg in system]
        nuance_present = "nuance" in args_lower
        snomed_present = "snomed" in args_lower
        radlex_present = "radlex" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        probability_systems_failure = []
        probability_absence = []
        probability_presence = []
        valid_args = {"row", "us", "nuance", "snomed", "radlex"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        
        if region_ROW and region_US:
            raise ValueError("Two regionofInstance arguments detected. Only one regionOfInstance is supported.")
        
        if not (snomed_present or radlex_present or nuance_present):
            raise ValueError("Any one of Probability coding systems (snomed/nuance/radlex) must be specified as argument")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
        probability_systems = {
                            'snomed_probability' : {
            "system": "http://snomed.info/sct",
            "code": "2931005",
            "display": "Probably"
            },
                            'nuance_probability' : {
            "system": "http://nuancepowerscribe.com/ai",
            "code": "90090302",
            "display": "Finding Probability"
            },
                            'radlex_probability' : {
            "system": "http://radlex.org",
            "code": "RID33",
            "display": "probably"
            }
                            }
    
        applicable_systems_mapping = {'snomed_probability' : snomed_present,
            'nuance_probability' : nuance_present,
            'radlex_probability' : radlex_present}
        
        applicable_systems = [probability_systems.get(key) for key,value in applicable_systems_mapping.items() if value]
        
        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002":
                continue
                
            if region_US and not region_ROW:
                if observation_name in self.fda_findings or observation_name in self.group_findings:
                    components = fhir_contents["contained"][observation]["component"]
                    probability_component_index  = self.find_component_index_for_probability(components)
                    try:
                        assert probability_component_index == -1, f"Probability Qualifier component are available for {observation_name} observation which is not expected."
                    except AssertionError:
                        probability_presence.append(observation_name)
                        
                    continue
            components = fhir_contents["contained"][observation]["component"]
            probability_component_index  = self.find_component_index_for_probability(components)
            if probability_component_index == -1:
                probability_absence.append(observation_name)

            else:
                probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
                try:
                    assert applicable_systems == probability_component_fhir, f"write correct error msg"
                    print(f"probability qualifier of {observation_name} matches as per requirement")
                except AssertionError:
                    probability_systems_failure.append(observation_name)
                    
                    
        if probability_systems_failure or probability_presence or probability_absence :
            error_messages = []

            if probability_systems_failure:
                error_messages.append(f"Probability Qualifier coding systems present in FHIR.json does not match with requirement or with coding systems that's passed as argument for test case for following observations: {probability_systems_failure}")
            if probability_presence:
                error_messages.append(f"Probability Qualifier component are available for following observations which is not expected : {probability_presence}.")
            if probability_absence:
                error_messages.append(f"Probability Qualifier component are NOT available for following observation which is not expected : {probability_absence}")
            
            if error_messages:
                print("\n".join(error_messages))
                return False
            
        else:
            return True
                
    
    
    def verify_probability_score(self,fhir_contents=None, model_output_contents=None,system=None):
        args_lower = [arg.lower() for arg in system]
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        score_mismatch = []
        probability_valueQuantity_mismatch = []
        probability_absence = []
        observation_not_found = []
        valid_args = {"row", "us"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        
        if region_ROW and region_US:
            raise ValueError("Two regionofInstance arguments detected. Only one regionOfInstance is supported.")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")

        
        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002" or observation_name=="intercostal_drain":
                continue #check why "intercostal_drain" not listed in model output
            if region_US and not region_ROW:
                if observation_name in self.fda_findings or observation_name in self.group_findings:
                    continue
            components = fhir_contents["contained"][observation]["component"]
            probability_component_index  = self.find_component_index_for_probability(components)
            
            try:
                assert probability_component_index != -1
            except AssertionError:
                probability_absence.append(observation_name)
                continue
            

            probability_score_component_fhir = components[probability_component_index].get("valueQuantity", {})
            
            for key, value in self.cxr_mappings.items():
                if observation_name in (key, value):
                    probability_mapping_code = key
                    probability_score_model_output = model_output_contents.get('cxr_value',{}).get('classifications',{}).get('groups',{}).get(probability_mapping_code,{})['present']
                    
                    
                    try:
                        assert probability_score_model_output*100 == probability_score_component_fhir["value"],f"Probability score from model output does not match with FHIR.json for {observation_name} observation"
                        print(f"Probability score from model output matches with FHIR.json for {observation_name} observation")
                    except AssertionError:
                        score_mismatch.append(observation_name)
                        continue
                    
                    
                    probability_score_req = {
                                                "value": probability_score_model_output * 100,
                                                "unit": "percent",
                                                "system": "http://unitsofmeasure.org"
                                            }
                    
                    
                    try:
                        assert probability_score_req == probability_score_component_fhir, f"Probability components - valueQuantity's keys/values does not match with requirement for {observation_name} observation"
                        print(f"Probability components - valueQuantity's keys & values matches with FHIR.json for {observation_name} observation")
                    except AssertionError:
                        probability_valueQuantity_mismatch.append(observation_name)
                else:
                    observation_not_found.append(observation_name)
        
        
        if probability_valueQuantity_mismatch or score_mismatch or probability_absence :
            error_messages = []

            if probability_valueQuantity_mismatch:
                error_messages.append(f"Probability components - valueQuantity's keys/values does not match with requirement for following observations : {probability_valueQuantity_mismatch}")
            if score_mismatch:
                error_messages.append(f"Probability score from model output does not match with FHIR.json for following observations : {score_mismatch}")
            if probability_absence:
                error_messages.append(f"Probability Qualifier not present in FHIR.json for following observation : {probability_absence}")
            if observation_not_found:
                error_messages.append(f"Observation code from FHIR.json not found in CXR supported observation coding system for following observations: {observation_not_found}")
            
            
            
            if error_messages:
                print("\n".join(error_messages))
                return False
        
        else:
            return True
            
                        
