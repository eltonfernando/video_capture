# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from .logger import LoggerConfig


def default_log():

    version = os.getenv("__VERSION__", "0.0.0")
    version = version.replace(".", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d")

    name_log = f"capture_{timestamp}_v{version}.log"
    path_log = os.path.join("log", name_log)

    level = logging.INFO
    if os.environ.get("LOG_LEVEL") == "DEBUG":
        level = logging.DEBUG

    LoggerConfig(
        console_level=level,
        file_level=logging.DEBUG,
        path_logger=path_log,
    )
