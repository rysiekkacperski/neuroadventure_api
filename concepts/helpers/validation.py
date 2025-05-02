from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict

class Diagnosis:
    """
        validate diagnosis given in the code
        Only a dict of diagnosis booleans is acceptable e.g. {"adhd": bool, "spectrum": bool}
    """
    def __init__(self, value: Dict[str, bool]):
        self.value = value
        if not isinstance(value, dict):
            raise TypeError("Diagnosis must be a dict")
        if set(value.keys()) != {"adhd", "spectrum"}:
            raise ValueError("Diagnosis must have keys 'adhd' and 'spectrum'")
        if not isinstance(value["adhd"], bool) or not isinstance(value["spectrum"], bool):
            raise TypeError("Both 'adhd' and 'spectrum' must be booleans")
        if not (value["adhd"] or value["spectrum"]):
            raise ValueError("At least one of 'adhd' or 'spectrum' must be True")

    def __repr__(self):
        match (self.value["adhd"], self.value["spectrum"]):
            case (True, True):
                status = "ADHD and autism spectrum"
            case (True, False):
                status = "ADHD"
            case (False, True):
                status = "autism spectrum"
        return status

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls)

    def __getitem__(self, item):
        return self.value[item]

