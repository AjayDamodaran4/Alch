import allure
from allure_commons.types import AttachmentType
from datetime import datetime
from .config_reader import Config

class AllureReport(object):
    __attachment_type = AttachmentType.PNG
    __driver_utils = None

    def __init__(self, driver_utils):
        self.__driver_utils = driver_utils

    def allure_attach_with_screenshot(self, name, screenshot_boolean):
        if screenshot_boolean:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            name = name + " Timestamp: " + str(timestamp)
            allure.attach(self.__driver_utils.take_screenshot(), name=name, attachment_type=self.__attachment_type)

    def allure_attach_with_text(self, name, body):
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        name = name + " Timestamp: " + str(timestamp)
        allure.attach(name=name, body=body)
        
        
    # def log_to_allure(self,message):
    #     allure.attach(message, name="Log Message", attachment_type=allure.attachment_type.TEXT)
    
    
    def allure_test_title(self,test_name):
        title = Config.get_value_of_info_key(test_name)
        allure.dynamic.title(title)
        # allure.dynamic.title("Verification of Observation code for all the findings in FHIR.json")

    def allure_test_description(self,test_name):
        title = Config.get_value_of_info_key(test_name)
        allure.dynamic.description(title)