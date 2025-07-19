from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

prompt_template = PromptTemplate.from_template("{msg}")
model = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)
parser = StrOutputParser()

chain = prompt_template | model | parser

if __name__ == "__main__":
    response = chain.stream("hello")
    print(response)
    for chunk in response:
        print(chunk, end="|", flush=True)