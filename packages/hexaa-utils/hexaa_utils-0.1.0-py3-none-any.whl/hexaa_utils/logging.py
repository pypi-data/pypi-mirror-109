import logging

def get_logger(name, log_level):
    """ return a named logger """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # add handler to logger
    logger.addHandler(handler)
    return logger


def get_debug_logger(name):
    return get_logger(name, logging.DEBUG)


def get_info_logger(name):
    return get_logger(name, logging.INFO)


def get_warn_logger(name):
    return get_logger(name, logging.WARN)


def get_error_logger(name):
    return get_logger(name, logging.ERROR)


def get_fatal_logger(name):
    return get_logger(name, logging.FATAL)
