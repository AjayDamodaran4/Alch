import json


class Config(object):
    __path_config = "properties/config.json"
    __path_test_input = "properties/test_input.json"
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
