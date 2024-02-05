import pytest
from marinaalchemist import BaseClass
import allure
import re


@pytest.mark.usefixtures("container_auto")
class TestKeys(BaseClass):

    
    def test_verify_observation_code(self):
        fhir_contents = self.fhir_contents
        annalise_obs_code_status = self.generic_util.verify_obs_code_annalise_system(fhir_contents)
        nuance_obs_code_status = self.generic_util.verify_obs_code_nuance_system(fhir_contents)
        radelement_obs_code_status = self.generic_util.verify_obs_code_radelement(fhir_contents)
        
        if annalise_obs_code_status is False or nuance_obs_code_status is False or radelement_obs_code_status is False:
            pytest.fail("Test Failed due to observation code mismatch is found in FHIR.json")


        
        # self.generic_util.VERIFY_OBSERVATION_CODE_FOR_ANNALISE_CODING_SYSTEM(fhir_contents)
    
    
    def test_verify_observation_display(self):
        fhir_contents = self.fhir_contents
        annalise_obs_display_status = self.generic_util.verify_obs_display_annalise_system(fhir_contents)
        nuance_obs_display_status = self.generic_util.verify_obs_display_nuance_system(fhir_contents)
        radelement_obs_display_status = self.generic_util.verify_obs_display_radelement(fhir_contents)
        
        if annalise_obs_display_status is False or nuance_obs_display_status is False or radelement_obs_display_status is False:
            pytest.fail("Test Failed due to observation display text mismatch is found in FHIR.json")


    def test_bodySite_code(self):
        fhir_contents = self.fhir_contents
        radlex_code_status = self.generic_util.verify_radlex_code(fhir_contents)
        
        if radlex_code_status is False:
            pytest.fail("Test Failed due to Radlex bodySite code mismatch is found in FHIR.json")