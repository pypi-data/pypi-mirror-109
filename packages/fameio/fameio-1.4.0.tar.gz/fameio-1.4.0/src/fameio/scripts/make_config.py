# !/usr/bin/env python
# -*- coding:utf-8 -*-
import logging as log

from fameio.source.cli import arg_handling_make_config
from fameio.source.logs import set_up_logger
from fameio.source.scenario import Scenario
from fameio.source.validator import SchemaValidator
from fameio.source.loader import load_yaml

from fameio.source.writer import ProtoWriter

DEFAULT_CONFIG = {"log_level": "warning", "log_file": None, "output_file": "config.pb", }


def get_config_or_default(config, default):
    """Returns specified `default` in case given `config` is None"""
    return default if config is None else config


def run(file, config=None):
    """Executes the main workflow for the building of a FAME configuration file"""
    config = get_config_or_default(config, DEFAULT_CONFIG)
    set_up_logger(level_name=config["log_level"], file_name=config["log_file"])

    scenario = Scenario(load_yaml(file))
    SchemaValidator.ensure_is_valid_scenario(scenario)

    writer = ProtoWriter(config["output_file"])
    writer.write_validated_scenario(scenario)

    log.info("Configuration completed.")


if __name__ == '__main__':
    input_file, run_config = arg_handling_make_config(DEFAULT_CONFIG)
    run(input_file, run_config)
