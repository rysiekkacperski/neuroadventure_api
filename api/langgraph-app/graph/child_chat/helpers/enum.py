from enum import Enum

class MoodEnum(str, Enum):
  HAPPY = "happy"
  SAD = "sad"
  NEUTRAL = "neutral"
  NERVOUS = "nervous"
  IRRITATED = "irritated"
  CURIOUS = "curious"