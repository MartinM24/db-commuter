# -*- coding: utf-8 -*-

"""
database manager for running db-commuter methods
"""

import argparse
import logging

from os import path, getenv
from dotenv import load_dotenv

from app import config

logging.basicConfig(
    format='%(asctime)s | %(name)s | %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('db_commuter')


def main(args):
    if path.isfile(config.path2env):
        load_dotenv(config.path2env)

    logger.info('completed')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='database manager',
        formatter_class=argparse.RawTextHelpFormatter)

    args = vars(arg_parser.parse_args())

    main(args)
