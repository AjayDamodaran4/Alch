import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils


class Laterality(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()

    def verify_laterality(self,fhir_contents,model_output_contents,*args):
        args_lower = [arg.lower() for arg in args]
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        
        valid_args = {"row", "us"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us', 'annalise', 'nuance', 'radelement')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")

        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
        
        result_flag = True
        laterality_mapping_code = None # Initialized for mapping nuance/radelement codes to annalise coded
        laterality_failures = []
        laterality_value_failures = []
        code_failures = []
        system_failures = []
        laterality_presence = []
        fda_findings = ["pleural_effusion", "pneumothorax", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax", "RDES225", "RDES254", "RDES44", "RDES230", "RDES228"]
        excel_util = ExcelUtils()
        opt_cli_laterality = excel_util.opt_cli_laterality()
        laterality_details = ['RIGHT', 'Right lateral', 'LEFT', 'Left lateral', 'BILATERAL', 'Bilateral', '24028007', '7771000', '51440002']
        if region_ROW:
            for observation in range(3,len(fhir_contents['contained'])):
                target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target_obs == "246501002":
                    pass
                elif target_obs in opt_cli_laterality:
                    print(opt_cli_laterality)
                    for key, value in self.cxr_mappings.items():
                        if target_obs in (key, value):
                            laterality_mapping_code = key
                            laterality_dict = model_output_contents['cxr_value']['study_laterality']['findings'][laterality_mapping_code]['values']
                            laterality = max(laterality_dict, key=laterality_dict.get)
                            laterality_value = max(laterality_dict.values()) * 100
                            observation_laterality = fhir_contents['contained'][observation]['component'][0]['code']['coding'][0]['display']
                            observation_laterality_value = fhir_contents['contained'][observation]['component'][0]['valueQuantity']['value']
                            laterality_code = fhir_contents['contained'][observation]['component'][0]['code']['coding'][0]['code']
                            laterality_system = fhir_contents['contained'][observation]['component'][0]['code']['coding'][0]['system']
                        
                            with allure.step(f"Verification of Laterality, Laterality value, code and system of {target_obs} observation"):
                                
                                verifications = [
                                    ("Laterality code", laterality_code, self.cxr_req['laterality_codes'][observation_laterality]),
                                    ("Laterality system", laterality_system, self.cxr_req['laterality_codes']['system']),
                                    ("Laterality", observation_laterality, self.cxr_req[laterality]),
                                    ("Laterality value", observation_laterality_value, laterality_value)
                                ]

                                for message, actual, expected in verifications:
                                    try:
                                        print(f"{message} of {target_obs} observation from FHIR.json: {actual}, {message} of {target_obs} observation from requirement: {expected}")
                                        allure.attach(f"{message} of {target_obs} observation from FHIR.json: {actual}, {message} of {target_obs} observation from requirement: {expected}", 
                                                    f"{message} of {target_obs} observation", allure.attachment_type.TEXT)
                                        assert actual == expected, f"{message} mismatch found for {target_obs} observation"
                                        allure.attach(f"{message} of {target_obs} observation matches with requirement", "Result", allure.attachment_type.TEXT)
                                    except AssertionError:
                                        if message == "Laterality code":
                                            code_failures.append(target_obs)
                                        elif message == "Laterality system":
                                            system_failures.append(target_obs)
                                        elif message == "Laterality":
                                            laterality_failures.append(target_obs)
                                        elif message == "Laterality value":
                                            laterality_value_failures.append(target_obs)
                else:
                    for component in fhir_contents['contained'][observation]['component']:
                        for key, value in component.items():
                            if isinstance(value, str):
                                try:
                                    assert value not in laterality_details, f"Laterality details are present in components of {target_obs} observation"
                                except AssertionError:
                                    laterality_presence.append(target_obs)
                            elif isinstance(value, dict):
                                for sub_key, sub_value in value.items():
                                    if isinstance(sub_value, str):
                                        try:
                                            assert sub_value not in laterality_details, f"Laterality details are present in components of {target_obs} observation"
                                        except AssertionError:
                                            laterality_presence.append(target_obs)
                                    elif isinstance(sub_value, list):
                                        for sub_dict in sub_value:
                                            for sub_key2, sub_value2 in sub_dict.items():
                                                try:
                                                    assert sub_value2 not in laterality_details, f"Laterality details are present in components of {target_obs} observation"
                                                except AssertionError:
                                                    laterality_presence.append(target_obs)
                                                    print(laterality_presence)
                
            failure_types = [laterality_failures, code_failures, system_failures, laterality_value_failures]
            failure_messages = ["Laterality", "Laterality code", "Laterality system", "Laterality value"]

            for fail_type, fail_message in zip(failure_types, failure_messages):
                if fail_type:
                    result_flag = False
                    print(f"Mismatch in {fail_message} is observed in following observations: {fail_type}")
                    with allure.step(f"Mismatch in {fail_message} is observed in FHIR.json"):
                        allure.attach(f"Mismatch in {fail_message} is observed for following observations: {fail_type}",
                                    "Step Failed", allure.attachment_type.TEXT)
                        
                        
            if laterality_presence:
                result_flag = False
                print(f"Laterality is present for following observations which is not expected. They dont belong to OPT-CLI-002 group : {laterality_presence}")
                with allure.step(f"Laterality is present for following observations which is not expected. They dont belong to OPT-CLI-002 group"):
                        allure.attach(f"Laterality is present for following observations which is not expected. They dont belong to OPT-CLI-002 group: {laterality_presence}",
                                    "Step Failed", allure.attachment_type.TEXT)
            return result_flag
            
        elif region_US:
            for observation in range(3,len(fhir_contents['contained'])):
                target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target_obs == "246501002":
                    pass
                elif target_obs not in fda_findings:
                    for key, value in self.cxr_mappings.items():
                        if target_obs in (key, value):
                            laterality_mapping_code = key
                            laterality_dict = model_output_contents['cxr_value']['study_laterality']['findings'][laterality_mapping_code]['values']
                            laterality = max(laterality_dict, key=laterality_dict.get)
                            laterality_value = max(laterality_dict.values()) * 100
                            if laterality_mapping_code in ["pneumomediastinum", "single_pulmonary_nodule"]:
                                observation_laterality = fhir_contents['contained'][observation]['component'][1]['code']['coding'][0]['display']
                                observation_laterality_value = fhir_contents['contained'][observation]['component'][1]['valueQuantity']['value']
                                laterality_code = fhir_contents['contained'][observation]['component'][1]['code']['coding'][0]['code']
                                laterality_system = fhir_contents['contained'][observation]['component'][1]['code']['coding'][0]['system']
                            else:
                                observation_laterality = fhir_contents['contained'][observation]['component'][0]['code']['coding'][0]['display']
                                observation_laterality_value = fhir_contents['contained'][observation]['component'][0]['valueQuantity']['value']
                                laterality_code = fhir_contents['contained'][observation]['component'][0]['code']['coding'][0]['code']
                                laterality_system = fhir_contents['contained'][observation]['component'][0]['code']['coding'][0]['system']
                            
                            with allure.step(f"Verification of Laterality, Laterality value, code and system of {target_obs} observation"):
                                verifications = [
                                    ("Laterality code", laterality_code, self.cxr_req['laterality_codes'][observation_laterality]),
                                    ("Laterality system", laterality_system, self.cxr_req['laterality_codes']['system']),
                                    ("Laterality", observation_laterality, self.cxr_req[laterality]),
                                    ("Laterality value", observation_laterality_value, laterality_value)
                                ]

                                for message, actual, expected in verifications:
                                    try:
                                        print(f"{message} of {target_obs} observation from FHIR.json: {actual}, {message} of {target_obs} observation from requirement: {expected}")
                                        allure.attach(f"{message} of {target_obs} observation from FHIR.json: {actual}, {message} of {target_obs} observation from requirement: {expected}", 
                                                    f"{message} of {target_obs} observation", allure.attachment_type.TEXT)
                                        assert actual == expected, f"{message} mismatch found for {target_obs} observation"
                                        allure.attach(f"{message} of {target_obs} observation matches with requirement", "Result", allure.attachment_type.TEXT)
                                    except AssertionError:
                                        if message == "Laterality code":
                                            code_failures.append(target_obs)
                                        elif message == "Laterality system":
                                            system_failures.append(target_obs)
                                        elif message == "Laterality":
                                            laterality_failures.append(target_obs)
                                        elif message == "Laterality value":
                                            laterality_value_failures.append(target_obs)

                else:
                    for component in fhir_contents['contained'][observation]['component']:
                        for key, value in component.items():
                            if isinstance(value, str):
                                try:
                                    assert value not in laterality_details, f"Laterality details are present in components of {target_obs} observation"
                                except AssertionError:
                                    laterality_presence.append(target_obs)
                            elif isinstance(value, dict):
                                for sub_key, sub_value in value.items():
                                    if isinstance(sub_value, str):
                                        try:
                                            assert sub_value not in laterality_details, f"Laterality details are present in components of {target_obs} observation"
                                        except AssertionError:
                                            laterality_presence.append(target_obs)
                                    elif isinstance(sub_value, list):
                                        for sub_dict in sub_value:
                                            for sub_key2, sub_value2 in sub_dict.items():
                                                try:
                                                    assert sub_value2 not in laterality_details, f"Laterality details are present in components of {target_obs} observation"
                                                except AssertionError:
                                                    laterality_presence.append(target_obs)
                    
            failure_types = [laterality_failures, code_failures, system_failures, laterality_value_failures]
            failure_messages = ["Laterality", "Laterality code", "Laterality system", "Laterality value"]

            for fail_type, fail_message in zip(failure_types, failure_messages):
                if fail_type:
                    result_flag = False
                    print(f"Mismatch in {fail_message} is observed in following observations: {fail_type}")
                    with allure.step(f"Mismatch in {fail_message} is observed in FHIR.json"):
                        allure.attach(f"Mismatch in {fail_message} is observed for following observations: {fail_type}",
                                    "Step Failed", allure.attachment_type.TEXT)

            if laterality_presence:
                result_flag = False
                print(f"Laterality is present for following observations which is not expected as these findings are FDA approved. : {laterality_presence}")
                with allure.step(f"Laterality is present for following observations which is not expected as these findings are FDA approved."):
                        allure.attach(f"Laterality is present for following observations which is not expected as these findings are FDA approved.: {laterality_presence}",
                                    "Step Failed", allure.attachment_type.TEXT)
                        
            return result_flag