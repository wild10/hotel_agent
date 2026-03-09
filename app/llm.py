# using wrapper of open ai sdk
from langchain_openai import ChatOpenAI
from openai import OpenAI

from app.config import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)

# function to ask and returns answer
# using the llm from OpenAI 

def ask_llm(my_prompt: str) -> str:
    # using the client for create anws.
    reponse = client.responses.create(
        model = "gpt-4.1-mini",
        input = my_prompt 
    )
    return reponse.output[0].content[0].text

def get_llm():
    return ChatOpenAI(
        model= "gpt-4.1-mini",
        temperature=0,
        api_key=OPEN_API_KEY
    )