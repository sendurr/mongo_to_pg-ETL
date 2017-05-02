import datetime  # noqa
import logging

from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter, object):
    """Based on the logmatic library and schema."""

    def __init__(self,  # noqa
                 fmt="%(asctime) %(name) %(processName) %(filename) " \
                        "%(funcName) %(levelname) %(lineno) %(module) %(threadName) %(message)",
                 datefmt="%Y-%m-%dT%H:%M:%SZ%z",
                 style='%',
                 extra={}, *args, **kwargs):
        self._extra = extra
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, datefmt=datefmt, *args, **kwargs)

    def process_log_record(self, log_record):  # noqa
        # Enforce the presence of a timestamp
        if "asctime" in log_record:
            log_record["timestamp"] = log_record["asctime"]
        else:
            log_record["timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ%z")

        if self._extra is not None:
            for key, value in self._extra.items():
                log_record[key] = value
        return super(JsonFormatter, self).process_log_record(log_record)


def json_logger(level='INFO'):
    """Start a logger called with a logging level `level`."""
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    # configure logging
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
