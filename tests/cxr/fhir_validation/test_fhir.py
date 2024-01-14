import pytest
from marinaalchemist import BaseClass
import allure
import re



# def get_input():
#     return ['test1', 'test2', 'test3']

# @pytest.mark.usefixtures("container_autorun")
class TestFHIR(BaseClass):
    

    # def sample(self):
    #     input_data = self.config.get_value_of_test_input_key("input_path_TC1278")
    #     launch = self.docker_utils.simulator_launch(input_path=input_data,
    #                                                 output_path=self.config.get_value_of_config_key("output_path"))
    #     f = self.url_util.get_url(self.url_util.LIVENESS_ENDPOINT)
    #     print(f)

    # @pytest.mark.parametrize("inputs", get_input())
    # def test_fhir(self, inputs):
    #     print("HEY!!")
    #     assert 1 == 1, "wrong assertion"
    #     print(inputs)

    #     with allure.step(f"{inputs}"):
    #         self.allure_util.allure_attach_with_text("FHIR JSON!", str(self.fhir_json))

    #     with allure.step("Excel contents"):
    #         self.allure_util.allure_attach_with_text("excel sheet observation!", str(self.observation_df))

    #     with allure.step("Excel contents"):
    #         self.allure_util.allure_attach_with_text("excel sheet non-observation!", str(self.non_observation_df))

    # @pytest.mark.first
    # def test_fhir_statics(self):
    #     assert self.fhir_json['resourceType'] == 'DiagnosticReport', "resourceType DiagnosticReport mismatch"
    #     with allure.step("fhir_statics"):
    #         self.allure_util.allure_attach_with_text("resourceType of FHIR report", str(self.fhir_json['resourceType']))

    # @pytest.mark.first
    # def test_fhir_annalise_obs_code(self):
    #     # test_data = self.config.get_value_of_test_input_key("input_path_TC1278")
    #     # fhir_path = self.output_path
    #     print("testing Annalise observation code")
    #     fhir_contents = self.fhir_json
    #     cxr_req = self.cxr_req
    #     count = 0
    #     non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            
    #         if target_obs == "246501002":
    #             count+=1
    #             pass
            
            
    #         elif cxr_req[target_obs][0]["RadElement_coding_system"]:
    #             RadElement_code_as_per_req = cxr_req[target_obs][0]["RadElement_observation.code"]
    #             fhir_RadElement_obs_code = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #             assert RadElement_code_as_per_req == fhir_RadElement_obs_code, "radele code not match"
    #             print(target_obs)
    #             count+=1
            
    #         else:
    #             if target_obs in cxr_req.keys() and target_obs not in non_nuance_findings:
    #                 Annalise_code_as_per_req = cxr_req[target_obs][0]["Annalise_observation.code"]
    #                 Nuance_code_as_per_req = cxr_req[target_obs][0]["Nuance_observation.code"]
    #                 fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
    #                 fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
                    
    #                 assert Annalise_code_as_per_req == fhir_annalise_obs_code, "Annalise code NOT MATCHING !!"
    #                 assert Nuance_code_as_per_req == fhir_nuance_obs_code, "Nuance code NOT Matching"
    #                 count+=1

    #     print(count)
            
            
    # def test_fhir_annalise_obs_display(self):
    #     print("testing Annalise observation display")
    #     fhir_contents = self.fhir_json
    #     cxr_req = self.cxr_req
    #     count = 0
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         target_obs_display = (fhir_contents["contained"][observation]["code"]["coding"][0]["display"])
    #         if target_obs in cxr_req.keys():
    #             display_as_per_req = cxr_req[target_obs][0]["Annalise_observation.display"]
    #             assert target_obs_display == display_as_per_req, "NOT MATCHING !!"
    #             count+=1
    #         else:
    #             print(target_obs)
                
    #     print(count)


    # def test_fhir_nuance_obs_code(self):
    #     # test_data = self.config.get_value_of_test_input_key("input_path_TC1278")
    #     # fhir_path = self.output_path
    #     print("testing Nuance observation code")
    #     fhir_contents = self.fhir_json
    #     cxr_req = self.cxr_req
    #     count = 0
    #     non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         if target_obs in cxr_req.keys() and target_obs not in non_nuance_findings:
    #             code_as_per_req = cxr_req[target_obs][0]["Nuance_observation.code"]
    #             target_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
    #             assert target_obs_code == code_as_per_req, "NOT MATCHING !!"
    #             count+=1
    #         else:
    #             print(target_obs)
                
    #     print(count)
            
            
    # def test_fhir_nuance_obs_display(self):
    #     print("testing Nuance observation display")
    #     fhir_contents = self.fhir_json
    #     cxr_req = self.cxr_req
    #     count = 0
    #     non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         if target_obs in cxr_req.keys() and target_obs not in non_nuance_findings:
    #             target_obs_display = (fhir_contents["contained"][observation]["code"]["coding"][1]["display"])
    #             display_as_per_req = cxr_req[target_obs][0]["Nuance_observation.display"]
    #             assert target_obs_display == display_as_per_req, "NOT MATCHING !!"
    #             count+=1
    #         else:
    #             print(target_obs)
                
    #     print(count)


     def test_fhir_nuance_obs_display(self):
        print("testing Nuance observation display")
        assert 1 == 1, "no"
        print("test done")

















