# import pydantic to validate data passed to the state
from pydantic import BaseModel, field_validator
from typing import Annotated

#import langgraph modules
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from child_chat.helpers.validation import DiagnosisType, MoodType
from child_chat.helpers.enum import MoodEnum

class ChildState(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages]
    name: str
    age: int 
    diagnosis: DiagnosisType
    language: str
    mood: MoodType = MoodEnum.NEUTRAL
    isSocialContext: bool = False
    isEmotionalContext: bool = False

    @field_validator('age')
    @classmethod
    def validate_age(cls, value):
        # Ensure the person is a child
        if value >= 18:
            raise ValueError("The person is not a child")
        return value

    @field_validator('language')
    @classmethod
    def validate_language(cls, value):
        # Ensure the language code is proper according to ISO standards
        if len(value) != 2:
            raise ValueError("Given language is not valid language code")
        return value