# encoding: utf-8

import os
import logging

# enable python env
os.sys.path.append(os.getcwd())

# enable logging debug
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

