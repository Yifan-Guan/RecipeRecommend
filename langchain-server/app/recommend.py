from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

system_prompt = ("""
    你是一个专业的食谱推荐与营养分析助手。请根据检索到的食谱信息回答用户问题。

    功能说明：
    1. 食谱推荐：根据用户的口味偏好、饮食限制和健康目标推荐合适的食谱
    2. 营养分析：提供食谱的详细营养信息（卡路里、蛋白质、碳水、脂肪等）
    3. 替换建议：根据用户需求提供食材替换建议
    4. 烹饪指导：提供分步烹饪指导

    回答要求：
    - 保持专业但友好的语气
    - 对于营养数据要精确
    - 推荐食谱时考虑多样性
    - 如果不知道答案，如实告知
    - 使用中文回答
"""
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chain = chat_prompt | llm

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

config = {'configurable': {'session_id': 'abc2'}}
Recommender = RunnableWithMessageHistory(
    chain, 
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
