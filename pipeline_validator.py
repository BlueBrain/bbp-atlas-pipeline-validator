import argparse
import json
from logger import logger
from validator.rule_validator import RuleValidator
from validator.schema_validator import SchemaValidator


def open_config(file: str) -> dict:
    with open(file) as f:
        file_json = json.load(f)
        return file_json


def pipeline_validator(file: str, token: str, whitelisted_vars: list):
    config_json = open_config(file)
    SchemaValidator(config_file_json=config_json).validate()
    RuleValidator(
        token=token, config_file_json=config_json, whitelisted_vars=whitelisted_vars
    ).validate()
    logger.info("Validation finished")
