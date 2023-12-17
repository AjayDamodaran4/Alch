from .config_reader import Config


class URLConstant(object):
    APP_NAME = "/aiservice/2/"
    LIVENESS_ENDPOINT = "live"
    READINESS_ENDPOINT = "ready"
    JOBS_ENDPOINT = "jobs"
    SHUTDOWN_ENDPOINT = "shutdown"

    def get_url(self, url_key, app_name=APP_NAME):
        base_url = Config.get_value_of_config_key('base_url')
        base_url = base_url.format(host=Config.get_value_of_config_key("host"), port=Config.get_value_of_config_key("port"))
        url = base_url + app_name + url_key
        return url




