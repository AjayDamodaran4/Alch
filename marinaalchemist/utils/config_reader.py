import json


class Config(object):
    __path_config = "properties/config.json"
    __path_test_input = "properties/test_input.json"
    __path_info = "properties/info.json"
    json_file = None

    @classmethod
    def get_value_of_config_key(cls, key):
        """
        Used to access the config.json file with Key name.
        :param key: Key name that which is required.
        :return: Value of the key from the config.json
        """
        with open(cls.__path_config) as f:
            my_json = json.load(f)
            return my_json.get(key)

    @classmethod
    def get_value_of_test_input_key(cls, key):
        with open(cls.__path_test_input) as f:
            my_json = json.load(f)
            return my_json.get(key)
    
    @classmethod
    def get_value_of_info_key(cls, key):
        with open(cls.__path_info) as f:
            my_json = json.load(f)
            return my_json.get(key)
    
    
    @classmethod
    def update_value_of_config_key(cls, key, value):
        """
        Used to access the config.json file with Key name.
        :param key: Key name that which is required.
        :return: Value of the key from the config.json
        """
        with open(cls.__path_config) as f:
            my_json = json.load(f)
            my_json[key] = str(value)
        with open(cls.__path_config, 'w') as f:
            json.dump(my_json, f, indent=2)
