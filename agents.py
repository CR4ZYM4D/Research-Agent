from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url
import os
import sys
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
            model = 'gemini-2.0-flash',
            temperature = 0.5,
            max_retries = 3
        )

def build_agent():

    return create_agent(model = llm, tools = [web_search])

def build_reader():

    return create_agent(model = llm, tools = [scrape_url])

