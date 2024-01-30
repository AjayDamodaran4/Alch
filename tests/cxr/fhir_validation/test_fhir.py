import pytest
from marinaalchemist import BaseClass
import allure
import re


@pytest.mark.usefixtures("container_auto")
class TestFHIR(BaseClass):
    


    def test_fhir_obs_code(self):
        
        allure.dynamic.title("Verification of Observation code for all the findings in FHIR.json")
        allure.dynamic.description("""This test verifies the Observation code (as per Annalise/Nuance/RadElement coding system) 
                                   for all the findings in FHIR.json against the requirement""")
        
        fhir_contents = self.fhir_contents
        with allure.step("FHIR contents"):
            self.allure_util.allure_attach_with_text("contents of FHIR report", str(fhir_contents))
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        failures = []
        total_observations_in_fhir = 0
        
        for observation in range(3,len(fhir_contents['contained'])):
            total_observations_in_fhir+=1
        
        with allure.step(f"Total Number of Observations present in FHIR"):
            self.allure_util.allure_attach_with_text(f"Total Number of Observations present in FHIR",str(total_observations_in_fhir))
        # non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            
            if target_obs == "246501002":
                pass
            
            else:
                if cxr_req[target_obs][0]["Annalise_coding_system"] and cxr_req[target_obs][0]["Nuance_coding_system"]:
                    try:
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
                    except AssertionError as e:
                        failures.append(f"ANNALISE Observation code not matching for : {target_obs}, ")
                        
                        
                    try:   
                        Nuance_code_as_per_req = cxr_req[target_obs][0]["Nuance_observation.code"]
                        fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
                        with allure.step(f"Fetching observation code for {target_obs} observation - NUANCE coding system"):
                            self.allure_util.allure_attach_with_text(f"Nuance code as per requirement for {target_obs} observation", str(Nuance_code_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Nuance code from FHIR report for {target_obs} observation", str(fhir_nuance_obs_code))
                        assert Nuance_code_as_per_req == fhir_nuance_obs_code, f"{Nuance_code_as_per_req} from requrirement and {fhir_nuance_obs_code} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - NUANCE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation code from FHIR report matches with requirement for {target_obs} observation", str(f"{Nuance_code_as_per_req}, {fhir_nuance_obs_code}"))
                    except AssertionError as e:
                        failures.append(f"NUANCE Observation code not matching for : {target_obs}, ")
                        
                            
                elif cxr_req[target_obs][0]["RadElement_coding_system"]:
                    try:
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
                    except AssertionError as e:
                        failures.append(f"RADELEMENT Observation code not matching for : {target_obs}, ")

                elif cxr_req[target_obs][0]["Annalise_coding_system"]==True and cxr_req[target_obs][0]["Nuance_coding_system"]==False:
                    try:
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
                    except AssertionError as e:
                        failures.append(f"ANNALISE Observation code not matching for : {target_obs}, ")
                        
                        
        
        if failures:
            with allure.step("Failures"):
                self.allure_util.allure_attach_with_text(f"Observation code mismatches are observed in FHIR.json for following observations ", str(failures))
            pytest.fail(f"Test failed")
            


    def test_fhir_obs_display(self):
        allure.dynamic.title("Verification of Observation display text for all the findings in FHIR.json")
        allure.dynamic.description("""This test verifies the Observation display text (as per Annalise/Nuance/RadElement coding system) 
                                   for all the findings in FHIR.json against the requirement""")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        failures = []


        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            
            else:
                if cxr_req[target_obs][0]["Annalise_coding_system"] and cxr_req[target_obs][0]["Nuance_coding_system"]:
                    try: 
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==2, f"More than two Coding systems are displayed in FHIR for {target_obs} observation. Only TWO coding systems are expected as per requirement"
                        assert cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                        assert cxr_req[target_obs][0]["Nuance_system"] in fhir_contents["contained"][observation]["code"]["coding"][1]["system"],"Nuance coding system text in FHIR does not match with requirement"
                        Annalise_display_as_per_req = cxr_req[target_obs][0]["Annalise_observation.display"]
                        fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                        with allure.step(f"Fetching observation display for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Annalise display as per requirement for {target_obs} observation", str(Annalise_display_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Annalise display from FHIR report for {target_obs} observation", str(fhir_annalise_obs_display))
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation display from FHIR report matches with requirement for {target_obs} observation", str(f"{Annalise_display_as_per_req}, {fhir_annalise_obs_display}"))
                    except AssertionError as e:
                        failures.append(f"ANNALISE Observation display text not matching for : {target_obs}, ")
                        
                        
                    try:    
                        Nuance_display_as_per_req = cxr_req[target_obs][0]["Nuance_observation.display"]
                        fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][1]["display"]
                        with allure.step(f"Fetching observation display for {target_obs} observation - NUANCE coding system"):
                            self.allure_util.allure_attach_with_text(f"Nuance display as per requirement for {target_obs} observation", str(Nuance_display_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Nuance display from FHIR report for {target_obs} observation", str(fhir_nuance_obs_display))
                        assert Nuance_display_as_per_req == fhir_nuance_obs_display, f"{Nuance_display_as_per_req} from requrirement and {fhir_nuance_obs_display} from FHIR are not matching"
                        with allure.step(f"Verification of Observation display for {target_obs} observation - NUANCE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation display from FHIR report matches with requirement for {target_obs} observation", str(f"{Nuance_display_as_per_req}, {fhir_nuance_obs_display}"))
                    except AssertionError as e:
                        failures.append(f"NUANCE Observation display text not matching for : {target_obs}, ")

                
                elif cxr_req[target_obs][0]["RadElement_coding_system"]:
                    try:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                        assert cxr_req[target_obs][0]["RadElement_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"RadElement coding system text in FHIR does not match with requirement"
                        RadElement_display_as_per_req = cxr_req[target_obs][0]["RadElement_observation.display"]
                        fhir_RadElement_obs_display = (fhir_contents["contained"][observation]["code"]["coding"][0]["display"])
                        with allure.step(f"Fetching observation code for {target_obs} observation - RADELEMENT coding system"):
                            self.allure_util.allure_attach_with_text(f"RadElement display as per requirement for {target_obs} observation", str(RadElement_display_as_per_req))
                            self.allure_util.allure_attach_with_text(f"RadElement display from FHIR report for {target_obs} observation", str(fhir_RadElement_obs_display))
                        assert RadElement_display_as_per_req == fhir_RadElement_obs_display, "radele code not match"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - RADELEMENT coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation display from FHIR report matches with requirement for {target_obs} observation", str(f"{RadElement_display_as_per_req}, {fhir_RadElement_obs_display}"))
                        # print(f"RadElement observation display {RadElement_display_as_per_req} from Requirements and {fhir_RadElement_obs_display} from FHIR json is matching")
                    except AssertionError as e:
                        failures.append(f"RADELEMENT Observation display text not matching for : {target_obs}, ")
                        
                elif cxr_req[target_obs][0]["Annalise_coding_system"]==True and cxr_req[target_obs][0]["Nuance_coding_system"]==False:
                    try:
                        assert len(fhir_contents["contained"][observation]["code"]["coding"])==1, f"More than one Coding systems are displayed in FHIR for {target_obs} observation. Only one coding system is expected as per requirement"
                        assert cxr_req[target_obs][0]["Annalise_system"] in fhir_contents["contained"][observation]["code"]["coding"][0]["system"],"Annalise coding system text in FHIR does not match with requirement"
                        Annalise_display_as_per_req = cxr_req[target_obs][0]["Annalise_observation.display"]
                        fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                        with allure.step(f"Fetching observation display for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Annalise display as per requirement for {target_obs} observation", str(Annalise_display_as_per_req))
                            self.allure_util.allure_attach_with_text(f"Annalise display from FHIR report for {target_obs} observation", str(fhir_annalise_obs_display))
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR are not matching"
                        with allure.step(f"Verification of Observation code for {target_obs} observation - ANNALISE coding system"):
                            self.allure_util.allure_attach_with_text(f"Observation display from FHIR report matches with requirement for {target_obs} observation", str(f"{Annalise_display_as_per_req}, {fhir_annalise_obs_display}"))
                        # print(f"Annalise observation display {Annalise_display_as_per_req} from Requirements and {fhir_annalise_obs_display} from FHIR json is matching")
                    except AssertionError as e:
                        failures.append(f"ANNALISE Observation display text not matching for : {target_obs}, ")

        if failures:
            with allure.step("Failures"):
                self.allure_util.allure_attach_with_text(f"Observation code mismatches are observed in FHIR.json for following observations ", str(failures))
            pytest.fail(f"Test failed")
        
        
        
        
        
    '''
    The test_obs_bodsite_code verifies the Observation's bodySite of Snomed & Radlex systems displayed in FHIR by comparing it the CXR FHIR requirements
    ''' 
    def test_obs_bodsite_code(self):
        allure.dynamic.title("Verification of Observation's bodySite code for all the findings in FHIR.json")
        allure.dynamic.description("""This test verifies the Observation's bodySite code (as per Snomed & Radlex coding systems)
                                   for all the findings in FHIR.json against the requirement""")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        failures = []
        
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            
            if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
                pass
            
            elif target == "RDES230": # This block verifies the bodySite of Vertebral Compression Fracture Observation
                try:
                    self.generic_util.verify_radlex_code(target,observation,fhir_contents)
                except Exception as e:
                    failures.append(target)
            elif target == "RDES225": # This block verifies the bodySite of Chest Radiograph Pulmonary Nodules observation
                try:    
                    self.generic_util.verify_observation_225(observation,fhir_contents)
                except Exception as e:
                    failures.append(target)
            else: # This block verifies the bodySite of all observations other than Vertebral Compression Fracture and Chest Radiograph Pulmonary Nodules
                try:
                    self.generic_util.verify_snomed_code(target,observation,fhir_contents)
                    self.generic_util.verify_radlex_code(target,observation,fhir_contents)
                except Exception as e:
                    failures.append(target)
    
        if failures:
            print(f"few: {failures}")
            with allure.step("Failures"):
                allure.attach(f"{failures}",f"Snomed/Radlex bodySite code mismatches are observed in FHIR.json for following observations :", allure.attachment_type.TEXT)
            pytest.fail(f"Test failed due to bodySite code mismatches are observed in FHIR.json")
            
            
            
            
            
            
    def test_study_uid(self):
        allure.dynamic.title("Verification of Study Instance UID code for all the findings in FHIR.json")
        allure.dynamic.description("""This test verifies if the study Instance UID is present for all the findings in FHIR.json 
                                   and if the Study UID from FHIR.json matches with the study UID from the input DICOM image's metadata""")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"

        study_uid_presence = self.generic_util.is_study_uid_present(fhir_contents)
        try:
            assert study_uid_presence==True, f"Study Instance UID is not present for {study_uid_presence} observations in FHIR"
            with allure.step(f"Verification of presence of Study Instance UID in all the Observations"):
                self.allure_util.allure_attach_with_text(f"Study Instance UID is present for all the observation in FHIR.json", str(f"No issues found"))
        except AssertionError as e:
            print(f"study UID absent for {study_uid_presence}")
            with allure.step(f"Study Instance UID is absent for following observations"):
                self.allure_util.allure_attach_with_text(f"Study Instance UID is absent for following observations", str(study_uid_presence))
            pytest.fail(f"Test failed since Study Instance UID is absent for {study_uid_presence} observations in FHIR.json")

        dicom_study_uid = self.dicom_util.extract_study_uid(self.fhir_input_path)
        fhir_study_uid = self.generic_util.extract_fhir_study_uid(fhir_contents)
        try:
            assert dicom_study_uid == fhir_study_uid, "Study Instance UID not matching !!"
            with allure.step(f"Verification of Study Instance UID"):
                self.allure_util.allure_attach_with_text(f"Study Instance UID from FHIR.json and DICOM metadata matches. No issues found.", \
                    str(f"From DICOM metadata : {dicom_study_uid}, From FHIR.json : {fhir_study_uid}"))
            
        except AssertionError as e:
            print(f"study UID does not match for one of the observation")
            with allure.step(f"Study Instance UID does not match"):
                self.allure_util.allure_attach_with_text(f"Study Instance UID does not match between DICOM metadata and FHIR.json", str("No attachments"))
            pytest.fail(f"Test failed since Study Instance UID does not match between DICOM metadata and FHIR.json")
            
            
            
            
            
            
    def test_fhir_tracking_id(self):
        allure.dynamic.title("Verification of Tracking Identifier for all the findings in FHIR.json")
        allure.dynamic.description("""This test verifies if the Tracking Identifier is present for all the findings in FHIR.json 
                                   and if the Tracking Identifier's code and display from FHIR.json matches with the requirement""")
        
        fhir_contents = self.fhir_contents
        failures = []
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        tracking_identifier_presence = self.generic_util.is_tracking_identifier_present(fhir_contents)
        
        try:
            assert tracking_identifier_presence==True, f"Tracking Identifiier is not present for {tracking_identifier_presence} observation in FHIR"
        except AssertionError as e:
            print(f"Tracking Identifier is absent for {tracking_identifier_presence}")
            with allure.step(f"Tracking Identifier is absent for following observations"):
                self.allure_util.allure_attach_with_text(f"Tracking Identifier is absent for following observations", str(tracking_identifier_presence))
            pytest.fail(f"Test failed since Tracking Identifier is absent for {tracking_identifier_presence} observations in FHIR.json")
               
                    
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target == '246501002':
                pass
            else:
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    if 'Tracking Identifier' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                        tracking_id_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                        tracking_id_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                        try:
                            assert tracking_id_code == "112039", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
                            assert tracking_id_display == "Tracking Identifier", f"Tracking ID Display of {target} observation from FHIR report does not match the requirement"
                            with allure.step(f"Verification of Tracking Identifier for {target} observation"):
                                allure.attach(f"Tracking Identifier code from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID code: 112039, From FHIR.json Tracking ID code: {tracking_id_code}", f"Verification of Tracking Identifier code for {target} observation against requirement", allure.attachment_type.TEXT)
                                allure.attach(f"Tracking Identifier display from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID display: Tracking Identifier, From FHIR.json Tracking ID display: {tracking_id_display}", f"Verification of Tracking Identifier display for {target} observation against requirement", allure.attachment_type.TEXT)
                        except AssertionError :
                            failures.append(target)
                            
            
        if failures:
            print(f"few : {failures}")
            with allure.step(f"Failures"):
                self.allure_util.allure_attach_with_text(f"Tracking Identifier from FHIR.json does not match with the requirements for following observations", str(failures))
            pytest.fail(f"Test failed due to Tracking Identifier from FHIR.json does not match with requirement")
    
    
    
    
    
    
    
    
    def test_fhir_tracking_uid(self):
        allure.dynamic.title("Verification of Tracking Unique Identifier for all the findings in FHIR.json")
        allure.dynamic.description("""This test verifies if the Tracking Unique Identifier is present for all the findings in FHIR.json 
                                   and if the Tracking Identifier's code and display from FHIR.json matches with the requirement""")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        failures = []
        tracking_uid_presence = self.generic_util.is_tracking_uid_present(fhir_contents)
        
        try:
            assert tracking_uid_presence==True, f"Tracking Unique Identifiier is not present for {tracking_uid_presence} observation in FHIR"
        except AssertionError as e:
            print(f"Tracking Unique Identifier is absent for {tracking_uid_presence}")
            with allure.step(f"Tracking Unique Identifier is absent for following observations"):
                self.allure_util.allure_attach_with_text(f"Tracking Unique Identifier is absent for following observations", str(tracking_uid_presence))
            pytest.fail(f"Test failed since Tracking Unique Identifier is absent for {tracking_uid_presence} observations in FHIR.json")
               
                    
        for observation in range(3,len(fhir_contents['contained'])):
            target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target == '246501002':
                pass
            else:
                for each in range(len(fhir_contents["contained"][observation]["component"])):
                    if 'Tracking Unique Identifier' in fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0].values():
                        tracking_uid_code = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["code"]
                        tracking_uid_display = fhir_contents["contained"][observation]["component"][each]["code"]["coding"][0]["display"]
                        try:
                            assert tracking_uid_code == "112040", f"Tracking ID code of {target} observation from FHIR report does not match the requirement"
                            assert tracking_uid_display == "Tracking Unique Identifier", f"Tracking Unique Identifier display text of {target} observation from FHIR report does not match the requirement"
                            with allure.step(f"Verification of Tracking Unique Identifier for {target} observation"):
                                allure.attach(f"Tracking Unique Identifier code from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID code: 112040, From FHIR.json Tracking ID code: {tracking_uid_code}", f"Verification of Tracking Unique Identifier code for {target} observation against requirement", allure.attachment_type.TEXT)
                                allure.attach(f"Tracking Unique Identifier display from FHIR matches with the requirement for {target} observation \
                                    From requirement Tracking ID display: Tracking Unique Identifier, From FHIR.json Tracking ID display: {tracking_uid_display}", f"Verification of Tracking Identifier display for {target} observation against requirement", allure.attachment_type.TEXT)
                        except AssertionError :
                            failures.append(target)
                            
            
        if failures:
            with allure.step(f"Failures"):
                self.allure_util.allure_attach_with_text(f"Tracking Unique Identifier from FHIR.json does not match with the requirements for following observations", str(failures))
            pytest.fail(f"Test failed due to Tracking Unique Identifier from FHIR.json does not match with requirement")
            
            
            
            



