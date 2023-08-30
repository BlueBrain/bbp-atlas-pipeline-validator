import json
import requests
from pipeline_validator.config import BRAIN_REGION_ONTOLOGY_URL
from pipeline_validator.decorators import nexus_token_is_valid
from pipeline_validator.exceptions import BrainRegionOntologyError


class BrainRegionOntologyFetcher:
    def __init__(self, token) -> None:
        self.token = token

    @nexus_token_is_valid
    def fetch_brain_regions_ontology(self):
        """
        Fetches and returns the brain region ontology. First fetches the ontology resource, retrieves the JSON-LD file
        distribution URL and then retrieves the content of the file
        :return:
        """
        # retrieve the brain region ontology
        bro_resource_response = requests.get(
            BRAIN_REGION_ONTOLOGY_URL,
            headers={f"Authorization": f"Bearer {self.token}"},
        )

        if bro_resource_response.status_code == 200:
            bro_resource = json.loads(bro_resource_response.text)
            # find the distribution whose encoding format is JSON-LD
            json_distribution_url = next(
                distribution["contentUrl"]
                for distribution in bro_resource["distribution"]
                if distribution["encodingFormat"] == "application/ld+json"
            )
            # retrieve the actual ontology
            bro_file_response = requests.get(
                json_distribution_url,
                headers={"Accept": "*/*", f"Authorization": f"Bearer {self.token}"},
            )
            if bro_file_response.status_code == 200:
                return json.loads(bro_file_response.text)
            else:
                raise BrainRegionOntologyError(
                    "Brain region ontology could not be fetched"
                )
        else:
            raise BrainRegionOntologyError("Brain region ontology could not be fetched")
