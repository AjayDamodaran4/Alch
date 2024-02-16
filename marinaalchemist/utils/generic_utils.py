import os, json, allure, pytest
from .config_reader import Config
import conftest
from .dicom_utils import DicomUtils


class GenericUtils(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        
    def output_folder_generator(self):
        parent_directory = Config.get_value_of_config_key("output_path")

        # Check if folder '1' exists, if not, start numbering from 1
        if not os.path.exists(os.path.join(parent_directory, '1')):
            next_folder_number = 1
        else:
            # Get the list of existing folders in the parent directory
            existing_folders = [int(folder) for folder in os.listdir(parent_directory) if folder.isdigit()]

            # Find the next sequential folder number
            next_folder_number = max(existing_folders) + 1 if existing_folders else 1

        # Create the new folder with the next sequential number
        new_folder_path = os.path.join(parent_directory, str(next_folder_number))
        os.makedirs(new_folder_path)
        os.chmod(new_folder_path, 0o777)

        return new_folder_path
    
    
    def validate_files_presence(self,files_list, folder_path):
        for file in files_list:
            file_path = os.path.join(folder_path, file)
            assert os.path.isfile(file_path), f"File {file} not found in {folder_path}"
        print("Annalise-cxr-FHIR.json and resultManifest.json files are available in the OUTPUT folder")
            
            
    # def parse_json_file(self, file_name, folder_path):
    #     file_path = os.path.join(folder_path, file_name)
    #     with open(file_path, 'r') as file:
    #         file_contents = json.load(file)
    #     print(f"{file_name} parsed successfully.")
    #     return file_contents

    def parse_json_file(self, folder_path):
        
        with open(folder_path, 'r') as file:
            file_contents = json.load(file)
        print(f"{folder_path} parsed successfully.")
        return file_contents
    
    
    
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
        
        
        
    def verify_snomed_code(self, fhir_contents):
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            # bodySite_snomed_code_as_per_req = self.cxr_req[target][0]["bodySite_Snomed.code"]
            
            if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
                pass
            
            elif target == "RDES230": # This is ignored from verifying as snomed is not applicable for RDES230 observation
                pass
            
            elif target == "RDES225": # This block verifies the bodySite of Chest Radiograph Pulmonary Nodules observation
                display_value = None
                
                if len(fhir_contents["contained"][observation]["component"]) == 4 :
                    display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
                elif len(fhir_contents["contained"][observation]["component"]) == 5 :
                    display_value = fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"]
                
                if display_value is not None and display_value not in ['absent', 'focal', 'multifocal', 'diffuse lower', 'diffuse upper']:
                    raise ValueError(f"Unexpected display value: {display_value}")

                key = None
                sub_key = None

                if display_value in ['absent', 'focal']:
                    key = 1
                    sub_key = "focal_airspace_opacity"
                    # Additional condition for 'absent' case
                    if display_value == 'absent':
                        display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
                elif display_value == 'multifocal':
                    key = 2
                    sub_key = "multifocal_airspace_opacity"
                elif display_value == 'diffuse lower':
                    key = 3
                    sub_key = "diffuse_lower_airspace_opacity"
                elif display_value == 'diffuse upper':
                    key = 4
                    sub_key = "diffuse_upper_airspace_opacity"

                if key is None or sub_key is None:
                    raise ValueError(f"Unexpected key or sub_key values: {key}, {sub_key}")

                bodySite_snomed_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Snomed.code"]
                fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                try:
                    assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, \
                        f"SNOMED code mismatch: Expected {bodySite_snomed_code_as_per_req}, but got {fhir_bodySite_snomed_code} for {target} observation, {sub_key}"
                    with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
                        allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
                            From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
                    
                except AssertionError:
                    failures.append(target)
                    
                print(f"BodySite Snomed code {bodySite_snomed_code_as_per_req} from Requirements match with {fhir_bodySite_snomed_code} from FHIR json for {target} observation, {sub_key}")

                continue
                
                
            else:
                bodySite_snomed_code_as_per_req = self.cxr_req[target][0]["bodySite_Snomed.code"]
                fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
            
                try:
                    assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
            
                    with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
                        allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
                                    From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Snomed bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)

                
                    print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")

                except AssertionError:
                    failures.append(target)
                
        if failures:
            print(f"Snomed bodySite code mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"Snomed bodySite code mismatches are observed in FHIR.json"):
                allure.attach(f"Snomed bodySite code mismatches are observed in FHIR.json for {failures} ", 
                            f"BodySite code mismatch found in FHIR.json - Snomed coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True   
                
            
            
            
    def verify_radlex_code(self, fhir_contents):
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            # bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
            
            if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
                pass
            
            elif target == "RDES230":
                bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
                fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
            
            
            elif target == "RDES225":
                display_value = None

                if len(fhir_contents["contained"][observation]["component"]) == 4 :
                    display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
                elif len(fhir_contents["contained"][observation]["component"]) == 5 :
                    display_value = fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"]
                
                if display_value is not None and display_value not in ['absent', 'focal', 'multifocal', 'diffuse lower', 'diffuse upper']:
                    raise ValueError(f"Unexpected display value: {display_value}")

                key = None
                sub_key = None

                if display_value in ['absent', 'focal']:
                    key = 1
                    sub_key = "focal_airspace_opacity"
                    # Additional condition for 'absent' case
                    if display_value == 'absent':
                        display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
                elif display_value == 'multifocal':
                    key = 2
                    sub_key = "multifocal_airspace_opacity"
                elif display_value == 'diffuse lower':
                    key = 3
                    sub_key = "diffuse_lower_airspace_opacity"
                elif display_value == 'diffuse upper':
                    key = 4
                    sub_key = "diffuse_upper_airspace_opacity"

                if key is None or sub_key is None:
                    raise ValueError(f"Unexpected key or sub_key values: {key}, {sub_key}")

                bodySite_radlex_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Radlex.code"]
                fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                try:
                    assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, \
                        f"Radlex code mismatch: Expected {bodySite_radlex_code_as_per_req}, but got {fhir_bodySite_radlex_code} for {target} observation"
                    with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
                        allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
                            From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
                    print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching, for {target} observation")            
                except AssertionError:
                    failures.append(target)
                    
                print(f"BodySite Radlex code {bodySite_radlex_code_as_per_req} from Requirements match with {fhir_bodySite_radlex_code} from FHIR json for {target} observation, {sub_key}")
                continue
            
            
            else:
                bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
                fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                
            try:
                assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
                    allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
                        From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
                print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching for {target} observation")            
            except AssertionError:
                failures.append(target)
        
        if failures:
            print(f"Radlex bodySite code mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"Radlex bodySite code mismatches are observed in FHIR.json"):
                allure.attach(f"Radlex bodySite code mismatches are observed in FHIR.json for {failures} ", 
                              f"BodySite code mismatch found in FHIR.json - Radlex coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True
        

    
    
    
    def verify_obs_code_annalise_system(self,fhir_contents, *args):
        count = 0
        args_lower = [arg.lower() for arg in args]
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        valid_args = {"row", "us"}
        failures = []
        target_unavailable = []
        self.cxr_req = conftest.read_cxr_req()
        Annalise_code_as_per_req = None
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                continue
            else:
                if region_ROW and not region_US:
                    assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                    try:
                        Annalise_code_as_per_req = self.cxr_req["ROW"][target_obs][0]["Annalise_observation.code"]
                    except KeyError:
                        target_unavailable.append(target_obs)
                elif region_US and not region_ROW:
                    try:
                        Annalise_code_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.code"]
                    except KeyError as e:
                        target_unavailable.append(target_obs)
                
                assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"

                fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                if Annalise_code_as_per_req is not None:
                    try:
                        assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"Observation code for {target_obs} does not match with requirement! \
                            Observation code as per requirement : {Annalise_code_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_code}"
                        print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_code_as_per_req}, From FHIR.json : {fhir_annalise_obs_code}")
                        count+=1
                    except AssertionError as e:
                            failures.append(target_obs)
        print(count)
        self.annalise_code_block_executed = True
                    
        
        if failures or target_unavailable:
            if failures:
                print(f"Annalise Observation code mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"Annalise Observation code mismatches are observed in FHIR.json"):
                    allure.attach(f"Annalise Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng Annalise Observation code from FHIR.json not found in requirement :{target_unavailable}")
                return False
            else:
                return True
        
        
        
    
    
    
    def verify_obs_code_nuance_system(self,fhir_contents, *args):
        args_lower = [arg.lower() for arg in args]
        region_US = "us" in args_lower
        valid_args = ["us"]
        failures = []
        count = 0
        target_unavailable = []
        self.cxr_req = conftest.read_cxr_req()
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        Annalise_code_as_per_req, nuance_code_as_per_req = None, None
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('us')")

        if not region_US:
            raise ValueError("regionOfInstance - 'US' argument must be specified")
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture", "pleural_effusion", "pneumomediastinum", 
                               "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax"]
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        self.cxr_req = conftest.read_cxr_req()
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                pass
            else:
                if region_US:
                    if target_obs in non_nuance_findings:
                        if not self.annalise_code_block_executed:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                            assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"
                        
                            try:
                                Annalise_code_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.code"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                                
                            if Annalise_code_as_per_req is not None:    
                                try:
                                    assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {Annalise_code_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_code}"
                                    print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_code_as_per_req}, From FHIR.json : {fhir_annalise_obs_code}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                        else:
                            pass
                    else:
                        if len(fhir_contents['contained'][observation]['code']['coding']) == 1:
                            assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'http://nuancepowerscribe.com/ai', f"Coding system displayed in FHIR.json for {target_obs} observation is not Nuance. Exepcted is Nuance Coding system."
                            try:
                                nuance_code_as_per_req = self.cxr_req["US"]['nuance_coding_system'][target_obs][0]["Nuance_observation.code"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                            
                            if nuance_code_as_per_req is not None: 
                                try:
                                    assert nuance_code_as_per_req == fhir_nuance_obs_code, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {nuance_code_as_per_req}, Observation code from FHIR.json : {fhir_nuance_obs_code}"
                                    count+=1
                                    print(f"Nuance coding system matches as per requirement. From requirement : {nuance_code_as_per_req}, From FHIR.json : {fhir_nuance_obs_code}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                                    
                        elif len(fhir_contents['contained'][observation]['code']['coding']) == 2:
                            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][1]["code"])
                            assert fhir_contents['contained'][observation]['code']['coding'][1]['system'] == 'http://nuancepowerscribe.com/ai', f"Coding system displayed in FHIR.json for {target_obs} observation is not Nuance. Exepcted is Nuance Coding system."
                            try:
                                nuance_code_as_per_req = self.cxr_req["US"]['nuance_coding_system'][target_obs][0]["Nuance_observation.code"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
                            
                            if nuance_code_as_per_req is not None: 
                                try:
                                    assert nuance_code_as_per_req == fhir_nuance_obs_code, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {nuance_code_as_per_req}, Observation code from FHIR.json : {fhir_nuance_obs_code}"
                                    count+=1
                                    print(f"Nuance coding system matches as per requirement. From requirement : {nuance_code_as_per_req}, From FHIR.json : {fhir_nuance_obs_code}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                                
                        else:
                            print(f"more than one/two coding systems are present for {target_obs} observation")
                            pytest.fail(f"more than one/two coding systems are present for {target_obs} observation")
                    
        print(count)
        
        
        if failures or target_unavailable:
            if failures:
                print(f"Nuance Observation code mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"Annalise Observation code mismatches are observed in FHIR.json"):
                    allure.attach(f"Annalise Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng Nuance Observation code from FHIR.json not found in requirement :{target_unavailable}")
                return False
            else:
                return True
        
    
    
    
    def verify_obs_code_radelement(self,fhir_contents,regionOfInstance):
        valid_args = ['us']
        presence = False
        if regionOfInstance.lower() not in valid_args:
            raise ValueError(f"Provided regionOfInstance argument : {regionOfInstance} is not supported. Supported argument is : 'US' ")
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        target_unavailable = []
        radelement_code_as_per_req = None
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            
            if "RDES" in target_obs:
                presence = True
            
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == "http://radelement.org", f"Coding system displayed in FHIR.json for {target_obs} observation is not RadElement. Exepcted is RadElement Coding system"

                try:
                    radelement_code_as_per_req = self.cxr_req["US"]['radelement_coding_system'][target_obs][0]["RadElement_observation.code"]
                except KeyError as e:
                    target_unavailable.append(target_obs)
            
                fhir_radelement_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                
                if radelement_code_as_per_req is not None:
                    try:
                        assert radelement_code_as_per_req == fhir_radelement_obs_code, f"Observation code for {target_obs} does not match with requirement! \
                            Observation code as per requirement : {radelement_code_as_per_req}, Observation code from FHIR.json : {fhir_radelement_obs_code}"
                        print(f"RadElement coding system matches as per requirement. From requirement : {radelement_code_as_per_req}, From FHIR.json : {fhir_radelement_obs_code}")
                    except AssertionError as e:
                        failures.append(target_obs)
                    
                    
            # else:
            #     if not self.annalise_code_block_executed:
            #         assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"
            #         try:
            #             Annalise_code_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.code"]
            #         except KeyError as e:
            #             target_unavailable.append(target_obs)
                        
            #         fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                        
            #         try:
            #             assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"Observation code for {target_obs} does not match with requirement! \
            #                 Observation code as per requirement : {Annalise_code_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_code}"
            #             print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_code_as_per_req}, From FHIR.json : {fhir_annalise_obs_code}")
            #         except AssertionError as e:
            #             failures.append(target_obs)
            #     else:
            #         pass
        
        # if not presence:
        #     print("No RadElement findings are found in FHIR.json")
        #     pytest.fail("No RadElement findings are found in FHIR.json")

        if failures or target_unavailable or not presence:
            if failures:
                print(f"RadElement Observation code mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"RadElement Observation code mismatches are observed in FHIR.json"):
                    allure.attach(f"RadElement Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in RadElement coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng RadElement Observation code from FHIR.json not found in requirement :{target_unavailable}")
                return False
            
            elif not presence:
                print("No RadElement findings are found in FHIR.json")
                return False
            
            else:
                return True



    
    def fetch_all_observation(self,fhir_contents):
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            yield target_obs
    
    
    def verify_observation_code(self, fhir_contents, *args):
        args_lower = [arg.lower() for arg in args]
        annalise_present = "annalise" in args_lower
        nuance_present = "nuance" in args_lower
        radelement_present = "radelement" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        
        
        valid_args = {"row", "annalise", "us", "nuance", "radelement"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us', 'annalise', 'nuance', 'radelement')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")

        if not (annalise_present or nuance_present or radelement_present):
            raise ValueError("Any one of coding systems (annalise/nuance/radelement) must be specified as argument")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture","pleural_effusion", 
                               "pneumomediastinum", "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", 
                               "subdiaphragmatic_gas", "tension_pneumothorax"]
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        # This block verifies the condition/scenario for ROW and annalise coding system
        if region_ROW and not region_US:
            valid_args_for_ROW = {"row", "annalise"}
            invalid_args_for_ROW = [arg for arg in args_lower if arg not in valid_args_for_ROW]
            
            if invalid_args_for_ROW:
                raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_ROW)}")

            else:
                if annalise_present and not (nuance_present or radelement_present):
                    self.verify_obs_code_annalise_system(fhir_contents,"ROW")


        # This block verifies the condition/scenario for ROW and annalise coding system
        elif region_US and not region_ROW:
            valid_args_for_US = {"us", "annalise", "nuance", "radelement"}
            invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
            
            if invalid_args_for_US:
                raise ValueError(f"The following arguments is not supported for US region: {', '.join(invalid_args_for_US)}")

            elif annalise_present and not (nuance_present or radelement_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                self.verify_obs_code_annalise_system(fhir_contents,"US")
            
            
            elif nuance_present and not (annalise_present or radelement_present):
                self.verify_obs_code_nuance_system(fhir_contents,"US")
                        

            elif annalise_present and nuance_present and not (radelement_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        if target_obs in non_nuance_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        else:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 2, f"Two coding systems are not available in FHIR.json for {target_obs} observation"
                self.verify_obs_code_annalise_system(fhir_contents,"US")
                self.verify_obs_code_nuance_system(fhir_contents,"US")
                
                        
            elif annalise_present and radelement_present and not (nuance_present) or radelement_present and not (annalise_present or nuance_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                self.verify_obs_code_annalise_system(fhir_contents,"US")
                self.verify_obs_code_radelement(fhir_contents,"US")
                

                            
            elif nuance_present and radelement_present and not (annalise_present):
                self.verify_obs_code_nuance_system(fhir_contents,"US")
                self.verify_obs_code_radelement(fhir_contents,"US")
            
            
            elif annalise_present and nuance_present and radelement_present:
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        if target_obs in non_nuance_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        elif target_obs in radelement_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        else:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 2, f"Two coding systems are not available in FHIR.json for {target_obs} observation"
                self.verify_obs_code_annalise_system(fhir_contents,"US")
                self.verify_obs_code_nuance_system(fhir_contents,"US")
                self.verify_obs_code_radelement(fhir_contents,"US")
        
        
        # FROM CHATGPT - better option
        # elif region_US and not region_ROW:
        #     valid_args_for_US = {"us", "annalise", "nuance", "radelement"}
        #     invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
        #     print(invalid_args_for_US)
        #     target_unavailable = []
        #     failures = []
        #     result = None
            
        #     if invalid_args_for_US:
        #         raise ValueError(f"The following arguments are not supported for the US region: {', '.join(invalid_args_for_US)}")
            
        #     system_combinations = {
        #         (True, False, False): ["verify_obs_code_annalise_system"],
        #         (False, True, False): ["verify_obs_code_nuance_system"],
        #         (True, True, False): ["verify_obs_code_annalise_system", "verify_obs_code_nuance_system"],
        #         (True, False, True): ["verify_obs_code_annalise_system", "verify_obs_code_radelement"],
        #         (False, False, True): ["verify_obs_code_radelement"],
        #         (False, True, True): ["verify_obs_code_nuance_system", "verify_obs_code_radelement"],
        #         (True, True, True): ["verify_obs_code_annalise_system", "verify_obs_code_nuance_system", "verify_obs_code_radelement"]
        #     }
            
        #     applicable_systems = (annalise_present, nuance_present, radelement_present)
        #     methods_to_call = system_combinations.get(applicable_systems, [])
            
        #     for method_name in methods_to_call:
        #         getattr(self, method_name)(fhir_contents, "US")


    
    
    def verify_obs_display_annalise_system(self,fhir_contents, *args):
        count = 0
        args_lower = [arg.lower() for arg in args]
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        valid_args = {"row", "us"}
        failures = []
        target_unavailable = []
        self.cxr_req = conftest.read_cxr_req()
        Annalise_display_as_per_req = None
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                continue
            else:
                if region_ROW and not region_US:
                    assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                    try:
                        Annalise_display_as_per_req = self.cxr_req["ROW"][target_obs][0]["Annalise_observation.display"]
                    except KeyError:
                        target_unavailable.append(target_obs)
                elif region_US and not region_ROW:
                    try:
                        Annalise_display_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.display"]
                    except KeyError as e:
                        target_unavailable.append(target_obs)
                
                assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"

                fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                if Annalise_display_as_per_req is not None:
                    try:
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                            Observation code as per requirement : {Annalise_display_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_display}"
                        print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_display_as_per_req}, From FHIR.json : {fhir_annalise_obs_display}")
                        count+=1
                    except AssertionError as e:
                            failures.append(target_obs)
        print(count)
        self.annalise_display_block_executed = True
                    
        
        if failures or target_unavailable:
            if failures:
                print(f"Annalise Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"Annalise Observation display text mismatches are observed in FHIR.json"):
                    allure.attach(f"Annalise Observation display text mismatches are observed in FHIR.json for {failures} ", f"Observation display text mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng Annalise Observation display text from FHIR.json not found in requirement :{target_unavailable}")
                return False
            else:
                return True
        
        
    
    
    def verify_obs_display_nuance_system(self,fhir_contents, *args):
        args_lower = [arg.lower() for arg in args]
        region_US = "us" in args_lower
        valid_args = ["us"]
        failures = []
        count = 0
        target_unavailable = []
        self.cxr_req = conftest.read_cxr_req()
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        Annalise_display_as_per_req, nuance_display_as_per_req = None, None
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('us')")

        if not region_US:
            raise ValueError("regionOfInstance - 'US' argument must be specified")
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture", "pleural_effusion", "pneumomediastinum", 
                               "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax"]
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        self.cxr_req = conftest.read_cxr_req()
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                pass
            else:
                if region_US:
                    if target_obs in non_nuance_findings:
                        if not self.annalise_display_block_executed:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                            assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"
                        
                            try:
                                Annalise_display_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.code"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                                
                            if Annalise_display_as_per_req is not None:    
                                try:
                                    assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {Annalise_display_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_display}"
                                    print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_display_as_per_req}, From FHIR.json : {fhir_annalise_obs_display}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                        else:
                            pass
                    else:
                        if len(fhir_contents['contained'][observation]['code']['coding']) == 1:
                            assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'http://nuancepowerscribe.com/ai', f"Coding system displayed in FHIR.json for {target_obs} observation is not Nuance. Exepcted is Nuance Coding system."
                            try:
                                nuance_display_as_per_req = self.cxr_req["US"]['nuance_coding_system'][target_obs][0]["Nuance_observation.display"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                            
                            if nuance_display_as_per_req is not None: 
                                try:
                                    assert nuance_display_as_per_req == fhir_nuance_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {nuance_display_as_per_req}, Observation code from FHIR.json : {fhir_nuance_obs_display}"
                                    count+=1
                                    print(f"Nuance coding system matches as per requirement. From requirement : {nuance_display_as_per_req}, From FHIR.json : {fhir_nuance_obs_display}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                                    
                        elif len(fhir_contents['contained'][observation]['code']['coding']) == 2:
                            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][1]["code"])
                            assert fhir_contents['contained'][observation]['code']['coding'][1]['system'] == 'http://nuancepowerscribe.com/ai', f"Coding system displayed in FHIR.json for {target_obs} observation is not Nuance. Exepcted is Nuance Coding system."
                            try:
                                nuance_display_as_per_req = self.cxr_req["US"]['nuance_coding_system'][target_obs][0]["Nuance_observation.display"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][1]["display"]
                            
                            if nuance_display_as_per_req is not None: 
                                try:
                                    assert nuance_display_as_per_req == fhir_nuance_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {nuance_display_as_per_req}, Observation code from FHIR.json : {fhir_nuance_obs_display}"
                                    count+=1
                                    print(f"Nuance coding system matches as per requirement. From requirement : {nuance_display_as_per_req}, From FHIR.json : {fhir_nuance_obs_display}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                                
                        else:
                            print(f"more than one/two coding systems are present for {target_obs} observation")
                            pytest.fail(f"more than one/two coding systems are present for {target_obs} observation")
                    
        print(count)
        
        
        if failures or target_unavailable:
            if failures:
                print(f"Nuance Observation code mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"Annalise Observation code mismatches are observed in FHIR.json"):
                    allure.attach(f"Annalise Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng Nuance Observation code from FHIR.json not found in requirement :{target_unavailable}")
                return False
            else:
                return True
        
    
    
    
    def verify_obs_display_radelement(self,fhir_contents,regionOfInstance):
        valid_args = ['us']
        presence = False
        if regionOfInstance.lower() not in valid_args:
            raise ValueError(f"Provided regionOfInstance argument : {regionOfInstance} is not supported. Supported argument is : 'US' ")
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        target_unavailable = []
        radelement_display_as_per_req = None
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            
            if "RDES" in target_obs:
                presence = True
            
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == "http://radelement.org", f"Coding system displayed in FHIR.json for {target_obs} observation is not RadElement. Exepcted is RadElement Coding system"

                try:
                    radelement_display_as_per_req = self.cxr_req["US"]['radelement_coding_system'][target_obs][0]["RadElement_observation.display"]
                except KeyError as e:
                    target_unavailable.append(target_obs)
            
                fhir_radelement_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                
                if radelement_display_as_per_req is not None:
                    try:
                        assert radelement_display_as_per_req == fhir_radelement_obs_display, f"Observation display text for {target_obs} does not match with requirement! \
                            Observation display text as per requirement : {radelement_display_as_per_req}, Observation display text from FHIR.json : {fhir_radelement_obs_display}"
                        print(f"RadElement coding system matches as per requirement. From requirement : {radelement_display_as_per_req}, From FHIR.json : {fhir_radelement_obs_display}")
                    except AssertionError as e:
                        failures.append(target_obs)
                    

        if failures or target_unavailable or not presence:
            if failures:
                print(f"RadElement Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"RadElement Observation display text mismatches are observed in FHIR.json"):
                    allure.attach(f"RadElement Observation display text mismatches are observed in FHIR.json for {failures} ", f"Observation display text mismatch found in FHIR.json in RadElement coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng RadElement Observation display text from FHIR.json not found in requirement :{target_unavailable}")
                return False
            
            elif not presence:
                print("No RadElement findings are found in FHIR.json")
                return False
            
            else:
                return True




    def verify_observation_display(self, fhir_contents, *args):
        args_lower = [arg.lower() for arg in args]
        annalise_present = "annalise" in args_lower
        nuance_present = "nuance" in args_lower
        radelement_present = "radelement" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        
        
        valid_args = {"row", "annalise", "us", "nuance", "radelement"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us', 'annalise', 'nuance', 'radelement')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")

        if not (annalise_present or nuance_present or radelement_present):
            raise ValueError("Any one of coding systems (annalise/nuance/radelement) must be specified as argument")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture","pleural_effusion", 
                               "pneumomediastinum", "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", 
                               "subdiaphragmatic_gas", "tension_pneumothorax"]
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        # This block verifies the condition/scenario for ROW and annalise coding system
        if region_ROW and not region_US:
            valid_args_for_ROW = {"row", "annalise"}
            invalid_args_for_ROW = [arg for arg in args_lower if arg not in valid_args_for_ROW]
            
            if invalid_args_for_ROW:
                raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_ROW)}")

            else:
                if annalise_present and not (nuance_present or radelement_present):
                    self.verify_obs_display_annalise_system(fhir_contents,"ROW")


        # This block verifies the condition/scenario for ROW and annalise coding system
        elif region_US and not region_ROW:
            valid_args_for_US = {"us", "annalise", "nuance", "radelement"}
            invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
            
            if invalid_args_for_US:
                raise ValueError(f"The following arguments is not supported for US region: {', '.join(invalid_args_for_US)}")

            elif annalise_present and not (nuance_present or radelement_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
            
            
            elif nuance_present and not (annalise_present or radelement_present):
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                        

            elif annalise_present and nuance_present and not (radelement_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        if target_obs in non_nuance_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        else:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 2, f"Two coding systems are not available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                
                        
            elif annalise_present and radelement_present and not (nuance_present) or radelement_present and not (annalise_present or nuance_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
                self.verify_obs_display_radelement(fhir_contents,"US")
                

                            
            elif nuance_present and radelement_present and not (annalise_present):
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                self.verify_obs_display_radelement(fhir_contents,"US")
            
            
            elif annalise_present and nuance_present and radelement_present:
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        if target_obs in non_nuance_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        elif target_obs in radelement_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        else:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 2, f"Two coding systems are not available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                self.verify_obs_display_radelement(fhir_contents,"US")
                
                
                
                
    # def verify_laterality(self,fhir_contents):
        