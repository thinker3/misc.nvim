#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from logging.handlers import RotatingFileHandler

from .. import config

DEBUG_PLUS = 15
logging.addLevelName(DEBUG_PLUS, "DEBUG_PLUS")
LOG_FORMAT = '[%(asctime)s - %(levelname)s] %(pathname)s...%(funcName)s, line %(lineno)s > %(message)s'


def deplus(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_PLUS):
        self._log(DEBUG_PLUS, message, args, **kws)


logging.Logger.deplus = deplus


def get_logger():
    logger = logging.getLogger()
    if logger.level == DEBUG_PLUS:
        return logger

    logger.setLevel(DEBUG_PLUS)
    debug_handler = RotatingFileHandler(
        config.log_path,
        maxBytes=1024 * 1024 * 5,
        backupCount=0,
    )
    debug_handler.setLevel(DEBUG_PLUS)
    formatter = logging.Formatter(LOG_FORMAT)
    debug_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(debug_handler)
    return logger


logger = get_logger()
