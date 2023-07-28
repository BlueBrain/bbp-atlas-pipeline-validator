import json
import pathlib
from jsonschema.validators import validate
from pipeline_validator.logger import logger
from pipeline_validator.validator.validator import Validator


class SchemaValidator(Validator):
    def __init__(self, config_file_json: dict) -> None:
        super().__init__(config_file_json)

    def validate(self):
        """
        Validates the provided configuration against the rules json schema
        :param config_file_json: the config file content
        :return:
        """
        cwd = str(pathlib.Path(__file__).parent.resolve())
        with open(cwd + "/schemas/rules_schema.json") as rules_schema_file:
            rules_json_schema = json.load(rules_schema_file)
            logger.info("Validating file schema...")
            validate(self.config_file_json, rules_json_schema)
            logger.info("File schema is validated...")
