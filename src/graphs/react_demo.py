from langchain_openai.chat_models.base import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.tools.web_search import web_search
from src.tools.code_exec import python_inter


# 提示词模板
prompt = """
你是一名经验丰富的智能数据分析助手，擅长帮助用户高效完成以下任务：

1. Python代码执行：使用python_inter工具执行Python代码
2. 网络搜索：使用search_tool工具获取实时信息

所有回答均使用简体中文，清晰、礼貌、简洁。
"""

# 创建工具列表
tools = [web_search, python_inter]

# 创建模型
model = ChatOpenAI(model="Qwen3-Coder-30B-A3B-Instruct", temperature=0)

# 创建图（Agent）
react_demo_graph = create_react_agent(model=model, tools=tools, prompt=prompt)