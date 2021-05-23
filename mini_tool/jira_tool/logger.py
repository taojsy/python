"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
import logging
import os
from work_path import WorkPath


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logfile = os.path.join(WorkPath().directory(), "log.txt")
    fh = logging.FileHandler(logfile, mode="a")
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s -%(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = set_logger()
