from .config_reader import Config
from .docker_utils import DockerUtils


class SimulatorUtils(object):
    APP_NAME = "/aiservice/2/"

    def get_url(self, url_key, app_name=APP_NAME):
        base_url = Config.get_value_of_config_key('base_url')
        base_url = base_url.format(host=Config.get_value_of_config_key("host"), port=Config.get_value_of_config_key("port"))
        url = base_url + app_name + url_key
        return url




