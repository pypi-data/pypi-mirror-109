# -*- coding:utf-8 -*-

import argparse

from fameio.source.logs import LOG_LEVELS


def arg_handling_make_config(defaults):
    """Handles command line arguments and returns `input_file` and `run_config` for make_config routine"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        required=True,
                        help=("Provide path to configuration file"
                              "Example: -f <path/to/configuration/file.yaml>'"),
                        )

    add_log_level_argument(parser, defaults["log_level"], LOG_LEVELS)
    add_output_argument(parser, defaults["output_file"])
    add_logfile_argument(parser)

    args = parser.parse_args()

    input_file = args.file
    level = args.log
    output_file = args.output
    log_file = args.logfile

    run_config = {"log_level": level,
                  "output_file": output_file,
                  "log_file": log_file,
                  }

    return input_file, run_config


def arg_handling_convert_results(defaults):
    """Handles command line arguments and returns `input_file` and `run_config` for convert_results routine"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        required=True,
                        help=("Provide path to protobuf file"
                              "Example: -f <path/to/result/file.pb>'"),
                        )

    add_log_level_argument(parser, defaults["log_level"], LOG_LEVELS)
    add_logfile_argument(parser)
    add_select_agents_argument(parser)

    args = parser.parse_args()

    input_file = args.file
    level = args.log
    log_file = args.logfile
    agents_to_extract = args.agents

    run_config = {"log_level": level,
                  "log_file": log_file,
                  "agents_to_extract": agents_to_extract,
                  }

    return input_file, run_config


def add_select_agents_argument(parser):
    """Adds argument handling for selecting agent types which get converted"""
    parser.add_argument("-a",
                        "--agents",
                        nargs="*",
                        type=str,
                        help=("Provide list of agents to extract. "
                              "Example --agents MyAgent1 MyAgent2 default='None'"),
                        )


def add_logfile_argument(parser):
    """Adds argument handling for setting the logfile"""
    parser.add_argument("-lf",
                        "--logfile",
                        help=("Provide logging file. "
                              "Example --logfile <path/to/log/file.log>', default='None'"),
                        )


def add_output_argument(parser, defaults):
    """Adds argument handling for setting the output file"""
    parser.add_argument("-o",
                        "--output",
                        default=defaults,
                        help=("Provide path to config.pb file. "
                              "Example --output <path/to/config.pb>', default='config.pb'"),
                        )


def add_log_level_argument(parser, defaults, levels):
    """Adds argument handling for setting the log_level"""
    parser.add_argument("-l",
                        "--log",
                        default=defaults,
                        choices=list(levels.keys()),
                        help=("Provide logging level. "
                              "Example --log debug', default='info'"),
                        )
