import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils

class Tracking_Identifier(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()
        
    def verify_fhir_tracking_id(self, fhir_contents):
        
        failures = []
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target == '246501002':
                pass
            else:
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    if 'Tracking Identifier' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                        tracking_id_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                        tracking_id_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                        try:
                            assert tracking_id_code == "112039", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
                            print(f"Tracking Identifier code matches with requirement for {target} observation")
                            assert tracking_id_display == "Tracking Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"
                            print(f"Tracking Identifier code matches with requirement for {target} observation")
                            with allure.step(f"Verification of Tracking Identifier for {target} observation"):
                                allure.attach(f"Tracking Identifier code from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID code: 112039, From FHIR.json Tracking ID code: {tracking_id_code}", f"Verification of Tracking Identifier code for {target} observation against requirement", allure.attachment_type.TEXT)
                                allure.attach(f"Tracking Identifier display from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID display: Tracking Identifier, From FHIR.json Tracking ID display: {tracking_id_display}", f"Verification of Tracking Identifier display for {target} observation against requirement", allure.attachment_type.TEXT)
                        except AssertionError:
                            failures.append(target)
                            
        
        if failures:
            print(f"Tracking Identifer code/display mismatch is observed in following observations : {failures}")
            with allure.step(f"Tracking Identifer code/display mismatch is observed in FHIR.json"):
                allure.attach(f"Tracking Identifier code/display from FHIR does not match with the requirement for following observations : {failures}",
                              f"Tracking Identifer code/display mismatch is observed in FHIR.json", allure.attachment_type.TEXT)
            pytest.fail(f"Test failed due to Tracking Identifier from FHIR.json does not match with requirement")
            
            
    
    
    def verify_fhir_tracking_uid(self, fhir_contents):
        
        failures = []
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target == '246501002':
                pass
            else:
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    if 'Tracking Unique Identifier' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                        tracking_uid_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                        tracking_uid_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                        try:
                            assert tracking_uid_code == "112040", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
                            print(f"Tracking Unique Identifier code matches with requirement for {target} observation")
                            assert tracking_uid_display == "Tracking Unique Identifier", f"Tracking Unique Identifier display text of {target} observation from FHIR report does not match the requirement"
                            print(f"Tracking Unique Identifier display text matches with requirement for {target} observation")
                            with allure.step(f"Verification of Tracking Unique Identifier for {target} observation"):
                                allure.attach(f"Tracking Unique Identifier code from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID code: 112040, From FHIR.json Tracking ID code: {tracking_uid_code}", f"Verification of Tracking Unique Identifier code for {target} observation against requirement", allure.attachment_type.TEXT)
                                allure.attach(f"Tracking Unique Identifier display from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID display: Tracking Unique Identifier, From FHIR.json Tracking ID display: {tracking_uid_display}", f"Verification of Tracking Identifier display for {target} observation against requirement", allure.attachment_type.TEXT)
                        except AssertionError:
                            failures.append(target)
                            
        
        if failures:
            print(f"Tracking Unique Identifer code/display mismatch is observed in following observations : {failures}")
            with allure.step(f"Tracking Unique Identifer code/display mismatch is observed in FHIR.json"):
                allure.attach(f"Tracking Unique Identifier code/display from FHIR does not match with the requirement for following observations : {failures}",
                              f"Tracking Unique Identifer code/display mismatch is observed in FHIR.json", allure.attachment_type.TEXT)
            pytest.fail(f"Test failed due to Tracking Unique Identifier from FHIR.json does not match with requirement")
            
            

                        
    def extract_fhir_tracking_id(self,fhir_input):
        try:
            for observation in range(3,len(fhir_input['contained'])):
                target = (fhir_input["contained"][observation]["code"]["coding"][0]["code"])
                if target == '246501002':
                    pass
                else:
                    for each in range(len(fhir_input["contained"][observation]["component"])):
                        if 'Tracking Identifier' in fhir_input["contained"][observation]["component"][each]["code"]["coding"][0].values():
                            tracking_id_code = fhir_input["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                            tracking_id_display = fhir_input["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                            yield tracking_id_code
        except Exception as e:
            print(f"Error extracting Study UID: {e}")
            return None
    
    
    
    
    def is_tracking_identifier_present(self,fhir_json_data):
        fhir_contents = fhir_json_data
        tracking_identifier_presenence = True
        tracking_id_absence = []
        for observation in range(3, len(fhir_contents['contained'])):
            
            target = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
            if target == '246501002':
                pass
            else:
                components_data = []
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    # Extract the 'coding' list from the current component
                    coding_list = fhir_contents["contained"][observation]["component"][each]["code"].get("coding", [])
                    for entry in coding_list:
                        components_data.extend(list(entry.values()))
                if "Tracking Identifier" in components_data:
                    components_data = []
                else:
                    tracking_identifier_presenence = False
                    tracking_id_absence.append(target)
                    
                    
        if tracking_identifier_presenence:
            print("Tracking Idenifier component is present for all the observations in FHIR.json")
            with allure.step(f"Verification of presence of Tracking Identifier component for all the observations in FHIR.json"):
                allure.attach(f"Tracking Identifier component is present for all the observations in FHIR.json", 
                    f"Tracking Identifier component is present for all the observations in FHIR.json", allure.attachment_type.TEXT)
        else:
            print(f"Tracking Identifier component is not present for following observations : {tracking_id_absence}")
            with allure.step(f"Verification of presence of Tracking Identifier component for all the observations in FHIR.json"):
                allure.attach(f"Tracking Identifier component is absent for following observations in FHIR.json : {tracking_id_absence}", 
                    f"Tracking Identifier component is absent for following observations in FHIR.json", allure.attachment_type.TEXT)
            pytest.fail(f"Test Failed since Tracking Identifier is not present for following observations in FHIR.json : {tracking_id_absence}")
        
        
        
    def is_tracking_uid_present(self,fhir_json_data):
        fhir_contents = fhir_json_data
        tracking_uid_presenence = True
        tracking_uid_absence = []
        for observation in range(3, len(fhir_contents['contained'])):
            
            target = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
            if target == '246501002':
                pass
            else:
                components_data = []
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    # Extract the 'coding' list from the current component
                    coding_list = fhir_contents["contained"][observation]["component"][each]["code"].get("coding", [])
                    for entry in coding_list:
                        components_data.extend(list(entry.values()))
                if "Tracking Unique Identifier" in components_data:
                    components_data = []
                else:
                    tracking_uid_presenence = False
                    tracking_uid_absence.append(target)
                    
        if tracking_uid_presenence:
            print("Tracking Unique Idenifier component is present for all the observations in FHIR.json")
            with allure.step(f"Verification of presence of Tracking Unique Identifier component for all the observations in FHIR.json"):
                allure.attach(f"Tracking Unique Identifier component is present for all the observations in FHIR.json", 
                    f"Tracking Unique Identifier component is present for all the observations in FHIR.json", allure.attachment_type.TEXT)
        else:
            print(f"Tracking Unique Identifier component is not present for following observations : {tracking_uid_absence}")
            with allure.step(f"Verification of presence of Tracking Unique Identifier component for all the observations in FHIR.json"):
                allure.attach(f"Tracking Unique Identifier component is absent for following observations in FHIR.json : {tracking_uid_absence}", 
                    f"Tracking Unique Identifier component is absent for following observations in FHIR.json", allure.attachment_type.TEXT)
            pytest.fail(f"Test Failed since Tracking Unique Identifier component is not present for following observations in FHIR.json : {tracking_uid_absence}")
        
        