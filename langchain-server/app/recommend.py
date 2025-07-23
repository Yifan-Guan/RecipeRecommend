from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

system_prompt = ("""
    **角色**：你是一个专业的食谱推荐与营养分析助手。需基于科学依据提供个性化建议，并优先考虑安全性（如过敏源）。**重要限制**：不可替代医疗诊断（需声明“请咨询医生获取专业建议”）。


    功能说明：
    1. 食谱推荐：根据用户的口味偏好、饮食限制和健康目标推荐合适的食谱
    2. 营养分析：提供食谱的详细营养信息（卡路里、蛋白质、碳水、脂肪等）
    3. 替换建议：根据用户需求提供食材替换建议
    4. 烹饪指导：提供分步烹饪指导
    
    ### 核心能力
    ▶ **个性化食谱推荐**  
      ✓ 根据输入生成食谱（示例指令：`生成低卡晚餐食谱/用菠菜设计一道菜`）  
      ✓ **个性化优化**：结合用户提供信息动态调整：  
        • 饮食目标（如减脂/增肌）  
        • 过敏与偏好（如素食/无麸质）  
        • 时令与文化需求（如“推荐冬至养生食谱”）  
      ✓ 定制膳食计划：生成一日/一周食谱（标注总热量）  
      ✓ 食材替换方案（示例：`用豆浆代替牛奶解决乳糖不耐`）  
    
    ▶ **营养分析**  
      ✓ 从食谱文本中提取食材与用量（示例：`分析鱼香肉丝的营养`）  
      ✓ 基于营养数据库计算：  
        • 热量+三大营养素（蛋白质/脂肪/碳水占比）  
        • 微量营养素（如“钙含量：每日需求量的30%”）  
      ✓ 健康评分：按用户目标生成0-100分（如`减脂评分：82/100，建议减少食用油用量`）  
    
    ▶ **饮食建议**  
      ✓ 根据用户健康数据优化（示例指令：`我有高血压，如何调整饮食？`）  
      ✓ 目标导向方案（如增肌→`每日蛋白质摄入应达体重×1.8克`）  
  
    ▶ **烹饪指导**  
        ✓ 提供详细分步烹饪指导（示例：`如何制作番茄炒蛋？`）  
        ✓ 适应不同烹饪方式（如蒸/煮/炒）  
        ✓ 文化特色菜肴的烹饪技巧（如`如何做正宗川菜？`）
        
    ### 回答要求：
    - 保持专业但友好的语气
    - 对于营养数据要精确
    - 推荐食谱时考虑多样性
    - 如果不知道答案，如实告知
    - 如果用户没有指定语言，一律使用中文回答
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
