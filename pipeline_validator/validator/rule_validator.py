import re

from bigtree import find_names, find_name
from pipeline_validator.exceptions import (
    BrainRegionNotFoundException,
    IncorrectBrainRegionOrderException,
    InvalidCommandException,
)
from pipeline_validator.fetchers.brain_region_ontology_fetcher import (
    BrainRegionOntologyFetcher,
)
from pipeline_validator.logger import logger
from pipeline_validator.validator.brain_region_tree_handler import (
    BrainRegionTreeHandler,
)
from pipeline_validator.validator.validator import Validator


class RuleValidator(Validator):
    def __init__(
        self, token: str, config_file_json: dict, whitelisted_vars: list
    ) -> None:
        super().__init__(config_file_json)
        self.token = token
        brain_regions_ontology = BrainRegionOntologyFetcher(
            token=token
        ).fetch_brain_regions_ontology()
        self.brain_region_tree = BrainRegionTreeHandler(
            brain_regions_ontology["defines"]
        )
        self.whitelisted_vars = whitelisted_vars

    def validate_brain_region_existence(self, brain_region_id: str):
        """
        Checks whether the brain region exists in the rule execution.

        If not, throws BrainRegionNotFoundException

        :param brain_region_id: the id of the brain region
        :return:
        """
        # querying the tree to find the brain region
        region_found = find_names(self.brain_region_tree.tree, brain_region_id)
        if not region_found:
            raise BrainRegionNotFoundException(
                f"Brain region {brain_region_id} is not present in the ontology"
            )

    def validate_order_of_brain_regions(self, brain_regions):
        """
        Given a list of brain regions, checks whether each brain region is a descendant of each previous one (if they are related)
        :param brain_regions:
        :return:
        """
        # avoid the first one since there is no previous brain region to check
        for index, brain_region in enumerate(brain_regions):
            # get all the previous brain regions
            previous_brain_regions = brain_regions[index - 1 : index]
            checking_node = find_name(self.brain_region_tree.tree, brain_region)
            for previous_brain_region in previous_brain_regions:
                ancestry_correct = (
                    self.brain_region_tree.check_ancestry_order_between_regions(
                        previous_brain_region, checking_node
                    )
                )
                if not ancestry_correct:
                    raise IncorrectBrainRegionOrderException(
                        f"Brain region {checking_node.name} can not be customized after {previous_brain_region} "
                        f"because region {previous_brain_region} is part of {checking_node.name}"
                    )

    def validate_command(self, command_var: str):
        # get all command variables using regular expression
        command_vars = re.findall("{(.*?)}", command_var)
        for command_var in command_vars:
            if command_var not in self.whitelisted_vars:
                raise InvalidCommandException(
                    f"{command_var} not part of accepted variables"
                )

    def validate_rule_executions(self, rule_executions):
        """
        Validates the array of executions by checking the validity of 2 conditions:

        1) That all the brain regions mentioned are present in the brain region ontology
        2) That the brain regions are provided in the correct order based on the ancestry order of the ontology

        :param rule_executions: the array of rule executions
        :return:
        """
        brain_regions = []
        for rule_execution in rule_executions:
            # first check if the brain region exists
            self.validate_brain_region_existence(rule_execution["brainRegion"])
            brain_regions.append(rule_execution["brainRegion"])
            if "args" in rule_execution["CLI"]:
                self.validate_command(rule_execution["CLI"]["args"])
        # then check if the brain regions appear in the correct order within the execution
        self.validate_order_of_brain_regions(brain_regions)

    def validate(self):
        logger.info("Validating rules...")
        rules = self.config_file_json["rules"]
        for rule in rules:
            rule_name = rule["rule"]
            logger.info(f"Validating rule {rule_name}...")
            self.validate_rule_executions(rule_executions=rule["execute"])
