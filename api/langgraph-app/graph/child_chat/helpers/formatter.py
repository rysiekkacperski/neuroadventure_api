from pydantic import BaseModel, Field

from child_chat.helpers.enum import MoodEnum

class SocialFormatter(BaseModel):
  social_p: float = Field(description='Probability of social context occurence')

class EmotionFormatter(BaseModel):
  emotion_p: float = Field(description='Probability of emotion occurence')

class SentimentFormatter(BaseModel):
  sentiment: MoodEnum = Field(description="""One of the moods from ['happy', 'sad', 'neutral', 'nervous', 'irritated', 'curious']""")

def FormatDiagnosis(diagnosis_dict):
  match (diagnosis_dict["adhd"], diagnosis_dict["spectrum"]):
    case (True, True):
      status = "ADHD and autism spectrum"
    case (True, False):
      status = "ADHD"
    case (False, True):
      status = "autism spectrum"
  return status