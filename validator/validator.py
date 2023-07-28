from abc import abstractmethod


class Validator:
    def __init__(self, config_file_json) -> None:
        self.config_file_json = config_file_json

    @abstractmethod
    def validate(self):
        pass
