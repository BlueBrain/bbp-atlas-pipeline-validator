# Pipeline Validator


## Install

You can install the file by using `pip install bbp-atlas-pipeline-validator`


## Examples

You can use the validator in the following way:

```python
from pipeline_validator.pipeline_validator import pipeline_validator

path_to_file = "./my_config.json"
token = "THIS_IS_MY_NEXUS_TOKEN"
whitelisted_vars = ["var1", "var2"]

pipeline_validator(path_to_file, token, whitelisted_vars)
```

where:

- `path_to_file` is the relative path to the configuration
- `token` is a valid nexus token
- `whitelisted_vars` is an array of accepted variables


## Configuration Format

The JSON configuration file should be in the following format:

```json
{
  "rules":[
    {
      "rule": "<NAME_OF_RULE_1>",
      "execute":
        [
          {
            "brainRegion": "http://api.brain-map.org/api/v2/data/Structure/<BRAIN_REGION_ID_1>",
            "container": "docker://<PATH_TO_DOCKER_IMAGE>",
            "command": "<THE COMMAND TO BE EXECUTED>"
          },
          {
            "brainRegion": "http://api.brain-map.org/api/v2/data/Structure/<BRAIN_REGION_ID_2>",
            "container": "docker://<PATH_TO_DOCKER_IMAGE>",
            "command": "<THE COMMAND TO BE EXECUTED>"
          }
        ]
    },
    {
      "rule": "<NAME_OF_RULE_2>",
      "execute":
        [
          {
            "brainRegion": "http://api.brain-map.org/api/v2/data/Structure/<BRAIN_REGION_ID_1>",
            "container": "docker://<PATH_TO_DOCKER_IMAGE>",
            "command": "<THE COMMAND TO BE EXECUTED>"
          },
          {
            "brainRegion": "http://api.brain-map.org/api/v2/data/Structure/<BRAIN_REGION_ID_2>",
            "container": "docker://<PATH_TO_DOCKER_IMAGE>",
            "command": "<THE COMMAND TO BE EXECUTED>"
          }
        ]
    }
  ]
}
```


## Validation Criteria

The following criteria need to be met in order for the configuration to be validated:

- The configuration need to follow the above JSON schema
- Brain region ID should be valid (exist in brain region ontology)
- Within each rule, each brain region need to be followed by brain region that are not related or that they are descendants in the ontology
- For each command, the variables passed need to be part of the whitelisted variables


## Funding & Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, a 
research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss 
government’s ETH Board of the Swiss Federal Institutes of Technology.

Copyright © 2023-2024 Blue Brain Project/EPFL
