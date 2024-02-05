import os, json, allure, pytest
from .config_reader import Config
import conftest
from .dicom_utils import DicomUtils


class GenericUtils(object):

        
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
                            assert tracking_id_display == "Tracking Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"
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
                            assert tracking_uid_display == "Tracking Unique Identifier", f"Tracking Unique Identifier display text of {target} observation from FHIR report does not match the requirement"
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
        

    # def verify_observation_225(self, observation, fhir_contents):

    # # Verify the bodySite for the Chest Radiograph Pulmonary Nodules observation (RDES225).

    # # Parameters:
    # # - observation: Index of the observation.
    # # - fhir_contents: Contents of the FHIR report.

    # # Raises:
    # # - AssertionError: If the bodySite codes do not match.

    #     target = "RDES225"
    #     display_value = None

    #     if len(fhir_contents["contained"][observation]["component"]) == 4 :
    #         display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
    #     elif len(fhir_contents["contained"][observation]["component"]) == 5 :
    #         display_value = fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"]
        
    #     if display_value is not None and display_value not in ['absent', 'focal', 'multifocal', 'diffuse lower', 'diffuse upper']:
    #         raise ValueError(f"Unexpected display value: {display_value}")

    #     key = None
    #     sub_key = None

    #     if display_value in ['absent', 'focal']:
    #         key = 1
    #         sub_key = "focal_airspace_opacity"
    #         # Additional condition for 'absent' case
    #         if display_value == 'absent':
    #             display_value = fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"]
    #     elif display_value == 'multifocal':
    #         key = 2
    #         sub_key = "multifocal_airspace_opacity"
    #     elif display_value == 'diffuse lower':
    #         key = 3
    #         sub_key = "diffuse_lower_airspace_opacity"
    #     elif display_value == 'diffuse upper':
    #         key = 4
    #         sub_key = "diffuse_upper_airspace_opacity"

    #     if key is None or sub_key is None:
    #         raise ValueError(f"Unexpected key or sub_key values: {key}, {sub_key}")

    #     bodySite_snomed_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Snomed.code"]
    #     fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
    #     try:
    #         assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, \
    #             f"SNOMED code mismatch: Expected {bodySite_snomed_code_as_per_req}, but got {fhir_bodySite_snomed_code} for {target} observation, {sub_key}"
    #         with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
    #             allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
    #                 From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
            
    #     except AssertionError:
    #         raise

    #     bodySite_radlex_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Radlex.code"]
    #     fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
    #     try:
    #         assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, \
    #             f"Radlex code mismatch: Expected {bodySite_radlex_code_as_per_req}, but got {fhir_bodySite_radlex_code} for {target} observation"
    #         with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
    #             allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
    #                 From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
       
    #     except AssertionError:
    #         raise    
    #     print(f"BodySite SNOMED code {bodySite_snomed_code_as_per_req} and Radlex code {bodySite_radlex_code_as_per_req} "
    #         f"from Requirements match with {fhir_bodySite_snomed_code} and {fhir_bodySite_radlex_code} from FHIR json for {target} observation, {sub_key}")



    
    def fetch_all_observation(self,fhir_contents):
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            yield target_obs
    
    
    def verify_obs_code_annalise_system(self,fhir_contents):
        failures = []
        self.cxr_req = conftest.read_cxr_req()
        count=0
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            else:
                if self.cxr_req[target_obs][0]["Annalise_coding_system"]==True:
                    if target_obs in non_nuance_findings:
                        try:
                            
                            assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                            assert self.cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                            print(f"Annalise code as per requirement for {target_obs} observation : {Annalise_code_as_per_req}")
                            print(f"Annalise code from FHIR report for {target_obs} observation : {fhir_annalise_obs_code}")
                            Annalise_code_as_per_req = self.cxr_req[target_obs][0]["Annalise_observation.code"]
                            fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                            assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"{Annalise_code_as_per_req} from requrirement and {fhir_annalise_obs_code} from FHIR are not matching"
                            with allure.step(f"Verifying Observation code for {target_obs} observation for Annalise coding system"):
                                allure.attach(f"Observation code as per requirement : {Annalise_code_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_code}, ", f"Verifying Observation code for {target_obs} observation for Annalise coding system", allure.attachment_type.TEXT)
                            count+=1
                            print(f"Observation code from FHIR report matches with requirement for {target_obs} observation")
                        except AssertionError as e:
                            failures.append(target_obs)
                            

                    
                    else:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==2, f"More than two Coding systems are displayed in FHIR for {target_obs} observation. Only TWO coding systems are expected as per requirement"
                        try:
                            assert self.cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                            assert self.cxr_req[target_obs][0]["Nuance_system"] in fhir_contents["contained"][observation]["code"]["coding"][1]["system"],"Nuance coding system text in FHIR does not match with requirement"
                            Annalise_code_as_per_req = self.cxr_req[target_obs][0]["Annalise_observation.code"]
                            fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                            print(f"Annalise code as per requirement for {target_obs} observation : {Annalise_code_as_per_req}")
                            print(f"Annalise code from FHIR report for {target_obs} observation : {fhir_annalise_obs_code}")
                            assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"{Annalise_code_as_per_req} from requrirement and {fhir_annalise_obs_code} from FHIR are not matching"
                            with allure.step(f"Verifying Observation code for {target_obs} observation for Annalise coding system"):
                                allure.attach(f"Observation code as per requirement : {Annalise_code_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_code}, ", f"Verifying Observation code for {target_obs} observation for Annalise coding system", allure.attachment_type.TEXT)
                            count+=1
                            print(f"Observation code from FHIR report matches with requirement for {target_obs} observation")
                        except AssertionError as e:
                            failures.append(target_obs)
                            
                            
        print(count)
        if failures:
            print(f"Annalise Observation code mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"Annalise Observation code mismatches are observed in FHIR.json"):
                allure.attach(f"Annalise Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True
    
    
    
    def verify_obs_code_nuance_system(self,fhir_contents):
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        count=0
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            else:
                if self.cxr_req[target_obs][0]["Nuance_coding_system"]==True:
                    Nuance_code_as_per_req = self.cxr_req[target_obs][0]["Nuance_observation.code"]
                    fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
                    print(f"Nuance code as per requirement for {target_obs} observation : {Nuance_code_as_per_req}")
                    print(f"Nuance code from FHIR report for {target_obs} observation : {fhir_nuance_obs_code}")
                    try:
                        assert Nuance_code_as_per_req == fhir_nuance_obs_code, f"{Nuance_code_as_per_req} from requrirement and {fhir_nuance_obs_code} from FHIR are not matching"
                        print(f"Observation code from FHIR report matches with requirement for {target_obs} observation")
                        with allure.step(f"Verifying Observation code for {target_obs} observation for Nuance coding system"):
                            allure.attach(f"Observation code as per requirement : {Nuance_code_as_per_req}, Observation code from FHIR.json : {Nuance_code_as_per_req}, ", f"Verifying Observation code for {target_obs} observation for Nuance coding system", allure.attachment_type.TEXT)
                        count+=1
                    except AssertionError as e:
                        failures.append(target_obs)

        print(count)
        if failures:
            print(f"Nuance Observation code mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"Nuance Observation code mismatches are observed in FHIR.json"):
                allure.attach(f"Nuance Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in Nuance coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True
            
        
    def verify_obs_code_radelement(self,fhir_contents):
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        count=0
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            else:
                if self.cxr_req[target_obs][0]["RadElement_coding_system"]==True:
                    assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                    try:
                        assert self.cxr_req[target_obs][0]["RadElement_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"RadElement coding system text in FHIR does not match with requirement"
                        RadElement_code_as_per_req = self.cxr_req[target_obs][0]["RadElement_observation.code"]
                        fhir_RadElement_obs_code = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                        print(f"RadElement code as per requirement for {target_obs} observation : {RadElement_code_as_per_req}")
                        print(f"RadElement code from FHIR report for {target_obs} observation : {fhir_RadElement_obs_code}")
                        assert RadElement_code_as_per_req == fhir_RadElement_obs_code, f"{RadElement_code_as_per_req} from requrirement and {fhir_RadElement_obs_code} from FHIR are not matching"
                        with allure.step(f"Verifying Observation code for {target_obs} observation for RadElement coding system"):
                            allure.attach(f"Observation code as per requirement : {RadElement_code_as_per_req}, Observation code from FHIR.json : {fhir_RadElement_obs_code}", f"Verifying Observation code for {target_obs} observation for RadElement coding system", allure.attachment_type.TEXT)
                        print(f"Observation code from FHIR report matches with requirement for {target_obs} observation")
                        count+=1
                    except AssertionError as e:
                        failures.append(target_obs)
                    
        print(count)
        if failures:
            print(f"RadElement Observation code mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"RadElement Observation code mismatches are observed in FHIR.json"):
                allure.attach(f"RadElement Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in RadElement coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True


    def verify_obs_display_annalise_system(self,fhir_contents):
        failures = []
        self.cxr_req = conftest.read_cxr_req()
        count=0
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            else:
                if self.cxr_req[target_obs][0]["Annalise_coding_system"]==True:
                    if target_obs in non_nuance_findings:
                        try:
                            assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                            assert self.cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                            Annalise_display_as_per_req = self.cxr_req[target_obs][0]["Annalise_observation.display"]
                            fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                            assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR.json is not matching"
                            with allure.step(f"Verifying Observation display text for {target_obs} observation for Annalise coding system"):
                                allure.attach(f"Observation display text as per requirement : {Annalise_display_as_per_req}, Observation display text from FHIR.json : {fhir_annalise_obs_display}, ", f"Verifying Observation display text for {target_obs} observation - Annalise coding system", allure.attachment_type.TEXT)
                            count+=1
                            print(f"Observation display text from FHIR report matches with requirement for {target_obs} observation")
                        except AssertionError as e:
                            failures.append(target_obs)
                            

                    
                    else:
                        try:
                            assert len(fhir_contents["contained"][observation]["code"]["coding"])==2, f"More than two Coding systems are displayed in FHIR for {target_obs} observation. Only TWO coding systems are expected as per requirement"
                            assert self.cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                            Annalise_display_as_per_req = self.cxr_req[target_obs][0]["Annalise_observation.display"]
                            fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                            assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR.json is not matching"
                            with allure.step(f"Verifying Observation display text for {target_obs} observation for Annalise coding system"):
                                allure.attach(f"Observation display text as per requirement : {Annalise_display_as_per_req}, Observation display text from FHIR.json : {fhir_annalise_obs_display}, ", f"Verifying Observation display text for {target_obs} observation - Annalise coding system", allure.attachment_type.TEXT)
                            count+=1
                            print(f"Observation display text from FHIR report matches with requirement for {target_obs} observation")
                        except AssertionError as e:
                            failures.append(target_obs)
                            
                            
        print(count)
        if failures:
            print(f"Annalise Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"Annalise Observation display text mismatches are observed in FHIR.json"):
                allure.attach(f"Annalise Observation display text mismatches are observed in FHIR.json for {failures} ", f"Observation display text mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True
        
        
        
    def verify_obs_display_nuance_system(self,fhir_contents):
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        count=0
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            else:
                if self.cxr_req[target_obs][0]["Nuance_coding_system"]==True:
                    Nuance_display_as_per_req = self.cxr_req[target_obs][0]["Nuance_observation.display"]
                    fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][1]["display"]
                    try:
                        assert Nuance_display_as_per_req == fhir_nuance_obs_display, f"{Nuance_display_as_per_req} from requrirement and {fhir_nuance_obs_display} from FHIR are not matching"
                        with allure.step(f"Verifying Observation display text for {target_obs} observation for Nuance coding system"):
                            allure.attach(f"Observation display text as per requirement : {Nuance_display_as_per_req}, Observation display text from FHIR.json : {fhir_nuance_obs_display}, ", 
                                            f"Verifying Observation display text for {target_obs} observation - Nuance coding system", allure.attachment_type.TEXT)
                        
                        print(f"Observation code from FHIR report matches with requirement for {target_obs} observation")
                        count+=1
                    except AssertionError as e:
                        failures.append(target_obs)

        print(count)
        if failures:
            print(f"Nuance Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"Nuance Observation display text mismatches are observed in FHIR.json"):
                allure.attach(f"Nuance Observation code mismatches are observed in FHIR.json for {failures} ", 
                              f"Observation display text mismatch found in FHIR.json - Nuance coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True


    def verify_obs_display_radelement(self,fhir_contents):
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        count=0
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            else:
                if self.cxr_req[target_obs][0]["RadElement_coding_system"]==True:
                    assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                    try:
                        assert self.cxr_req[target_obs][0]["RadElement_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"RadElement coding system text in FHIR does not match with requirement"
                        RadElement_display_as_per_req = self.cxr_req[target_obs][0]["RadElement_observation.display"]
                        fhir_RadElement_obs_display = (fhir_contents["contained"][observation]["code"]["coding"][0]["display"])
                        assert RadElement_display_as_per_req == fhir_RadElement_obs_display, f"{RadElement_display_as_per_req} from requrirement and {fhir_RadElement_obs_display} from FHIR are not matching"
                        with allure.step(f"Verifying Observation display text for {target_obs} observation for RadElement coding system"):
                            allure.attach(f"Observation display text as per requirement : {RadElement_display_as_per_req}, Observation display text from FHIR.json : {fhir_RadElement_obs_display}", f"Verifying Observation display text for {target_obs} observation for RadElement coding system", allure.attachment_type.TEXT)
                        print(f"Observation code from FHIR report matches with requirement for {target_obs} observation")
                        count+=1
                        
                    except AssertionError as e:
                        failures.append(target_obs)
                    
        print(count)
        if failures:
            print(f"RadElement Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
            with allure.step(f"RadElement Observation display text mismatches are observed in FHIR.json"):
                allure.attach(f"RadElement Observation display text mismatches are observed in FHIR.json for {failures} ", 
                              f"Observation display text mismatch found in FHIR.json in RadElement coding system", allure.attachment_type.TEXT)
            return False
        else:
            return True






















    # def verify_tracking_uid(self, fhir_contents):
    # # """
    # # Verify the Tracking Unique Identifier for a given observation in the FHIR report.

    # # Parameters:
    # # - observation: Index of the observation.
    # # - fhir_contents: Contents of the FHIR report.

    # # Raises:
    # # - AssertionError: If the Tracking Unique Identifier codes do not match.
    # # """
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]

    #         if target == '246501002':
    #             pass

    #         tracking_uid_presence = self.is_tracking_uid_present(fhir_contents)
    #         assert tracking_uid_presence, f"Tracking Unique Identifier is not present for the observation {target} in FHIR"
    #         for each in range(len(fhir_contents["contained"][observation]["component"])):
    #             code_coding_values = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values()
    #             if 'Tracking Unique Identifier' in code_coding_values:
    #                 tracking_uid_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
    #                 tracking_uid_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]

    #                 assert tracking_uid_code == "112040", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
    #                 assert tracking_uid_display == "Tracking Unique Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"

    
    # def verify_tracking_id(self, fhir_contents):
    # # """
    # # Verify the Tracking Identifier for a given observation in the FHIR report.

    # # Parameters:
    # # - observation: Index of the observation.
    # # - fhir_contents: Contents of the FHIR report.

    # # Raises:
    # # - AssertionError: If the Tracking Unique Identifier codes do not match.
    # # """
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]

    #         if target == '246501002':
    #             pass

    #         tracking_id_presence = self.is_tracking_identifier_present(fhir_contents)
    #         assert tracking_id_presence, f"Tracking Identifier is not present for the observation {target} in FHIR"
    #         for each in range(len(fhir_contents["contained"][observation]["component"])):
    #             code_coding_values = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values()
    #             if 'Tracking Identifier' in code_coding_values:
    #                 tracking_id_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
    #                 tracking_id_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
    #                 assert tracking_id_code == "112039", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
    #                 assert tracking_id_display == "Tracking Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"