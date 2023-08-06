__version__ = '0.1.6'

import logging
import cleanlog.formatter as cf
import cleanlog.handler as ch

# Integer representation of level names.
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def BasicLogger(name=None, handler=None, *args, **kwargs):
    """
    """
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        if handler is None:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(cf.BasicFormatter())
            logger.addHandler(stream_handler)

        elif isinstance(handler, list):
            for hndlr in handler:
                hndlr.setFormatter(cf.BasicFormatter())
                logger.addHandler(hnldr)

        else:
            handler.setFormatter(cf.BasicFormatter())
            logger.addHandler(handler)

    return logger

def ColoredLogger(name=None, handler=None, *args, **kwargs):
    """
    """
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        if handler is None:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(cf.ColoredFormatter())
            logger.addHandler(stream_handler)

        elif isinstance(handler, list):
            for hndlr in handler:
                hndlr.setformatter(cf.ColoredFormatter())
                logger.addHandler(hnldr)

        else:
            handler.setFormatter(cf.ColoredFormatter())
            logger.addHandler(handler)

    return logger


# Wrap logging.getLogger just for convenience.
getLogger = logging.getLogger

# Aliases.
basic_logger = BasicLogger
colored_logger = ColoredLogger
