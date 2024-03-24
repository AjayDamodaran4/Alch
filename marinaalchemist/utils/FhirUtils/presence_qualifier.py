import os, json, allure, pytest
from ..config_reader import Config
import conftest
from ..excelutils import ExcelUtils

"""
TO DO

1. what if finding name not present in config.json. it should read default threshold value ---> DONE.
2. write a test for "valueString": "present" ---> DONE.
3. what if finding name not present in both config.json and in default threshold. ---> DONE.
4. write a test for valuecodeableConcept ---> DONE.
5. failure reporting mecahnisms
6. log messages
7. assertion error handle for all scenarios


"""




class Presence_Qualifier(object):
    
    def __init__(self): 
        self.cxr_req = conftest.read_cxr_req()
        self.cxr_mappings = conftest.read_mappings_json()    
        self.fda_findings = ["pleural_effusion", "pneumothorax", "spine_wedge_fracture", "subdiaphragmatic_gas", "tension_pneumothorax", "RDES254", "RDES230", "RDES228"]
        self.group_findings =["RDES225","RDES44"]
        
    def read_config_json(self, config_json_path):
        with open(config_json_path) as f:
            config_json = json.load(f)
            thresholds = config_json["subscriber"]["thresholds"]
            return thresholds
        
    def find_component_index_for_presence(self,components):
        """
        Find the index of the dictionary in the components list that contains a value from the test list.

        Args:
        - components (list): A list of dictionaries to search through.
        - presence_details (list): A list of values to search for.

        Returns:
        - int: The index of the dictionary containing a value from the presence_details list, or -1 if no match is found.
        """
        
        presence_details = ["52101004", "Present", "90090301", "Finding Qualifier", "RID28472", "present", "2667000", "Absent", "90090301", "Finding Qualifier", "RID28473", "absent"] 

    # Iterate through each dictionary in the components
        for index, value in enumerate(components):
            # Iterate through the 'coding' list within the 'code' key of the dictionary
            for coding in value.get("code", {}).get("coding", []):
                # Check if the 'display' value is present in the test list
                if coding.get("display") in presence_details:
                    # If a match is found, return the index of the dictionary
                    return index
    
    # If no match is found, return -1
        return -1
    
    def presence_of_finding(self, model_output_contents, observation_name, config_json_path=None):
        observation_presence=None
        for key, value in self.cxr_mappings.items():
            if observation_name in (key, value):
                probability_mapping_code = key
                probability_score_model_output = model_output_contents.get('cxr_value',{}).get('classifications',{}).get('groups',{}).get(probability_mapping_code,{})['present']
                if config_json_path:
                    config_json_thresholds = self.read_config_json(config_json_path)
                    observation_threshold = next((i['predictionThreshold'] for i in config_json_thresholds if i["label"] == observation_name), None)
                    if observation_threshold is None:
                        observation_threshold = model_output_contents.get('cxr_value',{}).get('classifications',{}).get('thresholds',{})[probability_mapping_code]
                else:
                    observation_threshold = model_output_contents.get('cxr_value',{}).get('classifications',{}).get('thresholds',{})[probability_mapping_code]
                if probability_score_model_output>=observation_threshold:
                    observation_presence = "present"
                else:
                    observation_presence = "absent"
                
        return observation_presence
    

    def verify_presence_qualifier(self, fhir_contents=None, model_output_contents=None, config_json_path=None, system=None):
    # def verify_presence_qualifier(self,fhir_contents,model_output_contents,config_json_path=None,*args):  
        args_lower = [arg.lower() for arg in system]
        nuance_present = "nuance" in args_lower
        snomed_present = "snomed" in args_lower
        radlex_present = "radlex" in args_lower
        valid_args = {"nuance", "snomed", "radlex"}
        presence_qualifier_absent = []
        presence_systems_failure = []
        presence_qualifier_mismatch = {}
        observation_not_found = []
        valueCodeableConcept_failure = []
        
        invalid_args = [arg for arg in args_lower if arg not in valid_args]
        if invalid_args:
            raise ValueError(f"The following arguments is not supported: {', '.join(invalid_args)}. Supported arguments are : {valid_args}")

        if not (snomed_present or radlex_present or nuance_present):
            raise ValueError("Any one of Probability coding systems (snomed/nuance/radlex) must be specified as argument")
        
        if len(args_lower) != len(set(args_lower)):
            raise ValueError("Duplicate arguments detected. Please provide each argument only once.")
    
        presence_systems = {
                            'snomed_presence' : {
                                                    "system": "http://snomed.info/sct",
                                                    "code": "52101004",
                                                    "display": "Present"
                                                },
                            'nuance_presence' : {
                                                    "system": "http://nuancepowerscribe.com/ai",
                                                    "code": "90090301",
                                                    "display": "Finding Qualifier"
                                                    },
                            'radlex_presence' : {
                                                    "system": "http://radlex.org",
                                                    "code": "RID28472",
                                                    "display": "present"
                                                    },
                            'snomed_absence' : {
                                                    "system": "http://snomed.info/sct",
                                                    "code": "2667000",
                                                    "display": "Absent"
                                                },
                            'nuance_absence' : {
                                                    "system": "http://nuancepowerscribe.com/ai",
                                                    "code": "90090301",
                                                    "display": "Finding Qualifier"
                                                    },
                            'radlex_absence' : {
                                                    "system": "http://radlex.org",
                                                    "code": "RID28473",
                                                    "display": "absent"
                                                    }
                            }
    
    
        presence_systems_mapping = {'snomed_presence' : snomed_present,
            'nuance_presence' : nuance_present,
            'radlex_presence' : radlex_present}
        
        absence_systems_mapping = {'snomed_absence' : snomed_present,
            'nuance_absence' : nuance_present,
            'radlex_absence' : radlex_present}
        
        for observation in range(3,len(fhir_contents['contained'])):
            target_obs = (fhir_contents["contained"][observation]["code"]["coding"][0]["code"])
            if target_obs == "246501002" or target_obs=="intercostal_drain":
                    continue
            
            observation_presence = self.presence_of_finding(model_output_contents, target_obs, config_json_path)
            if observation_presence == "present":
                applicable_systems = [presence_systems.get(key) for key,value in presence_systems_mapping.items() if value]
            
            else:
                applicable_systems = [presence_systems.get(key) for key,value in absence_systems_mapping.items() if value]
                
                
            components = fhir_contents["contained"][observation]["component"]
            presence_component_index  = self.find_component_index_for_presence(components)
            if presence_component_index == -1:
                print(f"presence qualifier component not present for : {target_obs}")
                presence_qualifier_absent.append(target_obs)
            else:
                
                if observation_presence is None:
                    observation_not_found.append(target_obs)
                    continue

                try:
                    assert observation_presence == components[presence_component_index]['valueString']
                except AssertionError:
                    presence_qualifier_mismatch[f"{target_obs}"] = {f"Presence Qualifier as per model_output : {observation_presence}, Presence Qualifier as per FHIR.json: {components[presence_component_index]['valueString']}"}
                    continue

                presence_component_fhir = components[presence_component_index].get("code", {}).get("coding", [])
                
                
                try:
                    # print(f"{target_obs}, applicable_systems = {applicable_systems}, fhir_component : {presence_component_fhir}")
                    assert applicable_systems == presence_component_fhir, f"write correct error msg"
                    # print(f"presence qualifier of {target_obs} matches as per requirement")
                except AssertionError:
                    presence_systems_failure.append(target_obs)
                    
                    
                try:
                    assert applicable_systems == fhir_contents["contained"][observation]["valueCodeableConcept"].get("coding", [])
                    assert observation_presence == fhir_contents["contained"][observation]["valueCodeableConcept"]["text"]
                    
                except AssertionError:
                    valueCodeableConcept_failure.append(target_obs)
                    
                    
                    
        if presence_qualifier_absent or presence_systems_failure or presence_qualifier_mismatch or observation_not_found or valueCodeableConcept_failure:
            error_messages = []

            if presence_qualifier_mismatch:
                error_messages.append(f"Presence Qualifier mismatch is observed for following observations: {presence_qualifier_mismatch}")
            if presence_systems_failure:
                error_messages.append(f"Presence Qualifier coding systems present in FHIR.json does not match with requirement/coding systems that's passed as argument for test case for following observations: {presence_systems_failure}")
            if presence_qualifier_absent:
                error_messages.append(f"Presence Qualifier component not available in FHIR.json following observations: {presence_qualifier_absent}")
            if observation_not_found:
                error_messages.append(f"Following observation code does not match with cxr observation codes: {observation_not_found}")
            if valueCodeableConcept_failure:
                error_messages.append(f"valueCodeableConcept block from FHIR.json does not match as per requirement for following observations: {valueCodeableConcept_failure}")

            if error_messages:
                print("\n".join(error_messages))
                return False
        else:
            return True
            