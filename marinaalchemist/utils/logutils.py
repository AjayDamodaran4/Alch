import logging
from logging.handlers import RotatingFileHandler
import time
import platform, os


class Singleton(object):
    __log_handler = None
    __log_path = "results/logresults/"

    @classmethod
    def get_log_handler(cls):
        """
        Singleton patter for logger instance.
        :return:
        log_handler : Return the log handler.
        log_path : Return the path for the log file.
        """
        if cls.__log_handler is None:
            daytime_stamp = time.strftime("%m-%d-%Y_%H-%M:%S", time.gmtime())
            if platform.system() == "Windows":
                cls.__log_path += "log_file_" + daytime_stamp + ".log"
                cls.__log_path = "\\".join(cls.__log_path.split("/"))
                # path = os.getcwd() + "\\" + cls.__log_path
                # print(cls.__log_path)
            else:
                cls.__log_path += "log_file_" + daytime_stamp + ".log"
            file_handler = logging.FileHandler(filename=cls.__log_path)
            cls.__log_handler = file_handler
        return cls.__log_handler, cls.__log_path


class LogUtils(object):

    @staticmethod
    def get_log_instance(file_trace):
        """
        This method returns the logger instance.

        Accepts the file trace to insert in the log file for tracking and return the logger instance.

        :parameter
        file_trace (str) : Contains the trace back in format directory_name :: test_directory::module_name::test_name
        :return
        logger (log instance) ; Return the log instance to use with other modules.

        """
        try:
            file_handler, log_path = Singleton().get_log_handler()
            logger = logging.getLogger(file_trace)
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s |' + file_trace + ' | %(levelname)s' + ' : ')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            rotate_handler = RotatingFileHandler(log_path, maxBytes=100000000, backupCount=10)
            logger.addHandler(rotate_handler)
            return logger
        except Exception as e:
            print("An exception was thrown in log")
            print(type(e).__name__)


if __name__ == '__main__':
    LogUtils.get_log_instance("testmm")
