class BrainRegionNotFoundException(Exception):
    pass


class IncorrectBrainRegionOrderException(Exception):
    pass


class BrainRegionOntologyError(ConnectionRefusedError):
    pass


class InvalidCommandException(Exception):
    pass
