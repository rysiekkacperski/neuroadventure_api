from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict
from child_chat.helpers.enum import MoodEnum

class DiagnosisType:
    """
        Validate diagnosis value given in the code
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

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls)

    def __getitem__(self, item):
        return self.value[item]

class MoodType:
    """
        Validate mood value given in the code
        Only choosen moods are acceptable
    """
    def __init__(self, value: str):
        self.value = value
        self.accessible_moods = [e.value for e in MoodEnum]
        
        if self.value not in self.accessible_moods:
            raise ValueError('Value must be compliant with values set in enum')

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls)

    def __getitem__(self, item):
        return self.value[item]