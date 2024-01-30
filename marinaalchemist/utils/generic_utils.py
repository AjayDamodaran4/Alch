import os, json, allure, pytest
from .config_reader import Config
import conftest

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
    
    def extract_fhir_study_uid(self, fhir_input):
        try:
            for observation in range(3,len(fhir_input['contained'])):
                target = (fhir_input["contained"][observation]["code"]["coding"][0]["code"])
                if target == '246501002':
                    pass
                else:
                    for each in range(len(fhir_input["contained"][observation]["component"])):
                        if 'Study Instance UID' in fhir_input["contained"][observation]["component"][each]["code"]["coding"][0].values():
                            study_uid = fhir_input["contained"][observation]["component"][each]["valueString"]
                            return study_uid
        except Exception as e:
            print(f"Error extracting Study UID: {e}")
            return None
        
        
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
            return True
        else:
            return False

    def is_study_uid_present(self,fhir_json_data):
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
                if "Study Instance UID" in components_data:
                    components_data = []
                else:
                    tracking_identifier_presenence = False
                    tracking_id_absence.append(target)
                    
        if tracking_identifier_presenence:
            return True
        else:
            return False
        
    def is_tracking_uid_present(self,fhir_json_data):
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
                if "Tracking Unique Identifier" in components_data:
                    components_data = []
                else:
                    tracking_identifier_presenence = False
                    tracking_id_absence.append(target)
                    
        if tracking_identifier_presenence:
            return True
        else:
            return False
        
        
    def verify_snomed_code(self,target,observation, fhir_contents):
        self.cxr_req = conftest.read_cxr_req()

        bodySite_snomed_code_as_per_req = self.cxr_req[target][0]["bodySite_Snomed.code"]
        fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
    # with allure.step(f"Fetching Snomed bodySite code for {target} observation"):
    #     allure.attach(f"{bodySite_snomed_code_as_per_req}", "Snomed bodySite code for {target} observation as per requirement", allure.attachment_type.TEXT)
    #     allure.attach(f"{fhir_bodySite_snomed_code}", "Snomed bodySite code for {target} observation from FHIR.json", allure.attachment_type.TEXT)
    
        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
    
        with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
            allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
                        From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Snomed bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)

        
        print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")



    def verify_radlex_code(self,target,observation, fhir_contents):
        self.cxr_req = conftest.read_cxr_req()

        bodySite_radlex_code_as_per_req = self.cxr_req[target][0]["bodySite_Radlex.code"]
        if target == "RDES230":
        # Special case: Set fhir_bodySite_radlex_code from a different coding index
            fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
        else:
            fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
            assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
    
        with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
            allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
                        From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
        print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")

        
        
    def verify_observation_225(self, observation, fhir_contents):

    # Verify the bodySite for the Chest Radiograph Pulmonary Nodules observation (RDES225).

    # Parameters:
    # - observation: Index of the observation.
    # - fhir_contents: Contents of the FHIR report.

    # Raises:
    # - AssertionError: If the bodySite codes do not match.

        target = "RDES225"
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
        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, \
            f"SNOMED code mismatch: Expected {bodySite_snomed_code_as_per_req}, but got {fhir_bodySite_snomed_code} for {target} observation, {sub_key}"
        with allure.step(f"Verification of Snomed bodySite code for {target} observation"):
            allure.attach(f"Snomed bodySite code from FHIR matches with the requirement for {target} observation \
                From requirement : {bodySite_snomed_code_as_per_req}, From FHIR.json : {fhir_bodySite_snomed_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
        

        bodySite_radlex_code_as_per_req = self.cxr_req[target][key][sub_key][0]["bodySite_Radlex.code"]
        fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
        assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, \
            f"Radlex code mismatch: Expected {bodySite_radlex_code_as_per_req}, but got {fhir_bodySite_radlex_code} for {target} observation"
        with allure.step(f"Verification of Radlex bodySite code for {target} observation"):
            allure.attach(f"Radlex bodySite code from FHIR matches with the requirement for {target} observation \
                From requirement : {bodySite_radlex_code_as_per_req}, From FHIR.json : {fhir_bodySite_radlex_code}", f"Verification of Radlex bodySite code for {target} observation against requirement", allure.attachment_type.TEXT)
       
            
        print(f"BodySite SNOMED code {bodySite_snomed_code_as_per_req} and Radlex code {bodySite_radlex_code_as_per_req} "
            f"from Requirements match with {fhir_bodySite_snomed_code} and {fhir_bodySite_radlex_code} from FHIR json for {target} observation, {sub_key}")


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