import os, json
from .config_reader import Config


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