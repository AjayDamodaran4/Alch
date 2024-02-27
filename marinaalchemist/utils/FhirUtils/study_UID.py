import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils


class Study_Identifier(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()
        
    
    def verify_study_uid(self, dicom_study_uid, fhir_contents):
        
        failures = []
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target == '246501002':
                pass
            else:
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    if 'Study Instance UID' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                        study_uid = fhir_contents["contained"][observation]["component"][each]["valueString"]
                        if dicom_study_uid == study_uid:
                            pass
                        else:
                            failures.append(target)
                            
                        
        if failures:
            print("Study UID from DICOM metadata does not match with Study UID from FHIR.json")
            with allure.step(f"Verification of Study Instance UID match with Study Instance UID from DICOM metadata"):
                allure.attach(f"Study Instance UID displayed in following observations of FHIR.json does not match \
                     with Study Instance UID from DICOM metadatav : {failures}", 
                    f"Study Instance UID displayed in following observations of FHIR.json does not match for following observations", allure.attachment_type.TEXT)
            pytest.fail(f"Test failed since Study Instance UID displayed in following observations of FHIR.json does not match \
                     with Study Instance UID from DICOM metadatav : {failures}")
        else:
            print("Study UID from DICOM metadata matches match with Study UID from FHIR.json")
            with allure.step(f"Verification of Study Instance UID matches with Study Instance UID from DICOM metadata"):
                allure.attach(f"Study Instance UID displayed in all the observations of FHIR.json matches with Study Instance UID from DICOM metadata", 
                    f"Verification of Study Instance UID matches with Study Instance UID from DICOM metadata", allure.attachment_type.TEXT)

            
    
    def is_study_uid_present(self,fhir_json_data):
        fhir_contents = fhir_json_data
        study_uid_presenence = True
        study_uid_absence = []
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
                if "Study Instance UID" in components_data:
                    components_data = []
                else:
                    study_uid_presenence = False
                    study_uid_absence.append(target)
                    
        if study_uid_presenence:
            print("Study Instance UID is present for all the observations in FHIR.json")
            with allure.step(f"Verification of presence of Study Instance UID component for all the observations in FHIR.json"):
                allure.attach(f"Study Instance UID component is present for all the observations in FHIR.json", 
                    f"Study Instance UID component is present for all the observations in FHIR.json", allure.attachment_type.TEXT)
        else:
            print(f"Study Instance UID is not present for following observations : {study_uid_absence}")
            with allure.step(f"Verification of presence of Study Instance UID component for all the observations in FHIR.json"):
                allure.attach(f"Study Instance UID component is absent for following observations in FHIR.json : {study_uid_absence}", 
                    f"Study Instance UID component is absent for following observations in FHIR.json", allure.attachment_type.TEXT)
            pytest.fail(f"Test Failed since Study Instance UID is not present for following observations in FHIR.json : {study_uid_absence}")
        