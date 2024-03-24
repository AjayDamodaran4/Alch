import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils

class Tracking_ID(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()
    
    def find_component_index(self,key,components):

    # Iterate through each dictionary in the components
        for index, value in enumerate(components):
            # Iterate through the 'coding' list within the 'code' key of the dictionary
            for coding in value.get("code", {}).get("coding", []):
                # Check if the 'display' value is present in the test list
                if coding.get("display") == key:
                    # If a match is found, return the index of the dictionary
                    return index
    
    # If no match is found, return -1
        return -1
    
    def verify_tracking_ID(self, fhir_contents):
        tracking_ID_component_absence = []
        tracking_ID_mismatch =[]
        tracking_ID_req = {
                            "system": "http://dicom.nema.org/resources/ontology/DCM",
                            "code": "112039",
                            "display": "Tracking Identifier"
                            }
        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002":
                continue
            else:
                components = fhir_contents["contained"][observation]["component"]
                tracking_ID_component_index = self.find_component_index("Tracking Identifier",components=components)
                if tracking_ID_component_index!=-1:
                    tracking_ID_component_FHIR = fhir_contents["contained"][observation]["component"][tracking_ID_component_index]["code"]["coding"][0]
                    try:
                        assert tracking_ID_req == tracking_ID_component_FHIR
                    except AssertionError:
                        tracking_ID_mismatch.append(observation_name)
                else:
                    tracking_ID_component_absence.append(observation_name)
                    
            
        if tracking_ID_component_absence or tracking_ID_mismatch :
            error_messages = []

            if tracking_ID_component_absence:
                error_messages.append(f"Tracking ID component unavailable in FHIR.json for following observations: {tracking_ID_component_absence}")
            if tracking_ID_mismatch:
                error_messages.append(f"Tracking ID component in FHIR.json does not match with requirements for following observations : {tracking_ID_mismatch}.")
            
            if error_messages:
                print("\n".join(error_messages))
                return False
            
        else:
            return True
        
        
        
        
    
    def verify_tracking_UID(self, fhir_contents):
        tracking_UID_component_absence = []
        tracking_UID_mismatch =[]
        tracking_UID_req = {
                            "system": "http://dicom.nema.org/resources/ontology/DCM",
                            "code": "112040",
                            "display": "Tracking Unique Identifier"
                        }
        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002":
                continue
            else:
                components = fhir_contents["contained"][observation]["component"]
                tracking_UID_component_index = self.find_component_index("Tracking Unique Identifier",components=components)
                if tracking_UID_component_index!=-1:
                    tracking_UID_component_FHIR = fhir_contents["contained"][observation]["component"][tracking_UID_component_index]["code"]["coding"][0]
                    try:
                        assert tracking_UID_req == tracking_UID_component_FHIR
                    except AssertionError:
                        tracking_UID_mismatch.append(observation_name)
                        
                    assert components[tracking_UID_component_index]["valueString"][:22] == "1.2.36.1.2001.1005.78."
                    print(components[tracking_UID_component_index]["valueString"][:22])
                else:
                    tracking_UID_component_absence.append(observation_name)
                    
            
        if tracking_UID_component_absence or tracking_UID_mismatch :
            error_messages = []

            if tracking_UID_component_absence:
                error_messages.append(f"Tracking UID component unavailable in FHIR.json for following observations: {tracking_UID_component_absence}")
            if tracking_UID_mismatch:
                error_messages.append(f"Tracking UID component in FHIR.json does not match with requirements for following observations : {tracking_UID_mismatch}.")
            
            if error_messages:
                print("\n".join(error_messages))
                return False
            
        else:
            return True