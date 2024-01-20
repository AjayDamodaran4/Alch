import pytest
from marinaalchemist import BaseClass


class TestDicom(BaseClass):
    
    def test_study(self):
        input_path = self.config.get_value_of_test_input_key("input_path_TC321")
        study_uid = self.dicom_util.extract_study_uid(input_path)
        print(study_uid)