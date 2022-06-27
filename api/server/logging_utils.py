import copy
import logging
import os
import re
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger


try:  # Python 2.7+
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            # do nothing
            pass


class DynamicRotatingFileHandler(object):
    def __new__(cls, *args, **kw):
        log_path = kw.pop("log_path")
        filename = kw.pop("filename", None)

        if filename:
            kw["filename"] = os.path.join(log_path, filename)
            return RotatingFileHandler(*args, **kw)
        else:
            return NullHandler()


class JsonFormatter(jsonlogger.JsonFormatter):

    def __init__(self, *args, **kwargs):
        """
            :param default_logsindex: default static logsindex for formatter
        """
        self.default_logsindex = kwargs.pop("default_logsindex", None)
        super(JsonFormatter, self).__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp", None):
            log_record["timestamp"] = record.created

        if not log_record.get("logsindex"):
            log_record["logsindex"] = self.default_logsindex \
                if self.default_logsindex else re.sub(r"(?<!^)(?=[A-Z])", "_", record.name).lower()


class WorkerLoggingAdapter(logging.LoggerAdapter):
    """Need that to allow arbitrary extra parameters of logging calls to appear in Kibana
    https://docs.python.org/3.6/howto/logging-cookbook.html#using-loggeradapters-to-impart-contextual-information
    """

    def process(self, msg, kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"].update(self.extra)
        return msg, kwargs


def parse_logging_config(logger_name, config):
    dedicated_logger = config["loggers"].get(logger_name, None)
    generic_jl_logger = config["loggers"].get("generic_jl_logger", None)
    if dedicated_logger:
        return config
    elif generic_jl_logger:
        config["loggers"][logger_name] = copy.deepcopy(config["loggers"]["generic_jl_logger"])

        if "dynamic_jl_file_handler" in config["loggers"][logger_name]["handlers"]:
            fh_name = logger_name + "_jl_file_handler"
            config["loggers"][logger_name]["handlers"].remove("dynamic_jl_file_handler")

            config["handlers"][fh_name] = copy.deepcopy(config["handlers"]["dynamic_jl_file_handler"])
            config["handlers"][fh_name]["filename"] = logger_name + ".log"

            config["loggers"][logger_name]["handlers"].append(fh_name)

        return config
    else:
        config["loggers"][logger_name] = copy.deepcopy(config["loggers"]["default"])
        return config
