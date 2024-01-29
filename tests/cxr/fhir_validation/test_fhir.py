import pytest
from marinaalchemist import BaseClass
import allure
import re


# @pytest.mark.usefixtures("container_auto")
class TestFHIR(BaseClass):

    '''
    The test_fhir_obs_code verifies the Observation code of Annalise/Nuance/RadElement system displayed in FHIR by comparing it the CXR FHIR requirements
    '''
    def test_fhir_obs_code(self):
        fhir_contents = self.fhir_json
        with allure.step("FHIR contents"):
            self.allure_util.allure_attach_with_text("contents of FHIR report", str(fhir_contents))
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        total_observations_in_fhir = 0
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])        
        
        # non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target_obs == "246501002":
                    pass
                
                else:
                    if cxr_req[target_obs][0]["Annalise_coding_system"] and cxr_req[target_obs][0]["Nuance_coding_system"]:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==2, f"More than two Coding systems are displayed in FHIR for {target_obs} observation. Only TWO coding systems are expected as per requirement"
                        assert cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                        assert cxr_req[target_obs][0]["Nuance_system"] in fhir_contents["contained"][observation]["code"]["coding"][1]["system"],"Nuance coding system text in FHIR does not match with requirement"
                        Annalise_code_as_per_req = cxr_req[target_obs][0]["Annalise_observation.code"]
                        fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                        with allure.step(f"Fetching observation code for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Annalise code as per requirement for {target_obs} observation", str(Annalise_code_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Annalise code from FHIR report for {target_obs} observation", str(fhir_annalise_obs_code))
                        assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"{Annalise_code_as_per_req} from requrirement and {fhir_annalise_obs_code} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation code from FHIR report matches with requirement for {target_obs} observation", str(f"{Annalise_code_as_per_req}, {fhir_annalise_obs_code}"))
                        # print(f"Annalise observation code {Annalise_code_as_per_req} from Requirements and {fhir_annalise_obs_code} from FHIR json is matching")
                        Nuance_code_as_per_req = cxr_req[target_obs][0]["Nuance_observation.code"]
                        fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
                        with allure.step(f"Fetching observation code for {target_obs} observation - NUANCE coding system"):
                            self.allure_util.allure_attach_with_text(f"Nuance code as per requirement for {target_obs} observation", str(Nuance_code_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Nuance code from FHIR report for {target_obs} observation", str(fhir_nuance_obs_code))
                        assert Nuance_code_as_per_req == fhir_nuance_obs_code, f"{Nuance_code_as_per_req} from requrirement and {fhir_nuance_obs_code} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - NUANCE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation code from FHIR report matches with requirement for {target_obs} observation", str(f"{Nuance_code_as_per_req}, {fhir_nuance_obs_code}"))
                        # print(f"Nuance observation code {Nuance_code_as_per_req} from Requirements and {fhir_nuance_obs_code} from FHIR json is matching")

                    
                    elif cxr_req[target_obs][0]["RadElement_coding_system"]:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                        assert cxr_req[target_obs][0]["RadElement_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"RadElement coding system text in FHIR does not match with requirement"
                        RadElement_code_as_per_req = cxr_req[target_obs][0]["RadElement_observation.code"]
                        fhir_RadElement_obs_code = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                        with allure.step(f"Fetching observation code for {target_obs} observation - RADELEMENT coding system"):
                            self.allure_util.allure_attach_with_text(f"RadElement code as per requirement for {target_obs} observation", str(RadElement_code_as_per_req))
                            self.allure_util.allure_attach_with_text(f"RadElement code from FHIR report for {target_obs} observation", str(fhir_RadElement_obs_code))
                        assert RadElement_code_as_per_req == fhir_RadElement_obs_code, f"{RadElement_code_as_per_req} from requrirement and {fhir_RadElement_obs_code} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - RADELEMENT coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation code from FHIR report matches with requirement for {target_obs} observation", str(f"{RadElement_code_as_per_req}, {fhir_RadElement_obs_code}"))
                        # print(f"RadElement observation code {RadElement_code_as_per_req} from Requirements and {fhir_RadElement_obs_code} from FHIR json is matching")

                    elif cxr_req[target_obs][0]["Annalise_coding_system"]==True and cxr_req[target_obs][0]["Nuance_coding_system"]==False:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                        assert cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                        Annalise_code_as_per_req = cxr_req[target_obs][0]["Annalise_observation.code"]
                        fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                        with allure.step(f"Fetching observation code for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Annalise code as per requirement for {target_obs} observation", str(Annalise_code_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Annalise code from FHIR report for {target_obs} observation", str(fhir_annalise_obs_code))
                        assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"{Annalise_code_as_per_req} from requrirement and {fhir_annalise_obs_code} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation code from FHIR report matches with requirement for {target_obs} observation", str(f"{Annalise_code_as_per_req}, {fhir_annalise_obs_code}"))
                        # print(f"Annalise observation code {Annalise_code_as_per_req} from Requirements and {fhir_annalise_obs_code} from FHIR json is matching")


        except Exception as e:
            print(f"An exception occurred: {e}")
            pytest.fail(f"Test failed due to exception: {e}")
            

    '''
    The test_fhir_obs_display verifies the Observation's Display of Annalise/Nuance/RadElement system displayed in FHIR by comparing it the CXR FHIR requirements
    ''' 
    def test_fhir_obs_display(self):
        print("testing observation Display")
        fhir_contents = self.fhir_json
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target_obs == "246501002":
                    count+=1
                    pass
                
                else:
                    if cxr_req[target_obs][0]["Annalise_coding_system"] and cxr_req[target_obs][0]["Nuance_coding_system"]:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==2, f"More than two Coding systems are displayed in FHIR for {target_obs} observation. Only TWO coding systems are expected as per requirement"
                        assert cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                        assert cxr_req[target_obs][0]["Nuance_system"] in fhir_contents["contained"][observation]["code"]["coding"][1]["system"],"Nuance coding system text in FHIR does not match with requirement"
                        Annalise_display_as_per_req = cxr_req[target_obs][0]["Annalise_observation.display"]
                        fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR are not matching"
                        print(f"Annalise observation display {Annalise_display_as_per_req} from Requirements and {fhir_annalise_obs_display} from FHIR json is matching")
                        Nuance_display_as_per_req = cxr_req[target_obs][0]["Nuance_observation.display"]
                        fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][1]["display"]
                        assert Nuance_display_as_per_req == fhir_nuance_obs_display, f"{Nuance_display_as_per_req} from requrirement and {fhir_nuance_obs_display} from FHIR are not matching"
                        print(f"Nuance observation display {Nuance_display_as_per_req} from Requirements and {fhir_nuance_obs_display} from FHIR json is matching")

                    
                    elif cxr_req[target_obs][0]["RadElement_coding_system"]:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                        assert cxr_req[target_obs][0]["RadElement_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"RadElement coding system text in FHIR does not match with requirement"
                        RadElement_display_as_per_req = cxr_req[target_obs][0]["RadElement_observation.display"]
                        fhir_RadElement_obs_display = (fhir_contents["contained"][observation]["code"]["coding"][0]["display"])
                        assert RadElement_display_as_per_req == fhir_RadElement_obs_display, "radele code not match"
                        print(f"RadElement observation display {RadElement_display_as_per_req} from Requirements and {fhir_RadElement_obs_display} from FHIR json is matching")
                        
                    elif cxr_req[target_obs][0]["Annalise_coding_system"]==True and cxr_req[target_obs][0]["Nuance_coding_system"]==False:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                        assert cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                        Annalise_display_as_per_req = cxr_req[target_obs][0]["Annalise_observation.display"]
                        fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR are not matching"
                        print(f"Annalise observation display {Annalise_display_as_per_req} from Requirements and {fhir_annalise_obs_display} from FHIR json is matching")

        except Exception as e:
            print(f"An exception occurred: {e}")
        
        
    '''
    The test_obs_bodsite_code verifies the Observation's bodySite of Snomed & Radlex systems displayed in FHIR by comparing it the CXR FHIR requirements
    ''' 
    def test_obs_bodsite_code(self):
        print("testing observation Bodysite Code")
        fhir_contents = self.fhir_json
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req

        # try:
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
                pass
            
            elif target == "RDES230": # This block verifies the bodySite of Vertebral Compression Fracture Observation observation
                self.generic_util.verify_radlex_code(target,observation,fhir_contents)
            
            elif target == "RDES225": # This block verifies the bodySite of Chest Radiograph Pulmonary Nodules observation
                self.generic_util.verify_observation_225(observation,fhir_contents)
                
            else: # This block verifies the bodySite of all observations other than Vertebral Compression Fracture and Chest Radiograph Pulmonary Nodules
                self.generic_util.verify_snomed_code(target,observation,fhir_contents)
                self.generic_util.verify_radlex_code(target,observation,fhir_contents)
                

        # except Exception as e:
        #     print(f"An exception occurred: {e}")
    
    
    # def test_study_uid(self):
    #     print("testing observation Study instance UID")
    #     fhir_contents = self.fhir_json
    #     assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
    #     cxr_req = self.cxr_req
    #     try:
    #         study_uid_presence = self.generic_util.is_study_uid_present(fhir_contents)
    #         assert study_uid_presence, f"Study Instance UID is not present for one of the observation in FHIR"
    #         dicom_study_uid = self.dicom_util.extract_study_uid(self.fhir_input_path)
    #         fhir_study_uid = self.generic_util.extract_fhir_study_uid(fhir_contents)
    #         assert dicom_study_uid == fhir_study_uid, "Study Instance UID not matching !!"
    #     except Exception as e:
    #         print(f"An exception occurred: {e}")
    #         pytest.fail(f"Test failed: {e}")
            
            
    def test_fhir_tracking_id(self):
        print("testing FHIR Tracking Identifier")
        fhir_contents = self.fhir_json
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target == '246501002':
                    pass
                else:
                    tracking_identifier_presence = self.generic_util.is_tracking_identifier_present(fhir_contents)
                    assert tracking_identifier_presence, f"Tracking Identifiier is not present for one of the observation in FHIR"
                    for each in range(len(fhir_contents["contained"][observation]["component"])):
                        if 'Tracking Identifier' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                            tracking_id_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                            tracking_id_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                            assert tracking_id_code == "112039", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
                            assert tracking_id_display == "Tracking Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"

        except Exception as e:
            print(f"An exception occurred: {e}")
            pytest.fail(f"Test failed: {e}")
    
    def test_fhir_tracking_uid(self):
        print("testing FHIR Tracking Unique Identifier")
        fhir_contents = self.fhir_json
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target == '246501002':
                    pass
                else:
                    tracking_uid_presence = self.generic_util.is_tracking_uid_present(fhir_contents)
                    assert tracking_uid_presence, f"Tracking Unique Identifiier is not present for one of the observation in FHIR"
                    for each in range(len(fhir_contents["contained"][observation]["component"])):
                        if 'Tracking Unique Identifier' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                            tracking_uid_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                            tracking_uid_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                            assert tracking_uid_code == "112040", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
                            assert tracking_uid_display == "Tracking Unique Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"

    
        except Exception as e:
            print(f"An exception occurred: {e}")
            pytest.fail(f"Test failed: {e}")








