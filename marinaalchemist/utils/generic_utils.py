import os
from config_reader import Config


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

        return new_folder_path
