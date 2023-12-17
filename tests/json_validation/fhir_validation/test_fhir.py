import pytest
from marinaalchemist import DockerUtils
from marinaalchemist import BaseClass
import allure
import re



def get_input():
    return ['test1', 'test2', 'test3']


class TestFHIR(BaseClass):

    # def sample(self):
    #     input_data = self.config.get_value_of_test_input_key("input_path_TC1278")
    #     launch = self.docker_utils.simulator_launch(input_path=input_data,
    #                                                 output_path=self.config.get_value_of_config_key("output_path"))
    #     f = self.url_util.get_url(self.url_util.LIVENESS_ENDPOINT)
    #     print(f)

    @pytest.mark.parametrize("inputs", get_input())
    def test_fhir(self, inputs):
        print("HEY!!")
        assert 1 == 1, "wrong assertion"
        print(inputs)

        with allure.step(f"{inputs}"):
            self.allure_util.allure_attach_with_text("FHIR JSON!", str(self.fhir_json))

        with allure.step("Excel contents"):
            self.allure_util.allure_attach_with_text("excel sheet observation!", str(self.observation_df))

        with allure.step("Excel contents"):
            self.allure_util.allure_attach_with_text("excel sheet non-observation!", str(self.non_observation_df))

    @pytest.mark.first
    def test_fhir_statics(self):
        assert self.fhir_json['resourceType'] == 'DiagnosticReport', "resourceType DiagnosticReport mismatch"
        with allure.step("fhir_statics"):
            self.allure_util.allure_attach_with_text("resourceType of FHIR report", str(self.fhir_json['resourceType']))

    @pytest.mark.first
    def test_fhir_static(self):
        test_data = self.config.get_value_of_test_input_key("input_path_TC1278")















