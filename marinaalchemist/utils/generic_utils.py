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
            
            
    def parse_json_file(self, file_name, folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            file_contents = json.load(file)
        print(f"{file_name} parsed successfully.")
        return file_contents

