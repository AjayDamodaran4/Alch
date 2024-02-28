import pytest
from marinaalchemist import BaseClass
import allure
import re


# @pytest.mark.usefixtures("container_auto")
class TestKeys(BaseClass):

    
    def test_verify_observation_code(self):
        fhir_contents = self.fhir_contents
        
        self.allure_util.allure_test_title("title_test_verify_observation_code")
        self.allure_util.allure_test_description("description_test_verify_observation_code")
        
        # annalise_obs_code_status = self.fhir_keyword.VERIFY_OBSERVATION_CODE_FOR_ANNALISE_CODING_SYSTEM(fhir_contents)
        
        annalise_obs_code_status = self.generic_util.verify_obs_code_annalise_system(fhir_contents)
        nuance_obs_code_status = self.generic_util.verify_obs_code_nuance_system(fhir_contents)
        radelement_obs_code_status = self.generic_util.verify_obs_code_radelement(fhir_contents)
        
        if annalise_obs_code_status is False or nuance_obs_code_status is False or radelement_obs_code_status is False:
            pytest.fail("Test Failed due to observation code mismatch is found in FHIR.json")
        
        

        
        # self.generic_util.VERIFY_OBSERVATION_CODE_FOR_ANNALISE_CODING_SYSTEM(fhir_contents)
    # fhir_keyword
    
    
    
    def test_verify_observation_display(self):
        fhir_contents = self.fhir_contents
        self.allure_util.allure_test_title("title_test_verify_observation_display")
        self.allure_util.allure_test_description("description_test_verify_observation_display")
        
        annalise_obs_display_status = self.generic_util.verify_obs_display_annalise_system(fhir_contents)
        nuance_obs_display_status = self.generic_util.verify_obs_display_nuance_system(fhir_contents)
        radelement_obs_display_status = self.generic_util.verify_obs_display_radelement(fhir_contents)
        
        if annalise_obs_display_status is False or nuance_obs_display_status is False or radelement_obs_display_status is False:
            pytest.fail("Test Failed due to observation display text mismatch is found in FHIR.json")




    def test_bodySite_code(self):
        fhir_contents = self.fhir_json
        self.allure_util.allure_test_title("title_test_bodySite_code")
        self.allure_util.allure_test_description("description_test_bodySite_code")
        
        radlex_code_status = self.generic_util.verify_radlex_code(fhir_contents)
        snomed_code_status = self.generic_util.verify_snomed_code(fhir_contents)
        
        
        if radlex_code_status is False or snomed_code_status is False:
            pytest.fail("Test Failed due to Radlex/Snomed bodySite code mismatch is found in FHIR.json")
            
            
            
    def test_st_uid(self):
        fhir_contents = self.fhir_contents
        self.allure_util.allure_test_title("title_test_st_uid")
        self.allure_util.allure_test_description("description_test_st_uid")
        
        self.generic_util.is_study_uid_present(fhir_contents)
        
        dicom_study_uid = self.dicom_util.extract_study_uid(self.fhir_input_path)
        
        self.generic_util.verify_study_uid(dicom_study_uid,fhir_contents)
        
        
    
    def test_fhir_track_id(self):
        
        fhir_contents = self.fhir_contents
        self.allure_util.allure_test_title("title_test_fhir_track_id")
        self.allure_util.allure_test_description("description_test_fhir_track_id")
        
        self.generic_util.is_tracking_identifier_present(fhir_contents)
        self.generic_util.verify_fhir_tracking_id(fhir_contents)
        
        
        
    def test_fhir_track_uid(self):
        
        fhir_contents = self.fhir_contents
        self.allure_util.allure_test_title("title_test_fhir_track_uid")
        self.allure_util.allure_test_description("description_test_fhir_track_uid")
        
        self.generic_util.is_tracking_uid_present(fhir_contents)
        
        self.generic_util.verify_fhir_tracking_uid(fhir_contents)
        
        
    def test_sample(self):
        
        fhir_contents = self.fhir_json
        model_output_contents = self.model_output_json
        
        
        status = self.fhir_util.verify_probability(fhir_contents,'RoW',"radlex")
        print(status)
        # status = self.generic_util.verify_observation_code(fhir_contents,"uS","AnnaliSE","NUance","radelement")
        # # self.generic_util.verify_observation_display(fhir_contents,"uS","AnnaliSE","NUance")
        
        if not status:
            pytest.fail("failed")

        
        
        
        
        # max_value = max(self.model_output_json['cxr_value']['study_laterality']['findings']['abdominal_clips']['values'].values())
        # print(max_value)
        
        # print(op)
        
        # for i in op : 
        
        '''
        parse fhir json
        parse model output
        if obs.code of finding from fhir.json matches in model output, 
            - get key of max value of model output for that code
            - In component of finding of fhir.json, verify above and value of 'display' is same
            - then, the value of code should match as per req
            - then value of valueQuantity should match with the max value %
            - 
            
        code should match for nuance and radele as well
        '''
            
        
        
        
        
        
        
    