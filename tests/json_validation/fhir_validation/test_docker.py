import pytest
import time, os, json
from marinaalchemist import BaseClass


class TestDocker(BaseClass):
    
    # def test_autorun(self):
    #     input_path = self.config.get_value_of_test_input_key("input_path_TC1278")
    #     output_path = "/nuance/output/aut"
    #     self.docker_util.container_autorun(input_path=input_path, output_path=output_path)
    #     self.docker_util.check_container_logs()
    #     files_to_assert = ['Annalise-cxr-FHIR.json', 'resultManifest.json']
    #     for file in files_to_assert:
    #         file_path = os.path.join(output_path, file)
    #         assert os.path.isfile(file_path), f"File {file} not found in {output_path}"
            
    #     resultManifest_path = os.path.join(output_path, 'resultManifest.json')
    #     with open(resultManifest_path, 'r') as file: 
    #         resultManifest_contents = json.load(file)
        
    #     assert resultManifest_contents["status"]["code"] == "ANALYSIS_COMPLETE"
    #     assert resultManifest_contents["status"]["text"] == "Study Processed Successfully"
        
        
    def test_autorun(self):
        input_path = self.config.get_value_of_test_input_key("input_path_TC1278")
        output_path = self.generic_util.output_folder_generator()
        print(output_path)
        # self.docker_util.container_autorun(input_path=input_path, output_path=output_path)
        











