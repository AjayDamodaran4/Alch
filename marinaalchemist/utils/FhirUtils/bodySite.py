import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils


class bodySite(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()

    def verify_bodysite(self, fhir_contents=None, system=None):
        if fhir_contents is None or system is None:
            print("arguments connot be None")
            pytest.fail("arguments cannot be None for verify_bodysite")
        args_lower = [arg.lower() for arg in system]

        region_ROW = "row" in args_lower
        snomed_present = "snomed" in args_lower
        radlex_present = "radlex" in args_lower
        bodySite_mismatch = []
        bodySite_absence = []
        
        valid_args = {"row", "snomed","radlex"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

        if not (region_ROW):
            raise ValueError("regionOfInstance - 'ROW' argument must be specified")

        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
        
        
        for observation in range(3,len(fhir_contents['contained'])):
            expected_bodysite_component = []
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002":
                continue
            if radlex_present:
                radlex_code = self.cxr_req["ROW"][observation_name][0]["bodySite_Radlex.code"]
                radlex_display = self.cxr_req["ROW"][observation_name][0]["bodySite_Radlex.display"]
                bodySite_radlex_block = {
                                            "system": "http://radlex.org",
                                            "code": radlex_code,
                                            "display": radlex_display
                                        }
                expected_bodysite_component.append(bodySite_radlex_block)
            if snomed_present and observation_name!="spine_wedge_fracture":
                snomed_code = self.cxr_req["ROW"][observation_name][0]["bodySite_Snomed.code"]
                snomed_display = self.cxr_req["ROW"][observation_name][0]["bodySite_Snomed.display"]
                bodySite_snomed_block = {
                                            "system": "http://snomed.info/sct",
                                            "code": snomed_code,
                                            "display": snomed_display
                                        }
                expected_bodysite_component.append(bodySite_snomed_block)
            
            try:
                fhir_bodySite_component = fhir_contents["contained"][observation]["bodySite"]["coding"]
            except KeyError:
                bodySite_absence.append(observation_name)
                continue
            
            
            try:
                assert expected_bodysite_component == fhir_bodySite_component
            except AssertionError:
                bodySite_mismatch.append(observation_name)
                
                
                
        if bodySite_mismatch or bodySite_absence:
            error_messages = []

            if bodySite_mismatch:
                error_messages.append(f"bodySite component in FHIR.json does not match with requirement or with coding systems that's passed as argument for test case for following observations: {bodySite_mismatch}")
            
            if bodySite_absence:
                error_messages.append(f"bodySite component not available in FHIR.json for following observations: {bodySite_absence}")
            
            if error_messages:
                print("\n".join(error_messages))
                return False
            
        else:
            return True
                
                
            
            
               
                
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    # def verify_snomed_code(self, fhir_contents):
    #     self.cxr_req = conftest.read_cxr_req()
    #     failures = []
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         # bodySite_snomed_code_as_per_req = self.cxr_req[target][0]["bodySite_Snomed.code"]
            
    #         if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
    #             pass
            
    #         elif target == "RDES230": # This is ignored from verifying as snomed is not applicable for RDES230 observation
    #             pass
            
    #         elif target == "RDES225": # This block verifies the bodySite of Chest Radiograph Pulmonary Nodules observation
    #             display_value = None
                
    #             if len(fhir_contents["contained"][observation]["component"]) == 4 :
    #                 display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
    #             elif len(fhir_contents["contained"][observation]["component"]) == 5 :
    #                 display_value = fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"]
                
    #             if display_value is not None and display_value not in ['absent', 'focal', 'multifocal', 'diffuse lower', 'diffuse upper']:
    #                 raise ValueError(f"Unexpected display value: {display_value}")

    #             key = None
    #             sub_key = None

    #             if display_value in ['absent', 'focal']:
    #                 key = 1
    #                 sub_key = "focal_airspace_opacity"
    #                 # Additional condition for 'absent' case
    #                 if display_value == 'absent':
    #                     display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
    #             elif display_value == 'multifocal':
    #                 key = 2
    #                 sub_key = "multifocal_airspace_opacity"
    #             elif display_value == 'diffuse lower':
    #                 key = 3
    #                 sub_key = "diffuse_lower_airspace_opacity"
    #             elif display_value == 'diffuse upper':
    #                 key = 4
    #                 sub_key = "diffuse_upper_airspace_opacity"

    #             if key is None or sub_key is None:
    #                 raise ValueError(f"Unexpected key or sub_key values: {key}, {sub_key}")

    #             bodySite_snomed_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Snomed.code"]
    #             fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
    #             try:
    #                 assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, \
    #                     f"SNOMED code mismatch: Expected {bodySite_snomed_code_as_per_req}, but got {fhir_bodySite_snomed_code} for {target} observation, {sub_key}"
    #                 with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
    #                     allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
    #                         From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
                    
    #             except AssertionError:
    #                 failures.append(target)
                    
    #             print(f"BodySite Snomed code {bodySite_snomed_code_as_per_req} from Requirements match with {fhir_bodySite_snomed_code} from FHIR json for {target} observation, {sub_key}")

    #             continue
                
                
    #         else:
    #             bodySite_snomed_code_as_per_req = self.cxr_req[target][0]["bodySite_Snomed.code"]
    #             fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
            
    #             try:
    #                 assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
            
    #                 with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
    #                     allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
    #                                 From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Snomed bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)

                
    #                 print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")

    #             except AssertionError:
    #                 failures.append(target)
                
    #     if failures:
    #         print(f"Snomed bodySite code mismatches are observed in FHIR.json for following observations :{failures}")
    #         with allure.step(f"Snomed bodySite code mismatches are observed in FHIR.json"):
    #             allure.attach(f"Snomed bodySite code mismatches are observed in FHIR.json for {failures} ", 
    #                         f"BodySite code mismatch found in FHIR.json - Snomed coding system", allure.attachment_type.TEXT)
    #         return False
    #     else:
    #         return True   
                
            
            
            
    # def verify_radlex_code(self, fhir_contents):
    #     self.cxr_req = conftest.read_cxr_req()
    #     failures = []
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         # bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
            
    #         if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
    #             pass
            
    #         elif target == "RDES230":
    #             bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
    #             fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
            
            
    #         elif target == "RDES225":
    #             display_value = None

    #             if len(fhir_contents["contained"][observation]["component"]) == 4 :
    #                 display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
    #             elif len(fhir_contents["contained"][observation]["component"]) == 5 :
    #                 display_value = fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"]
                
    #             if display_value is not None and display_value not in ['absent', 'focal', 'multifocal', 'diffuse lower', 'diffuse upper']:
    #                 raise ValueError(f"Unexpected display value: {display_value}")

    #             key = None
    #             sub_key = None

    #             if display_value in ['absent', 'focal']:
    #                 key = 1
    #                 sub_key = "focal_airspace_opacity"
    #                 # Additional condition for 'absent' case
    #                 if display_value == 'absent':
    #                     display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
    #             elif display_value == 'multifocal':
    #                 key = 2
    #                 sub_key = "multifocal_airspace_opacity"
    #             elif display_value == 'diffuse lower':
    #                 key = 3
    #                 sub_key = "diffuse_lower_airspace_opacity"
    #             elif display_value == 'diffuse upper':
    #                 key = 4
    #                 sub_key = "diffuse_upper_airspace_opacity"

    #             if key is None or sub_key is None:
    #                 raise ValueError(f"Unexpected key or sub_key values: {key}, {sub_key}")

    #             bodySite_radlex_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Radlex.code"]
    #             fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
    #             try:
    #                 assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, \
    #                     f"Radlex code mismatch: Expected {bodySite_radlex_code_as_per_req}, but got {fhir_bodySite_radlex_code} for {target} observation"
    #                 with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
    #                     allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
    #                         From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
    #                 print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching, for {target} observation")            
    #             except AssertionError:
    #                 failures.append(target)
                    
    #             print(f"BodySite Radlex code {bodySite_radlex_code_as_per_req} from Requirements match with {fhir_bodySite_radlex_code} from FHIR json for {target} observation, {sub_key}")
    #             continue
            
            
    #         else:
    #             bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
    #             fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                
    #         try:
    #             assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
    #             with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
    #                 allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
    #                     From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
    #             print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching for {target} observation")            
    #         except AssertionError:
    #             failures.append(target)
        
    #     if failures:
    #         print(f"Radlex bodySite code mismatches are observed in FHIR.json for following observations :{failures}")
    #         with allure.step(f"Radlex bodySite code mismatches are observed in FHIR.json"):
    #             allure.attach(f"Radlex bodySite code mismatches are observed in FHIR.json for {failures} ", 
    #                           f"BodySite code mismatch found in FHIR.json - Radlex coding system", allure.attachment_type.TEXT)
    #         return False
    #     else:
    #         return True
        