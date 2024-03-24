import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils


class Observation_Code_Display(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()
        self.non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture","pleural_effusion", 
                            "pneumomediastinum", "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", 
                            "subdiaphragmatic_gas", "tension_pneumothorax"]
        self.group_findings = ["focal_airspace_opacity", "multifocal_airspace_opacity", "diffuse_lower_airspace_opacity", "diffuse_upper_airspace_opacity", "RDES225"]
        self.radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]


    def check_for_systems(self,fhir_contents=None, system=None):
        args_lower = [arg.lower() for arg in system]
        annalise_present = "annalise" in args_lower
        nuance_present = "nuance" in args_lower
        radelement_present = "radelement" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        systems_mismatch = []

        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002" :
                continue
            
            fhir_observation_detail_block = fhir_contents["contained"][observation]["code"]["coding"]
            
            if region_ROW and not region_US:
                
                try:
                    assert len(fhir_observation_detail_block) == 1
                    assert fhir_observation_detail_block[0]["system"] == "https://www.annalise.ai/guides"
                except AssertionError:
                    systems_mismatch.append(observation_name)
                    
            elif region_US and not region_ROW:
                
                expected_systems = {
                    (True, False, False): ["https://www.annalise.ai/guides"],
                    (False, True, False): ["https://www.annalise.ai/guides"] if observation_name in self.non_nuance_findings else ["http://nuancepowerscribe.com/ai"],
                    (False, False, True): ["http://radelement.org"] if observation_name in self.radelement_findings else ["https://www.annalise.ai/guides"],
                    (True, True, False): ["https://www.annalise.ai/guides"] if observation_name in self.non_nuance_findings else ["https://www.annalise.ai/guides", "http://nuancepowerscribe.com/ai"],
                    (True, False, True): ["http://radelement.org"] if observation_name in self.radelement_findings else ["https://www.annalise.ai/guides"],
                    (False, True, True): ["https://www.annalise.ai/guides"] if observation_name in self.non_nuance_findings else ["http://radelement.org"] if observation_name in self.radelement_findings else ["http://nuancepowerscribe.com/ai"],
                    (True, True, True): ["http://radelement.org"] if observation_name in self.radelement_findings else (["https://www.annalise.ai/guides"] if observation_name in self.non_nuance_findings else ["https://www.annalise.ai/guides", "http://nuancepowerscribe.com/ai"])
                }

                expected_system = expected_systems.get((annalise_present, nuance_present, radelement_present))
                try:
                    assert len(fhir_observation_detail_block) == len(expected_system)
                except AssertionError:
                    systems_mismatch.append(observation_name)
                if len(fhir_observation_detail_block) == len(expected_system):
                    for i, detail in enumerate(fhir_observation_detail_block):
                        if detail["system"] != expected_system[i]:
                            systems_mismatch.append(observation_name)

        if systems_mismatch:
            with allure.step(f"Test Failure Details"):
                allure.attach(f"{systems_mismatch}", f"Observation's coding systems present in FHIR.json does not match with requirement or with coding systems that's passed as argument for test case for following observations: ", allure.attachment_type.TEXT)
            print(f"Observation's coding systems present in FHIR.json does not match with requirement or with coding systems that's passed as argument for test case for following observations: {systems_mismatch}")
            return False
        else:
            return True
            
    
    def get_observation_details(self,observation_name,system):
        applicable_details = []
        for each in system:
            if each == "nuance_coding_system": 
                if observation_name in self.group_findings:
                    mapped_observation_name = self.cxr_mappings[observation_name][0]
                else:
                    if observation_name not in self.cxr_mappings.keys():
                        mapped_observation_name = observation_name
                    else:
                        mapped_observation_name = self.cxr_mappings[observation_name]
            else:
                mapped_observation_name = observation_name
            
            obs_code = self.cxr_req['US'][each][mapped_observation_name][0][(f"{each.split('_')[0]}_observation.code").capitalize()]
            obs_display = self.cxr_req['US'][each][mapped_observation_name][0][(f"{each.split('_')[0]}_observation.display").capitalize()]
            obs_system = self.cxr_req['US'][each][mapped_observation_name][0][(f"{each.split('_')[0]}_system").capitalize()]
            obs_text = self.cxr_req['US'][each][mapped_observation_name][0][(f"{each.split('_')[0]}_observation.text").capitalize()]
            applicable_details.extend([obs_system, obs_code, obs_display, obs_text])
        return applicable_details
    
    
    def verify_observation1_code(self,fhir_contents=None, system=None):
        args_lower = [arg.lower() for arg in system]
        annalise_present = "annalise" in args_lower
        nuance_present = "nuance" in args_lower
        radelement_present = "radelement" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        observation_details_mismatch = []
        observation_text_mismatch = []
        
        valid_args = ["row", "annalise", "us", "nuance", "radelement"]
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        
        if region_US and not region_ROW:
            if not (annalise_present or nuance_present or radelement_present):
                raise ValueError("Any one of coding systems (annalise/nuance/radelement) must be specified as argument for 'US' regionOfInstance")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
        
        with allure.step(f"Verification of Observation code and display details in Annalise-cxr-FHIR.json"):
            allure.attach(f"{fhir_contents}", f"Annalise-cxr-FHIR.json contents", allure.attachment_type.TEXT)
        
        if not self.check_for_systems(fhir_contents=fhir_contents, system=system):
            return False
        
        for observation in range(3,len(fhir_contents['contained'])):
            observation_name = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if observation_name == "246501002" :
                continue
            
            if region_ROW and not region_US:
                obs_annalise_code = self.cxr_req["ROW"][observation_name][0]["Annalise_observation.code"]
                obs_annalise_display = self.cxr_req["ROW"][observation_name][0]["Annalise_observation.display"]
                expected_obs_code_display = [{
                                        "system": "https://www.annalise.ai/guides",
                                        "code": obs_annalise_code,
                                        "display": obs_annalise_display
                                        }]
                
                fhir_observation_detail_block = fhir_contents["contained"][observation]["code"]["coding"]
                    
            elif region_US and not region_ROW:
                
                valid_args_for_US = {"us", "annalise", "nuance", "radelement"}
                invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
                
                if invalid_args_for_US:
                    raise ValueError(f"The following arguments is not supported for US region: {', '.join(invalid_args_for_US)}")
                
                expected_systems = {
                    (True, False, False): ["annalise_coding_system"],
                    (False, True, False): ["annalise_coding_system"] if observation_name in self.non_nuance_findings else ["nuance_coding_system"],
                    (False, False, True): ["radelement_coding_system"] if observation_name in self.radelement_findings else ["annalise_coding_system"],
                    (True, True, False): ["annalise_coding_system"] if observation_name in self.non_nuance_findings else ["annalise_coding_system","nuance_coding_system"],
                    (True, False, True):  ["radelement_coding_system"] if observation_name in self.radelement_findings else ["annalise_coding_system"],
                    (False, True, True): ["annalise_coding_system"] if observation_name in self.non_nuance_findings else ["radelement_coding_system"] if observation_name in self.radelement_findings else ["nuance_coding_system"],
                    (True, True, True): ["radelement_coding_system"] if observation_name in self.radelement_findings else ["annalise_coding_system"] if observation_name in self.non_nuance_findings else ["annalise_coding_system","nuance_coding_system"]
                }

                # Retrieve expected systems based on the combination of present flags
                expected_system = expected_systems.get((annalise_present, nuance_present, radelement_present))
                
                expected_obs_details = self.get_observation_details(observation_name, expected_system)

                expected_obs_code_display = [
                    {"system": expected_obs_details[i], "code": expected_obs_details[i+1], "display": expected_obs_details[i+2]}
                    for i in range(0, len(expected_obs_details), 4)]

                fhir_observation_detail_block = fhir_contents["contained"][observation]["code"]["coding"]
            with allure.step(f"Verification of code and display of {observation_name} observation as per applicable coding systems"):
                allure.attach(f"Expected details as per requirement : {expected_obs_code_display}, Details from FHIR : {fhir_observation_detail_block}",
                            f"Observation code and display details of {observation_name} observation", allure.attachment_type.TEXT)
                
            try:
                assert expected_obs_code_display == fhir_observation_detail_block
                allure.attach(f"Validation complete for {observation_name} observation",
                                f"Observation code and display matches as per requirement for {observation_name} observation", allure.attachment_type.TEXT)
                print(f"observation code and display match as per requirement for {observation_name}")
            except AssertionError:
                observation_details_mismatch.append(observation_name)
                
            try:
                text_req = expected_obs_details[3]
                if observation_name!="RDES225": # text field should be added to RDES225 in FHIR.json
                    assert text_req == fhir_contents["contained"][observation]["code"]["text"]
                    allure.attach(f"Text matches as per requirement. Text from requirement : {text_req} , Text from Annalise-cxr-FHIR.json : {fhir_contents["contained"][observation]["code"]["text"]}",
                                f"Validation results of Observation text for {observation_name} observation", allure.attachment_type.TEXT)
            except AssertionError:
                observation_text_mismatch.append(observation_name)
                    
        if observation_details_mismatch or observation_text_mismatch:
            error_messages = []

            if observation_details_mismatch:
                error_messages.append(f"Observation's code/Display in FHIR.json does not match with requirement for following observations : {observation_details_mismatch}")
            if observation_text_mismatch:
                error_messages.append(f"Observation's text in FHIR.json does not match with requirement for following observations : {observation_text_mismatch}")
            
            if error_messages:
                with allure.step(f"Test Failure Details :"):
                    
                    allure.attach(f"{error_messages}",
                                f"Test Failure Details", allure.attachment_type.TEXT)
                print("\n".join(error_messages))
                return False
        
        else:
            return True
