import pytest
import time, os, json
from marinaalchemist import BaseClass


class TestDocker(BaseClass):
    
    def test_autorun(self):
        input_path = self.config.get_value_of_test_input_key("input_path_TC321")
        output_path = self.generic_util.output_folder_generator()
        self.docker_util.container_autorun(input_path=input_path, output_path=output_path)
        self.docker_util.check_container_logs()
        files_to_verify = ['Annalise-cxr-FHIR.json', 'resultManifest.json']
        self.generic_util.validate_files_presence(files_to_verify,output_path)  
        resultManifest_contents = self.generic_util.parse_json_file('resultManifest.json', output_path)
        assert resultManifest_contents["status"]["code"] == "ANALYSIS_COMPLETE"
        assert resultManifest_contents["status"]["text"] == "Study Processed Successfully"

            
        
    # def test_autorun(self):
    #     input_path = self.config.get_value_of_test_input_key("input_path_TC1278")
    #     output_path = self.generic_util.output_folder_generator()
    #     print(output_path)
    #     # self.docker_util.container_autorun(input_path=input_path, output_path=output_path)
        











