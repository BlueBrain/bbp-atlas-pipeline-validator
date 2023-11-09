import json
import unittest
import pytest
from pipeline_validator.exceptions import (
    BrainRegionNotFoundException,
    IncorrectBrainRegionOrderException,
    InvalidCommandException,
)
from pipeline_validator.fetchers.brain_region_ontology_fetcher import (
    BrainRegionOntologyFetcher,
)
from pipeline_validator.tests.utils import load_params_from_json
from unittest.mock import patch
from pipeline_validator.validator.rule_validator import RuleValidator


class BrainRegionValidation(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def rules_config(self):
        with open("./tests/mocks/rule_config.json") as rule_config_file:
            rule_config = json.load(rule_config_file)
            self._rule_config = rule_config

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_brain_region_in_execution_is_present_in_ontology(
        self, fetch_brain_regions_ontology
    ):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )

        rule_execution = {
            "brainRegion": "http://api.brain-map.org/api/v2/data/Structure/1",
            "container": "docker://image-for-cerebellum-placement-hints",
            "CLI": {"command": "user_cli"},
        }

        RuleValidator(
            token="", config_file_json=self._rule_config, whitelisted_vars=[]
        ).validate_brain_region_existence(rule_execution["brainRegion"])

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_throws_exceptions_if_brain_region_is_not_present_in_ontology(
        self, fetch_brain_regions_ontology
    ):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )

        rule_execution = {
            "brainRegion": "http://api.brain-map.org/api/v2/data/Structure/8",
            "container": "docker://image-for-cerebellum-placement-hints",
            "CLI": {"command": "user_cli"},
        }

        with pytest.raises(BrainRegionNotFoundException):
            RuleValidator(
                token="", config_file_json=self._rule_config, whitelisted_vars=[]
            ).validate_brain_region_existence(rule_execution["brainRegion"])

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_correct_brain_regions_order(self, fetch_brain_regions_ontology):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )

        brain_regions = [
            "http://api.brain-map.org/api/v2/data/Structure/1",
            "http://api.brain-map.org/api/v2/data/Structure/2",
            "http://api.brain-map.org/api/v2/data/Structure/3",
        ]

        RuleValidator(
            token="", config_file_json=self._rule_config, whitelisted_vars=[]
        ).validate_order_of_brain_regions(brain_regions)

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_incorrect_brain_regions_order(self, fetch_brain_regions_ontology):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )

        brain_regions = [
            "http://api.brain-map.org/api/v2/data/Structure/1",
            "http://api.brain-map.org/api/v2/data/Structure/3",
            "http://api.brain-map.org/api/v2/data/Structure/2",
        ]

        with pytest.raises(IncorrectBrainRegionOrderException):
            RuleValidator(
                token="", config_file_json=self._rule_config, whitelisted_vars=[]
            ).validate_order_of_brain_regions(brain_regions)

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_correct_brain_regions_order_with_multiple_branches(
        self, fetch_brain_regions_ontology
    ):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )

        brain_regions = [
            "http://api.brain-map.org/api/v2/data/Structure/1",
            "http://api.brain-map.org/api/v2/data/Structure/2",
            "http://api.brain-map.org/api/v2/data/Structure/3",
            "http://api.brain-map.org/api/v2/data/Structure/4",
            "http://api.brain-map.org/api/v2/data/Structure/5",
        ]

        RuleValidator(
            token="", config_file_json=self._rule_config, whitelisted_vars=[]
        ).validate_order_of_brain_regions(brain_regions)

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_incorrect_brain_regions_order_with_multiple_branches(
        self, fetch_brain_regions_ontology
    ):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )

        brain_regions = [
            "http://api.brain-map.org/api/v2/data/Structure/5",
            "http://api.brain-map.org/api/v2/data/Structure/1",
            "http://api.brain-map.org/api/v2/data/Structure/2",
            "http://api.brain-map.org/api/v2/data/Structure/3",
            "http://api.brain-map.org/api/v2/data/Structure/4",
        ]

        with pytest.raises(IncorrectBrainRegionOrderException):
            RuleValidator(
                token="", config_file_json=self._rule_config, whitelisted_vars=[]
            ).validate_order_of_brain_regions(brain_regions)

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_correct_rules_command(self, fetch_brain_regions_ontology):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )
        RuleValidator(
            token="",
            config_file_json=self._rule_config,
            whitelisted_vars=["test1", "test2"],
        ).validate_command("mycommand --arg1 {test1} --ar2 {test2}")

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_rule_command_not_part_of_whitelisted(self, fetch_brain_regions_ontology):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )
        with pytest.raises(InvalidCommandException):
            RuleValidator(
                token="", config_file_json=self._rule_config, whitelisted_vars=["test1"]
            ).validate_command("mycommand --arg1 {test1} --ar2 {test2}")

    @patch.object(BrainRegionOntologyFetcher, "fetch_brain_regions_ontology")
    def test_rule_command_not_part_of_whitelisted(self, fetch_brain_regions_ontology):
        fetch_brain_regions_ontology.return_value = load_params_from_json(
            "./tests/mocks/brain_region_ontology.json"
        )
        RuleValidator(
            token="",
            config_file_json=self._rule_config,
            whitelisted_vars=["test1", "test2"],
        ).validate_command("mycommand --arg1 {test1}")
