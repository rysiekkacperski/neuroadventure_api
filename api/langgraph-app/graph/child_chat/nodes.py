from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate

from child_chat.helpers.formatter import SocialFormatter, EmotionFormatter, SentimentFormatter, FormatDiagnosis
from child_chat.helpers.enum import MoodEnum
from child_chat.helpers.messages import format_messages_for_prompt
from child_chat.helpers.validation import DiagnosisType
from child_chat.state import ChildState
from child_chat.model import llm

def assess_social_context(state: ChildState):
  socialContextPrompt = """You are a therapist of neurodivergent children. Neurodivergent kid is talking with you. Assess the probability [social_p], from 0 to 1, 
  that content of previous messages concerns social scenario experienced by a child. Remember that you should assess only HumanMessages, the ones written by a child."""
  
  llm_with_structured_output = llm.with_structured_output(SocialFormatter)
  messages = add_messages(state.messages, HumanMessage(content=socialContextPrompt))

  probability = llm_with_structured_output.invoke(messages)

  if probability.social_p >= 0.75:
    return {'isSocialContext': True}
  else:
    return {'isSocialContext': False}

def assess_emotional_context(state: ChildState):
  emotionContextPrompt = """You are a therapist of neurodivergent children. Neurodivergent kid is talking with you. Assess the probability [emotion_p], from 0 to 1, 
  that content of previous messages can involve any child's emotions. Remember that you should assess only HumanMessages, the ones written by a child"""
  
  llm_with_structured_output = llm.with_structured_output(EmotionFormatter)
  messages = add_messages(state.messages, HumanMessage(content=emotionContextPrompt))

  probability = llm_with_structured_output.invoke(messages)

  if probability.emotion_p >= 0.75:
    return {'isEmotionalContext': True}
  else:
    return {'isEmotionalContext': False}
  
def analyze_mood(state: ChildState):

  def moodAnalyzePrompt():
    #create a string from enum of moods given
    accessible_moods = ', '.join([e.value for e in MoodEnum])
    return (f"""You are a therapist of neurodivergent children. Assess the sentiment of previous messages (mood of a child) in one 
    of those emotions: {accessible_moods}. Remember that you should assess only HumanMessages, the ones written by a child. Additionally, if you think 
    that more than adjective complies with the criteria, then pick the one which describe better the newest messages""")
  
  llm_with_structured_output = llm.with_structured_output(SentimentFormatter)
  messages = add_messages(state.messages, HumanMessage(content=moodAnalyzePrompt()))

  sentiment = llm_with_structured_output.invoke(messages)

  if sentiment.sentiment is not None:
    return {'mood': sentiment.sentiment.value}
  else:
    return {'mood': state.mood}
  
#Generate the LLM model response based on current state
def generate_response(state: ChildState):
    
    #Get current values from the state
    child_current_mood = state.mood
    social_context_present = state.isSocialContext
    emotional_context_present = state.isEmotionalContext
    child_name = state.name
    child_diagnosis = state.diagnosis
    child_age = state.age
    language = state.language

    #Format recent messages for context
    formatted_history = format_messages_for_prompt(state.messages)

    def childChatBotSystemMessage(diagnosis: DiagnosisType, age: int):
        return (f'''Pretend to be a terapist who talks with a neurodivergent kid. Their diagnosis is {FormatDiagnosis(diagnosis)}. Kid is {age} years old. 
                Remember that neurodivergent kids have special language needs. You should be very detailed but concise in the same time.''')

    #Instruction for a response generation
    def responsePrompt(social_context: bool, emotional_context: bool, mood: str, name: str, language: str, history: str):
        return(f"""
            As a therapist create a response to a message of a neurodivergent child.

            RESPONSE RULES:
            - Current mood of a child is: {mood}
            - If mood is 'sad', 'nervous', or 'irritated': Generate a calming, validating, supportive message.
            - If mood is 'happy' or 'curious': Generate a praising, encouraging, engaging message. 
            - If mood is 'neutral', generate message which will try changin the mood to 'happy' or 'curious'.
            - If Social Context Present is False (Current state: {social_context}): Make the response have a question 
                which would cause a child to share experienced social scenario but if there is a factual question/statement in place also respond clearly. 
                The question should be connected with a factual question/statement and very precise (about one concrete social scenario). 
            - If Emotional Context Present is False (Current state: {emotional_context}): Make the response have a question or statement 
                which would cause a child to share experienced emotions but if there is a factual question/statement in place also respond clearly.
                The question should be connected with a factual question/statement and very precise (about one concrete emotion). 
            - If both contexts are False, you can combine the questions or choose one.
            - Address the child by name ({name}) occasionally.
            - Respond ONLY in language: {language}.

            RECENT CONVERSATION HISTORY:
            {history}

            Based on the rules and context above, generate your response to the child's last message.
            Generate ONLY the response text.
        """
        )

    #Construct the prompt 
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=childChatBotSystemMessage(child_diagnosis, child_age)),
        HumanMessage(content=responsePrompt(social_context_present, emotional_context_present, child_current_mood, child_name, language, formatted_history))
    ])

    #Invoke the LLM with the constructed prompt
    chain = prompt_template | llm
    response_content = chain.invoke({}).content # Pass empty dict as input because template handles entire necessary context 

    # Return the message to be added to the state
    # LangGraph's `add_messages` handles appending this
    return {"messages": [AIMessage(content=response_content)]}