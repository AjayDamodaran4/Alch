import pytest
from marinaalchemist import BaseClass


class TestDocker(BaseClass):

    def test_autorun(self):
        input_path = self.config.get_value_of_test_input_key("input_path_TC1278")
        output_path = self.generic_util.output_folder_generator
        self.docker_utils.container_autorun(input=input_path, output_path=output_path)


















