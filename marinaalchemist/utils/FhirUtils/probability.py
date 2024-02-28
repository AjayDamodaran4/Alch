import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..dicom_utils import DicomUtils
from ..excelutils import ExcelUtils

"""
TO DO

1. remove probabilily absence from snomed, nuance and radlex methods. create a new single method for it

3. Add US region scenarios.
4. probability score verification method - create
"""




class Probability_Qualifier(object):
    
    def __init__(self):
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()    
        self.fda_findings = ["pleural_effusion", "pneumothorax", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax", "RDES254", "RDES230", "RDES228"]
        self.group_findings =["RDES225","RDES44"]
    
    def find_component_index_for_probability(self,components):
        """
        Find the index of the dictionary in the components list that contains a value from the test list.

        Args:
        - components (list): A list of dictionaries to search through.
        - probability_details (list): A list of values to search for.

        Returns:
        - int: The index of the dictionary containing a value from the probability_details list, or -1 if no match is found.
        """
        
        probability_details = ['Probably', 'probably', 'Finding Probability']

    # Iterate through each dictionary in the components
        for index, value in enumerate(components):
            # Iterate through the 'coding' list within the 'code' key of the dictionary
            for coding in value.get("code", {}).get("coding", []):
                # Check if the 'display' value is present in the test list
                if coding.get("display") in probability_details:
                    # If a match is found, return the index of the dictionary
                    return index
    
    # If no match is found, return -1
        return -1
    
    
    # def probability_snomed_coding(self,fhir_contents,regionOfInstance):
    #     probability_absence = []
    #     probability_snomed_failure = []
    #     probability_snomed_requirement = {
    #             "system": "http://snomed.info/sct",
    #             "code": "2931005",
    #             "display": "Probably"
    #           }
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         if target_obs == "246501002":
    #             pass
    #         else:
    #             if regionOfInstance == "ROW":
    #                 components = fhir_contents["contained"][observation]["component"]
    #                 probability_component_index  = self.find_component_index_for_probability(components)
    #                 probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                 if probability_component_index != -1:
    #                     try:
    #                         assert probability_snomed_requirement in probability_component_fhir, \
    #                         f"Probability qualifier of snomed coding system does not match requirement for {target_obs} observation"
    #                         print(f"probability qualifier component matches as per snomed coding system for {target_obs} observation")
    #                     except AssertionError :
    #                         probability_snomed_failure.append(target_obs)
    #                 else:
    #                     probability_absence.append(target_obs)
    #             elif regionOfInstance == "US":
    #                 if target_obs in (self.fda_findings + self.group_findings):
    #                     pass
    #                 else:
    #                     components = fhir_contents["contained"][observation]["component"]
    #                     probability_component_index  = self.find_component_index_for_probability(components)
    #                     probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                     if probability_component_index != -1:
    #                         try:
    #                             assert probability_snomed_requirement in probability_component_fhir, \
    #                             f"Probability qualifier of snomed coding system does not match requirement for {target_obs} observation"
    #                             print(f"probability qualifier component matches as per snomed coding system for {target_obs} observation")
    #                         except AssertionError :
    #                             probability_snomed_failure.append(target_obs)
    #                     else:
    #                         probability_absence.append(target_obs)
    #             else:
    #                 raise ValueError  
                        
    #     if probability_absence or probability_snomed_failure:
    #             if probability_snomed_failure:
    #                 print(f"Probability qualifier - snomed coding system does not match with requirement for following observations :{probability_snomed_failure}")
    #                 return False
                
    #             elif probability_absence:
    #                 print(f"Probability qualifier component not present in FHIR.json for following observations :{probability_absence}")
    #                 return False
    #             else:
    #                 return True
                    


    # def probability_nuance_coding(self,fhir_contents,regionOfInstance):
    #     probability_absence = []
    #     probability_nuance_failure = []
    #     probability_nuance_requirement = {
    #             "system": "http://nuancepowerscribe.com/ai",
    #             "code": "90090302",
    #             "display": "Finding Probability"
    #           }
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         if target_obs == "246501002":
    #             pass
    #         else:
    #             if regionOfInstance == "ROW":
    #                 components = fhir_contents["contained"][observation]["component"]
    #                 probability_component_index  = self.find_component_index_for_probability(components)
    #                 probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                 if probability_component_index != -1:
    #                     try:
    #                         assert probability_nuance_requirement in probability_component_fhir, \
    #                         f"Probability qualifier of nuance coding system does not match requirement for {target_obs} observation"
    #                         print(f"probability qualifier component matches as per nuance coding system for {target_obs} observation")
    #                     except AssertionError :
    #                         probability_nuance_failure.append(target_obs)
    #                 else:
    #                     probability_absence.append(target_obs)
    #             elif regionOfInstance == "US":
    #                 if target_obs in self.fda_findings or self.group_findings:
    #                     pass
    #                 else:
    #                     components = fhir_contents["contained"][observation]["component"]
    #                     probability_component_index  = self.find_component_index_for_probability(components)
    #                     probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                     if probability_component_index != -1:
    #                         try:
    #                             assert probability_nuance_requirement in probability_component_fhir, \
    #                             f"Probability qualifier of nuance coding system does not match requirement for {target_obs} observation"
    #                             print(f"probability qualifier component matches as per nuance coding system for {target_obs} observation")
    #                         except AssertionError :
    #                             probability_nuance_failure.append(target_obs)
    #                     else:
    #                         probability_absence.append(target_obs)
    #             else:
    #                 raise ValueError
                    
                    
    #     if probability_absence or probability_nuance_failure:
    #             if probability_nuance_failure:
    #                 print(f"Probability qualifier - nuance coding system does not match with requirement for following observations :{probability_nuance_failure}")
    #                 return False
                
    #             elif probability_absence:
    #                 print(f"Probability qualifier component not present in FHIR.json for following observations :{probability_absence}")
    #                 return False
    #             else:
    #                 return True

            

    # def probability_radlex_coding(self,fhir_contents,regionOfInstance):
    #     probability_absence = []
    #     probability_radlex_failure = []
    #     probability_radlex_requirement = {
    #             "system": "http://radlex.org",
    #             "code": "RID33",
    #             "display": "probably"
    #             }
    #     for observation in range(3,len(fhir_contents['contained'])):
    #         target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #         if target_obs == "246501002":
    #             pass
    #         else:
    #             if regionOfInstance == "ROW":
    #                 components = fhir_contents["contained"][observation]["component"]
    #                 probability_component_index  = self.find_component_index_for_probability(components)
    #                 probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                 if probability_component_index != -1:
    #                     try:
    #                         assert probability_radlex_requirement in probability_component_fhir, \
    #                         f"Probability qualifier of radlex coding system does not match requirement for {target_obs} observation"
    #                         print(f"probability qualifier component matches as per radlex coding system for {target_obs} observation")
    #                     except AssertionError :
    #                         probability_radlex_failure.append(target_obs)
    #                 else:
    #                     probability_absence.append(target_obs)
    #             elif regionOfInstance == "US":
    #                 if target_obs in self.fda_findings or self.group_findings:
    #                     pass
    #                 else:
    #                     components = fhir_contents["contained"][observation]["component"]
    #                     probability_component_index  = self.find_component_index_for_probability(components)
    #                     probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                     if probability_component_index != -1:
    #                         try:
    #                             assert probability_radlex_requirement in probability_component_fhir, \
    #                             f"Probability qualifier of radlex coding system does not match requirement for {target_obs} observation"
    #                             print(f"probability qualifier component matches as per radlex coding system for {target_obs} observation")
    #                         except AssertionError :
    #                             probability_radlex_failure.append(target_obs)
    #                     else:
    #                         probability_absence.append(target_obs)
    #             else:
    #                 raise ValueError
                    
                    
    #     if probability_absence or probability_radlex_failure:
    #             if probability_radlex_failure:
    #                 print(f"Probability qualifier - Radlex coding system does not match with requirement for following observations :{probability_radlex_failure}")
    #                 return False
                
    #             elif probability_absence:
    #                 print(f"Probability qualifier component not present in FHIR.json for following observations :{probability_absence}")
    #                 return False
    #             else:
    #                 return True 
            
                        
                    
    def verify_probability(self,fhir_contents,*args):
        args_lower = [arg.lower() for arg in args]
        nuance_present = "nuance" in args_lower
        snomed_present = "snomed" in args_lower
        radlex_present = "radlex" in args_lower
        region_ROW = "row" in args_lower
        region_US = "us" in args_lower
        probability_systems_count_failure = []
        probability_absence = []
        probability_presence = []
        valid_args = {"row", "us", "nuance", "snomed", "radlex"}
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

        if not (region_ROW or region_US):
            raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        
        if region_ROW and region_US:
            raise ValueError("Two regionofInstance arguments detected. Only one regionOfInstance is supported.")
        
        if not (snomed_present or radlex_present or nuance_present):
            raise ValueError("Any one of Probability coding systems (snomed/nuance/radlex) must be specified as argument")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
        probability_systems = {
                            'snomed_probability' : {
            "system": "http://snomed.info/sct",
            "code": "2931005",
            "display": "Probably"
            },
                            'nuance_probability' : {
            "system": "http://nuancepowerscribe.com/ai",
            "code": "90090302",
            "display": "Finding Probability"
            },
                            'radlex_probability' : {
            "system": "http://radlex.org",
            "code": "RID33",
            "display": "probably"
            }
                            }
    
        applicable_systems_mapping = {'snomed_probability' : snomed_present,
            'nuance_probability' : nuance_present,
            'radlex_probability' : radlex_present}
        
        applicable_systems = [probability_systems.get(key) for key,value in applicable_systems_mapping.items() if value]
        
        if region_ROW and not region_US:
            valid_args_for_ROW = {"row","snomed", "radlex","nuance"}
            invalid_args_for_ROW = [arg for arg in args_lower if arg not in valid_args_for_ROW]
            
            if invalid_args_for_ROW:
                raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_ROW)}")

            else:
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    else:
                        components = fhir_contents["contained"][observation]["component"]
                        probability_component_index  = self.find_component_index_for_probability(components)
                        if probability_component_index == -1:
                            probability_absence.append(target_obs)
    
                        else:
                            probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
                            try:
                                assert applicable_systems == probability_component_fhir, f"write correct error msg"
                                print(f"probability qualifier of {target_obs} matches as per requirement")
                            except AssertionError:
                                probability_systems_count_failure.append(target_obs)
                                
            if probability_systems_count_failure :
                print(f"Probability Qualifier coding systems present in FHIR.json does not match with\
                        coding systems that's passed as argument for test case for following observations: {probability_systems_count_failure}")
                return False
            else:   
                return True
    
        elif region_US and not region_ROW:
            valid_args_for_US = {"us","snomed", "radlex","nuance"}
            invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
            
            if invalid_args_for_US:
                raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_US)}")

            else:
                for observation in range(3,len(fhir_contents['contained'])):
                    target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
                    if target_obs == "246501002":
                        pass
                    elif target_obs in self.fda_findings or target_obs in self.group_findings:
                        components = fhir_contents["contained"][observation]["component"]
                        probability_component_index  = self.find_component_index_for_probability(components)
                        try:
                            assert probability_component_index == -1, f"Probability Qualifier component are available for {target_obs} observation which is not expected."
                        except AssertionError:
                            probability_presence.append(target_obs)
                    else:
                        components = fhir_contents["contained"][observation]["component"]
                        probability_component_index  = self.find_component_index_for_probability(components)
                        if probability_component_index == -1:
                            probability_absence.append(target_obs)
    
                        else:
                            probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
                            try:
                                assert applicable_systems == probability_component_fhir, f"write correct error msg"
                                print(f"probability qualifier of {target_obs} matches as per requirement")
                            except AssertionError:
                                probability_systems_count_failure.append(target_obs)
                
                
            if probability_systems_count_failure or probability_presence or probability_absence :
                if probability_systems_count_failure:
                    print(f"Probability Qualifier coding systems present in FHIR.json does not match with \
                            coding systems that's passed as argument for test case for following observations: {probability_systems_count_failure}")
                    return False
            
                elif probability_presence:
                    print(f"Probability Qualifier component are available for following observations which is not expected : {probability_presence}")
                    return False
                elif probability_absence:
                    print(f"Probability Qualifier component are NOT available for following observation which is not expected : {probability_absence}")
                    return False
            else:
                return True
                
                

    # def verify_probability(self,fhir_contents,*args):
    #     args_lower = [arg.lower() for arg in args]
    #     annalise_present = "annalise" in args_lower
    #     nuance_present = "nuance" in args_lower
    #     radelement_present = "radelement" in args_lower
    #     snomed_present = "snomed" in args_lower
    #     radlex_present = "radlex" in args_lower
    #     region_ROW = "row" in args_lower
    #     region_US = "us" in args_lower
    #     probability_systems_count_failure = []
    #     probability_absence = []
    #     probability_presence = []
    #     valid_args = {"row", "annalise", "us", "nuance", "radelement", "snomed", "radlex"}
        
    #     invalid_args = [arg for arg in args_lower if arg not in valid_args]
    #     if invalid_args:
    #         raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

    #     if not (region_ROW or region_US):
    #         raise ValueError("regionOfInstance - 'ROW' or 'US' argument must be specified")
        
    #     if region_ROW and region_US:
    #         raise ValueError("Two regionofInstance arguments detected. Only one regionOfInstance is supported.")
        
    #     if not (snomed_present or radlex_present or nuance_present):
    #         raise ValueError("Any one of Probability coding systems (snomed/nuance/radlex) must be specified as argument")
        
    #     if len(args_lower) != len(set(args_lower)):
    #         raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
    #     fda_findings = ["pleural_effusion", "pneumothorax", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax", "RDES254", "RDES230", "RDES228"]
    #     group_findings =["RDES225","RDES44"]
        
    #     probability_systems = {
    #                         'snomed_probability' : {
    #         "system": "http://snomed.info/sct",
    #         "code": "2931005",
    #         "display": "Probably"
    #         },
    #                         'nuance_probability' : {
    #         "system": "http://nuancepowerscribe.com/ai",
    #         "code": "90090302",
    #         "display": "Finding Probability"
    #         },
    #                         'radlex_probability' : {
    #         "system": "http://radlex.org",
    #         "code": "RID33",
    #         "display": "probably"
    #         }
    #                         }
    
    #     applicable_systems_mapping = {'snomed_probability' : snomed_present,
    #         'nuance_probability' : nuance_present,
    #         'radlex_probability' : radlex_present}
        
    #     applicable_systems = [probability_systems.get(key) for key,value in applicable_systems_mapping.items() if value]


    #     if region_ROW and not region_US:
    #         valid_args_for_ROW = {"row","snomed", "radlex","nuance"}
    #         invalid_args_for_ROW = [arg for arg in args_lower if arg not in valid_args_for_ROW]
            

    #         if invalid_args_for_ROW:
    #             raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_ROW)}")

    #         else:
    #             for observation in range(3,len(fhir_contents['contained'])):
    #                 target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #                 if target_obs == "246501002":
    #                     pass
    #                 else:
    #                     components = fhir_contents["contained"][observation]["component"]
    #                     probability_component_index  = self.find_component_index_for_probability(components)
    #                     if probability_component_index == -1:
    #                         probability_absence.append(target_obs)
    
    #                     else:
    #                         probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                         try:
    #                             assert applicable_systems == probability_component_fhir, f"write correct error msg"
    #                         except AssertionError:
    #                             probability_systems_count_failure.append(target_obs)
    #             conditions = [
    #                 (snomed_present and not radlex_present and not nuance_present, self.probability_snomed_coding),
    #                 (nuance_present and not radlex_present and not snomed_present, self.probability_nuance_coding),
    #                 (radlex_present and not nuance_present and not snomed_present, self.probability_radlex_coding),
    #                 (snomed_present and nuance_present and not radlex_present, (self.probability_snomed_coding, self.probability_nuance_coding)),
    #                 (snomed_present and radlex_present and not nuance_present, (self.probability_snomed_coding, self.probability_radlex_coding)),
    #                 (nuance_present and radlex_present and not snomed_present, (self.probability_nuance_coding, self.probability_radlex_coding)),
    #                 (snomed_present and nuance_present and radlex_present, (self.probability_snomed_coding, self.probability_nuance_coding, self.probability_radlex_coding))
    #             ]
                
    #             for functions in [func for condition, func in conditions if condition]:
    #                 if isinstance(functions, tuple):
    #                     for func in functions:
    #                         func(fhir_contents,regionOfInstance="ROW")
    #                 else:
    #                     functions(fhir_contents,regionOfInstance="ROW")
                        
                        
    #         if probability_systems_count_failure :
    #             print(f"Probability Qualifier coding systems present in FHIR.json does not match with\
    #                     coding systems that's passed as argument for test case for following observations: {probability_systems_count_failure}")
    #             return False
    #         else:
    #             return True
        
    #     elif region_US and not region_ROW:
    #         valid_args_for_US = {"us","snomed", "radlex","nuance"}
    #         invalid_args_for_US = [arg for arg in args_lower if arg not in valid_args_for_US]
            
    #         if invalid_args_for_US:
    #             raise ValueError(f"The following arguments is not supported for ROW region: {', '.join(invalid_args_for_US)}")
    #         else:
    #             for observation in range(3,len(fhir_contents['contained'])):
    #                 target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
    #                 if target_obs == "246501002":
    #                     pass
    #                 elif target_obs in (fda_findings + group_findings):
    #                     components = fhir_contents["contained"][observation]["component"]
    #                     probability_component_index  = self.find_component_index_for_probability(components)
    #                     try:
    #                         assert probability_component_index == -1, f"Probability Qualifier component are available for {target_obs} observation which is not expected."
    #                     except AssertionError:
    #                         probability_presence.append(target_obs)
    #                 else:
    #                     components = fhir_contents["contained"][observation]["component"]
    #                     probability_component_index  = self.find_component_index_for_probability(components)
    #                     if probability_component_index == -1:
    #                         probability_absence.append(target_obs)
    
    #                     else:
    #                         probability_component_fhir = components[probability_component_index].get("code", {}).get("coding", [])
    #                         try:
    #                             assert applicable_systems == probability_component_fhir, f"write correct error msg"
    #                         except AssertionError:
    #                             probability_systems_count_failure.append(target_obs)

                    
    #             conditions = [
    #             (snomed_present and not radlex_present and not nuance_present, self.probability_snomed_coding),
    #             (nuance_present and not radlex_present and not snomed_present, self.probability_nuance_coding),
    #             (radlex_present and not nuance_present and not snomed_present, self.probability_radlex_coding),
    #             (snomed_present and nuance_present and not radlex_present, (self.probability_snomed_coding, self.probability_nuance_coding)),
    #             (snomed_present and radlex_present and not nuance_present, (self.probability_snomed_coding, self.probability_radlex_coding)),
    #             (nuance_present and radlex_present and not snomed_present, (self.probability_nuance_coding, self.probability_radlex_coding)),
    #             (snomed_present and nuance_present and radlex_present, (self.probability_snomed_coding, self.probability_nuance_coding, self.probability_radlex_coding))
    #             ]
                
    #             for functions in [func for condition, func in conditions if condition]:
    #                 if isinstance(functions, tuple):
    #                     for func in functions:
    #                         func(fhir_contents,regionOfInstance="US")
    #                 else:
    #                     functions(fhir_contents,regionOfInstance="US")
                

    #             if probability_systems_count_failure or probability_presence or probability_absence :
    #                 if probability_systems_count_failure:
    #                     print(f"Probability Qualifier coding systems present in FHIR.json does not match with \
    #                             coding systems that's passed as argument for test case for following observations: {probability_systems_count_failure}")
    #                     return False
                
    #                 elif probability_presence:
    #                     print(f"Probability Qualifier component are available for following observations which is not expected : {probability_presence}")
    #                     return False
    #                 elif probability_absence:
    #                     print(f"Probability Qualifier component are NOT available for following observation which is not expected : {probability_absence}")
    #                     return False
    #             else:
    #                 return True
                
                
                
                