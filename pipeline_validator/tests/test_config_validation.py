import json
import unittest
import pytest
from jsonschema.exceptions import ValidationError
from pipeline_validator.validator.schema_validator import SchemaValidator


class TestRulesConfigValidation(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def rules_config(self):
        with open("./tests/mocks/rule_config.json") as rule_config_file:
            rule_config = json.load(rule_config_file)
            self._rule_config = rule_config

    def test_correct_rules_config(self):
        SchemaValidator(config_file_json=self._rule_config).validate()
        assert True

    def test_rules_config_if_rules_is_missing(self):
        changed_config = self._rule_config
        del changed_config["rules"]
        with pytest.raises(ValidationError):
            SchemaValidator(config_file_json=changed_config).validate()

    def test_rules_config_if_brain_region_is_missing(self):
        """brainRegion is a required attribute"""
        changed_config = self._rule_config
        del changed_config["rules"][0]["execute"][0]["brainRegion"]
        with pytest.raises(ValidationError):
            SchemaValidator(config_file_json=changed_config).validate()

    def test_rules_config_if_command_is_missing(self):
        """CLI is a required attribute"""
        changed_config = self._rule_config
        del changed_config["rules"][0]["execute"][0]["CLI"]
        with pytest.raises(ValidationError):
            SchemaValidator(config_file_json=changed_config).validate()

    def test_rules_config_if_container_is_missing(self):
        """container is an optional attribute"""
        changed_config = self._rule_config
        del changed_config["rules"][0]["execute"][0]["container"]
        try:
            SchemaValidator(config_file_json=changed_config).validate()
            assert True
        except ValidationError:
            assert False

    def test_rules_config_if_execute_is_missing(self):
        """container is an optional attribute"""
        changed_config = self._rule_config
        del changed_config["rules"][0]["execute"]
        with pytest.raises(ValidationError):
            SchemaValidator(config_file_json=changed_config).validate()

    def test_rules_config_if_container_does_not_start_with_docker_pattern(self):
        changed_config = self._rule_config
        changed_config["rules"][0]["execute"][0][
            "container"
        ] = "image-for-cerebellum-placement-hints"
        with pytest.raises(ValidationError):
            SchemaValidator(config_file_json=changed_config).validate()

    def test_rules_config_if_container_has_whitespace(self):
        changed_config = self._rule_config
        changed_config["rules"][0]["execute"][0][
            "container"
        ] = "docker://image-for-cerebellum placement-hints"
        with pytest.raises(ValidationError):
            SchemaValidator(config_file_json=changed_config).validate()
