import pytest
from marinaalchemist import BaseClass
import allure
import re

@pytest.mark.usefixtures("container_auto")
class TestFHIR(BaseClass):
    

    # run the autorun fixture first
    # store the output path in a variable
    # do the update_fhir_path() function
    # after updation, do the read_fhir() function
    

        # with allure.step("fhir_statics"):
        #     self.allure_util.allure_attach_with_text("resourceType of FHIR report", str(self.fhir_json['resourceType']))
    '''
    The test_fhir_obs_code verifies the Observation code of Annalise/Nuance/RadElement system displayed in FHIR by comparing it the CXR FHIR requirements
    '''
    def test_fhir_obs_code(self):
        print("testing Annalise observation code")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
        # non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture"]
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target_obs == "246501002":
                    count+=1
                    pass
                
                elif len(fhir_contents["contained"][observation]["code"]["coding"])==2:
                    Annalise_code_as_per_req = cxr_req[target_obs][0]["Annalise_observation.code"]
                    fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                    assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"{Annalise_code_as_per_req} from requrirement and {fhir_annalise_obs_code} from FHIR are not matching"
                    print(f"Annalise observation code {Annalise_code_as_per_req} from Requirements and {fhir_annalise_obs_code} from FHIR json is matching")
                    Nuance_code_as_per_req = cxr_req[target_obs][0]["Nuance_observation.code"]
                    fhir_nuance_obs_code = fhir_contents["contained"][observation]["code"]["coding"][1]["code"]
                    assert Nuance_code_as_per_req == fhir_nuance_obs_code, f"{Nuance_code_as_per_req} from requrirement and {fhir_nuance_obs_code} from FHIR are not matching"
                    print(f"Nuance observation code {Nuance_code_as_per_req} from Requirements and {fhir_nuance_obs_code} from FHIR json is matching")
                    count+=1
                
                elif len(fhir_contents["contained"][observation]["code"]["coding"])==1:
                    if cxr_req[target_obs][0]["RadElement_coding_system"]:
                        RadElement_code_as_per_req = cxr_req[target_obs][0]["RadElement_observation.code"]
                        fhir_RadElement_obs_code = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                        assert RadElement_code_as_per_req == fhir_RadElement_obs_code, "radele code not match"
                        print(f"RadElement observation code {RadElement_code_as_per_req} from Requirements and {fhir_RadElement_obs_code} from FHIR json is matching")
                        count+=1
                        
                    else:
                        Annalise_code_as_per_req = cxr_req[target_obs][0]["Annalise_observation.code"]
                        fhir_annalise_obs_code = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                        assert Annalise_code_as_per_req == fhir_annalise_obs_code, f"{Annalise_code_as_per_req} from requrirement and {fhir_annalise_obs_code} from FHIR are not matching"
                        print(f"Annalise observation code {Annalise_code_as_per_req} from Requirements and {fhir_annalise_obs_code} from FHIR json is matching")
                        count+=1
        except Exception as e:
            print(f"An exception occurred: {e}")
            
            

    '''
    The test_fhir_obs_display verifies the Observation's Display of Annalise/Nuance/RadElement system displayed in FHIR by comparing it the CXR FHIR requirements
    ''' 
    def test_fhir_obs_display(self):
        print("testing observation Display")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target == "246501002":
                    count+=1
                    pass
                elif len(fhir_contents["contained"][observation]["code"]["coding"])==2:
                    Annalise_display_as_per_req = cxr_req[target][0]["Annalise_observation.display"]
                    fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                    assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR are not matching"
                    print(f"Annalise observation display {Annalise_display_as_per_req} from Requirements and {fhir_annalise_obs_display} from FHIR json is matching")
                    Nuance_display_as_per_req = cxr_req[target][0]["Nuance_observation.display"]
                    fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][1]["display"]
                    assert Nuance_display_as_per_req == fhir_nuance_obs_display, f"{Nuance_display_as_per_req} from requrirement and {fhir_nuance_obs_display} from FHIR are not matching"
                    print(f"Nuance observation display {Nuance_display_as_per_req} from Requirements and {fhir_nuance_obs_display} from FHIR json is matching")
                    count+=1

                elif len(fhir_contents["contained"][observation]["code"]["coding"])==1:
                    if cxr_req[target][0]["RadElement_coding_system"]:
                        RadElement_display_as_per_req = cxr_req[target][0]["RadElement_observation.display"]
                        fhir_RadElement_obs_display = (fhir_contents["contained"][observation]["code"]["coding"][0]["display"])
                        assert RadElement_display_as_per_req == fhir_RadElement_obs_display, "radele code not match"
                        print(f"RadElement observation display {RadElement_display_as_per_req} from Requirements and {fhir_RadElement_obs_display} from FHIR json is matching")
                        count+=1
                        
                    else:
                        Annalise_display_as_per_req = cxr_req[target][0]["Annalise_observation.display"]
                        fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"{Annalise_display_as_per_req} from requrirement and {fhir_annalise_obs_display} from FHIR are not matching"
                        print(f"Annalise observation display {Annalise_display_as_per_req} from Requirements and {fhir_annalise_obs_display} from FHIR json is matching")
                        count+=1

            print(count)
            
        except Exception as e:
            print(f"An exception occurred: {e}")
        
        
    '''
    The test_obs_bodsite_code verifies the Observation's bodySite of Snomed & Radlex systems displayed in FHIR by comparing it the CXR FHIR requirements
    ''' 
    def test_obs_bodsite_code(self):
        print("testing observation Bodysite Code")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
        try:
            for observation in range(3,len(fhir_contents['contained'])):
                target = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                if target == "246501002": # This is ignored from verifying as its not an observation. Shall be verified in a dedicated test case.
                    count+=1
                    pass
                
                elif target == "RDES230": # This block verifies the bodySite of Vertebral Compression Fracture Observation observation
                    print(target)
                    bodySite_radlex_code_as_per_req = cxr_req[target][0]["bodySite_Radlex.code"]
                    fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                    assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                    print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                    count+=1
                
                elif target == "RDES225": # This block verifies the bodySite of Chest Radiograph Pulmonary Nodules observation
                    if fhir_contents["contained"][observation]["component"][0]["valueCodeableConcept"]["coding"][0]["display"] == "absent":
                        print("correct")
                        bodySite_snomed_code_as_per_req = cxr_req[target][1]["focal_airspace_opacity"][0]["bodySite_Snomed.code"]
                        fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requrirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
                        print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")
                        bodySite_radlex_code_as_per_req = cxr_req[target][1]["focal_airspace_opacity"][0]["bodySite_Radlex.code"]
                        fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                        assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                        print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                        count+=1
                    elif fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"] == "focal":
                        bodySite_snomed_code_as_per_req = cxr_req[target][1]["focal_airspace_opacity"][0]["bodySite_Snomed.code"]
                        fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requrirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
                        print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")
                        bodySite_radlex_code_as_per_req = cxr_req[target][1]["focal_airspace_opacity"][0]["bodySite_Radlex.code"]
                        fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                        assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                        print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                        count+=1
                        
                    elif fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"] == "multifocal":
                        bodySite_snomed_code_as_per_req = cxr_req[target][2]["multifocal_airspace_opacity"][0]["bodySite_Snomed.code"]
                        fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requrirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
                        print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")
                        bodySite_radlex_code_as_per_req = cxr_req[target][2]["multifocal_airspace_opacity"][0]["bodySite_Radlex.code"]
                        fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                        assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                        print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                        count+=1
                
                    elif fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"] == "diffuse lower":
                        bodySite_snomed_code_as_per_req = cxr_req[target][3]["diffuse_lower_airspace_opacity"][0]["bodySite_Snomed.code"]
                        fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requrirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
                        print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")
                        bodySite_radlex_code_as_per_req = cxr_req[target][3]["diffuse_lower_airspace_opacity"][0]["bodySite_Radlex.code"]
                        fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                        assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                        print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                        count+=1
                        
                    elif fhir_contents["contained"][observation]["component"][1]["valueCodeableConcept"]["coding"][0]["display"] == "diffuse upper":
                        bodySite_snomed_code_as_per_req = cxr_req[target][4]["diffuse_upper_airspace_opacity"][0]["bodySite_Snomed.code"]
                        fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                        assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requrirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
                        print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")
                        bodySite_radlex_code_as_per_req = cxr_req[target][4]["diffuse_upper_airspace_opacity"][0]["bodySite_Radlex.code"]
                        fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                        assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                        print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                        count+=1

                else: # This block verifies the bodySite of all observations other than Vertebral Compression Fracture and Chest Radiograph Pulmonary Nodules
                    bodySite_snomed_code_as_per_req = cxr_req[target][0]["bodySite_Snomed.code"]
                    fhir_bodySite_snomed_code = fhir_contents["contained"][observation]["bodySite"]["coding"][0]["code"]
                    assert bodySite_snomed_code_as_per_req == fhir_bodySite_snomed_code, f"{bodySite_snomed_code_as_per_req} from requrirement and {fhir_bodySite_snomed_code} from FHIR are not matching"
                    print(f"bodySite snomed code {bodySite_snomed_code_as_per_req} from Requirements and {fhir_bodySite_snomed_code} from FHIR json is matching")
                    bodySite_radlex_code_as_per_req = cxr_req[target][0]["bodySite_Radlex.code"]
                    fhir_bodySite_radlex_code = fhir_contents["contained"][observation]["bodySite"]["coding"][1]["code"]
                    assert bodySite_radlex_code_as_per_req == fhir_bodySite_radlex_code, f"{bodySite_radlex_code_as_per_req} from requrirement and {fhir_bodySite_radlex_code} from FHIR are not matching"
                    print(f"bodySite radlex code {bodySite_radlex_code_as_per_req} from Requirements and {fhir_bodySite_radlex_code} from FHIR json is matching")
                    count+=1

            print(count)
            
        except Exception as e:
            print(f"An exception occurred: {e}")
    
    def test_study_uid(self):
        print("testing observation Study instance UID")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
        try:
            study_uid_presence = self.generic_util.is_study_uid_present(fhir_contents)
            assert study_uid_presence, f"Study Instance UID is not present for one of the observation in FHIR"
            dicom_study_uid = self.dicom_util.extract_study_uid(self.fhir_input_path)
            fhir_study_uid = self.generic_util.extract_fhir_study_uid(fhir_contents)
            assert dicom_study_uid == fhir_study_uid, "Study Instance UID not matching !!"
        except Exception as e:
            print(f"An exception occurred: {e}")
            pytest.fail(f"Test failed: {e}")
            
            
    def test_fhir_tracking_id(self):
        print("testing FHIR Tracking Identifier")
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
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
        fhir_contents = self.fhir_contents
        assert fhir_contents is not None, f"Annalise-cxr-FHIR.json does not exist at {self.fhir_output_path} or the contents are None"
        cxr_req = self.cxr_req
        count = 0
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
    

















