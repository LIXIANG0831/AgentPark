from dotenv import load_dotenv
from langchain_openai.chat_models.base import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_tavily import TavilySearch

# 加载环境变量
load_dotenv(override=True)

# 创建Tavily搜索工具
search_tool = TavilySearch(max_results=5, topic="general")


# Python代码执行工具参数模型
class PythonCodeInput(BaseModel):
    py_code: str = Field(description="合法的Python代码字符串")


@tool(args_schema=PythonCodeInput)
def python_inter(py_code):
    """
    执行Python代码并返回结果
    :param py_code: Python代码字符串
    :return: 执行结果
    """
    import matplotlib
    matplotlib.use('Agg')
    g = globals()
    try:
        return str(eval(py_code, g))
    except Exception as e:
        global_vars_before = set(g.keys())
        try:
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "代码已顺利执行"


# 提示词模板
prompt = """
你是一名经验丰富的智能数据分析助手，擅长帮助用户高效完成以下任务：

1. Python代码执行：使用python_inter工具执行Python代码
2. 网络搜索：使用search_tool工具获取实时信息

所有回答均使用简体中文，清晰、礼貌、简洁。
"""

# 创建工具列表
tools = [search_tool, python_inter]

# 创建模型
model = ChatOpenAI(model="Qwen3-Coder-30B-A3B-Instruct", temperature=0)

# 创建图（Agent）
react_demo_graph = create_react_agent(model=model, tools=tools, prompt=prompt)
