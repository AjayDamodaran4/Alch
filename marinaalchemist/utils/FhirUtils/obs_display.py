import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils


class ObservationDisplay(object):
    
    def __init__(self):
        self.annalise_code_block_executed = False
        self.annalise_display_block_executed = False
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()    
    
    
    
    def verify_obs_display_annalise_system(self,fhir_contents, *args):
        count = 0
        args_lower = [arg.lower() for arg in args]
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        valid_args = {"row", "us"}
        failures = []
        target_unavailable = []
        self.cxr_req = conftest.read_cxr_req()
        Annalise_display_as_per_req = None
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                continue
            else:
                if region_ROW and not region_US:
                    assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                    try:
                        Annalise_display_as_per_req = self.cxr_req["ROW"][target_obs][0]["Annalise_observation.display"]
                    except KeyError:
                        target_unavailable.append(target_obs)
                elif region_US and not region_ROW:
                    try:
                        Annalise_display_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.display"]
                    except KeyError as e:
                        target_unavailable.append(target_obs)
                
                assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"

                fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                if Annalise_display_as_per_req is not None:
                    try:
                        assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                            Observation code as per requirement : {Annalise_display_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_display}"
                        print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_display_as_per_req}, From FHIR.json : {fhir_annalise_obs_display}")
                        count+=1
                    except AssertionError as e:
                            failures.append(target_obs)
        print(count)
        self.annalise_display_block_executed = True
                    
        
        if failures or target_unavailable:
            if failures:
                print(f"Annalise Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"Annalise Observation display text mismatches are observed in FHIR.json"):
                    allure.attach(f"Annalise Observation display text mismatches are observed in FHIR.json for {failures} ", f"Observation display text mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng Annalise Observation display text from FHIR.json not found in requirement :{target_unavailable}")
                return False
            else:
                return True
        
        
    
    
    def verify_obs_display_nuance_system(self,fhir_contents, *args):
        args_lower = [arg.lower() for arg in args]
        region_US = "us" in args_lower
        valid_args = ["us"]
        failures = []
        count = 0
        target_unavailable = []
        self.cxr_req = conftest.read_cxr_req()
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        Annalise_display_as_per_req, nuance_display_as_per_req = None, None
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('us')")

        if not region_US:
            raise ValueError("regionOfInstance - 'US' argument must be specified")
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture", "pleural_effusion", "pneumomediastinum", 
                               "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax"]
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        self.cxr_req = conftest.read_cxr_req()
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                pass
            else:
                if region_US:
                    if target_obs in non_nuance_findings:
                        if not self.annalise_display_block_executed:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                            assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'https://www.annalise.ai/guides', f"Coding system displayed in FHIR.json for {target_obs} observation is not Annalise. Exepcted is Annalise Coding system"
                        
                            try:
                                Annalise_display_as_per_req = self.cxr_req["US"]['annalise_coding_system'][target_obs][0]["Annalise_observation.code"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_annalise_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["code"]
                                
                            if Annalise_display_as_per_req is not None:    
                                try:
                                    assert Annalise_display_as_per_req == fhir_annalise_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {Annalise_display_as_per_req}, Observation code from FHIR.json : {fhir_annalise_obs_display}"
                                    print(f"Annalise coding system matches as per requirement. From requirement : {Annalise_display_as_per_req}, From FHIR.json : {fhir_annalise_obs_display}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                        else:
                            pass
                    else:
                        if len(fhir_contents['contained'][observation]['code']['coding']) == 1:
                            assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == 'http://nuancepowerscribe.com/ai', f"Coding system displayed in FHIR.json for {target_obs} observation is not Nuance. Exepcted is Nuance Coding system."
                            try:
                                nuance_display_as_per_req = self.cxr_req["US"]['nuance_coding_system'][target_obs][0]["Nuance_observation.display"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                            
                            if nuance_display_as_per_req is not None: 
                                try:
                                    assert nuance_display_as_per_req == fhir_nuance_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {nuance_display_as_per_req}, Observation code from FHIR.json : {fhir_nuance_obs_display}"
                                    count+=1
                                    print(f"Nuance coding system matches as per requirement. From requirement : {nuance_display_as_per_req}, From FHIR.json : {fhir_nuance_obs_display}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                                    
                        elif len(fhir_contents['contained'][observation]['code']['coding']) == 2:
                            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][1]["code"])
                            assert fhir_contents['contained'][observation]['code']['coding'][1]['system'] == 'http://nuancepowerscribe.com/ai', f"Coding system displayed in FHIR.json for {target_obs} observation is not Nuance. Exepcted is Nuance Coding system."
                            try:
                                nuance_display_as_per_req = self.cxr_req["US"]['nuance_coding_system'][target_obs][0]["Nuance_observation.display"]
                            except KeyError as e:
                                target_unavailable.append(target_obs)
                                
                            fhir_nuance_obs_display = fhir_contents["contained"][observation]["code"]["coding"][1]["display"]
                            
                            if nuance_display_as_per_req is not None: 
                                try:
                                    assert nuance_display_as_per_req == fhir_nuance_obs_display, f"Observation code for {target_obs} does not match with requirement! \
                                        Observation code as per requirement : {nuance_display_as_per_req}, Observation code from FHIR.json : {fhir_nuance_obs_display}"
                                    count+=1
                                    print(f"Nuance coding system matches as per requirement. From requirement : {nuance_display_as_per_req}, From FHIR.json : {fhir_nuance_obs_display}")
                                except AssertionError as e:
                                    failures.append(target_obs)
                                
                        else:
                            print(f"more than one/two coding systems are present for {target_obs} observation")
                            pytest.fail(f"more than one/two coding systems are present for {target_obs} observation")
                    
        print(count)
        
        
        if failures or target_unavailable:
            if failures:
                print(f"Nuance Observation code mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"Annalise Observation code mismatches are observed in FHIR.json"):
                    allure.attach(f"Annalise Observation code mismatches are observed in FHIR.json for {failures} ", f"Observation code mismatch found in FHIR.json in Annalise coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng Nuance Observation code from FHIR.json not found in requirement :{target_unavailable}")
                return False
            else:
                return True
        
    
    
    
    def verify_obs_display_radelement(self,fhir_contents,regionOfInstance):
        valid_args = ['us']
        presence = False
        if regionOfInstance.lower() not in valid_args:
            raise ValueError(f"Provided regionOfInstance argument : {regionOfInstance} is not supported. Supported argument is : 'US' ")
        self.cxr_req = conftest.read_cxr_req()
        failures = []
        target_unavailable = []
        radelement_display_as_per_req = None
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            
            if "RDES" in target_obs:
                presence = True
            
            if target_obs == "246501002":
                pass
            elif target_obs in radelement_findings:
                assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                assert fhir_contents['contained'][observation]['code']['coding'][0]['system'] == "http://radelement.org", f"Coding system displayed in FHIR.json for {target_obs} observation is not RadElement. Exepcted is RadElement Coding system"

                try:
                    radelement_display_as_per_req = self.cxr_req["US"]['radelement_coding_system'][target_obs][0]["RadElement_observation.display"]
                except KeyError as e:
                    target_unavailable.append(target_obs)
            
                fhir_radelement_obs_display = fhir_contents["contained"][observation]["code"]["coding"][0]["display"]
                
                if radelement_display_as_per_req is not None:
                    try:
                        assert radelement_display_as_per_req == fhir_radelement_obs_display, f"Observation display text for {target_obs} does not match with requirement! \
                            Observation display text as per requirement : {radelement_display_as_per_req}, Observation display text from FHIR.json : {fhir_radelement_obs_display}"
                        print(f"RadElement coding system matches as per requirement. From requirement : {radelement_display_as_per_req}, From FHIR.json : {fhir_radelement_obs_display}")
                    except AssertionError as e:
                        failures.append(target_obs)
                    

        if failures or target_unavailable or not presence:
            if failures:
                print(f"RadElement Observation display text mismatches are observed in FHIR.json for following observations :{failures}")
                with allure.step(f"RadElement Observation display text mismatches are observed in FHIR.json"):
                    allure.attach(f"RadElement Observation display text mismatches are observed in FHIR.json for {failures} ", f"Observation display text mismatch found in FHIR.json in RadElement coding system", allure.attachment_type.TEXT)
                return False
            
            elif target_unavailable:
                print(f"Folloiwng RadElement Observation display text from FHIR.json not found in requirement :{target_unavailable}")
                return False
            
            elif not presence:
                print("No RadElement findings are found in FHIR.json")
                return False
            
            else:
                return True




    def verify_observation_display(self, fhir_contents, *args):
        args_lower = [arg.lower() for arg in args]
        annalise_present = "annalise" in args_lower
        nuance_present = "nuance" in args_lower
        radelement_present = "radelement" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        
        
        valid_args = {"row", "annalise", "us", "nuance", "radelement"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : ('row', 'us', 'annalise', 'nuance', 'radelement')")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")

        if not (annalise_present or nuance_present or radelement_present):
            raise ValueError("Any one of coding systems (annalise/nuance/radelement) must be specified as argument")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
        non_nuance_findings = ["acute_humerus_fracture", "acute_rib_fracture", "acute_clavicle_fracture","pleural_effusion", 
                               "pneumomediastinum", "pneumothorax", "single_pulmonary_nodule", "spine_wedge_fracture", 
                               "subdiaphragmatic_gas", "tension_pneumothorax"]
        radelement_findings = ["RDES225", "RDES254", "RDES76", "RDES44", "RDES227", "RDES230", "RDES228", "RDES44"]
        
        # This block verifies the condition/scenario for ROW and annalise coding system
        if region_ROW and not region_US:
            valid_args_for_ROW = {"row", "annalise"}
            invalid_args_for_ROW = [arg for arg in args_lower if arg not in valid_args_for_ROW]
            
            if invalid_args_for_ROW:
                raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_ROW)}")

            else:
                if annalise_present and not (nuance_present or radelement_present):
                    self.verify_obs_display_annalise_system(fhir_contents,"ROW")


        # This block verifies the condition/scenario for ROW and annalise coding system
        elif region_US and not region_ROW:
            valid_args_for_US = {"us", "annalise", "nuance", "radelement"}
            invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
            
            if invalid_args_for_US:
                raise ValueError(f"The following arguments is not supported for US region: {', '.join(invalid_args_for_US)}")

            elif annalise_present and not (nuance_present or radelement_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
            
            
            elif nuance_present and not (annalise_present or radelement_present):
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                        

            elif annalise_present and nuance_present and not (radelement_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        if target_obs in non_nuance_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        else:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 2, f"Two coding systems are not available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                
                        
            elif annalise_present and radelement_present and not (nuance_present) or radelement_present and not (annalise_present or nuance_present):
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
                self.verify_obs_display_radelement(fhir_contents,"US")
                

                            
            elif nuance_present and radelement_present and not (annalise_present):
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                self.verify_obs_display_radelement(fhir_contents,"US")
            
            
            elif annalise_present and nuance_present and radelement_present:
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        if target_obs in non_nuance_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        elif target_obs in radelement_findings:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 1, f"More than one coding system is available in FHIR.json for {target_obs} observation"
                        else:
                            assert len(fhir_contents['contained'][observation]['code']['coding']) == 2, f"Two coding systems are not available in FHIR.json for {target_obs} observation"
                self.verify_obs_display_annalise_system(fhir_contents,"US")
                self.verify_obs_display_nuance_system(fhir_contents,"US")
                self.verify_obs_display_radelement(fhir_contents,"US")
                
                