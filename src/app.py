import os
import sys
from dotenv import load_dotenv
from langsmith import Client

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# ReAct Agent Demo
from graphs.react_demo import react_demo_graph
# 研究智能体
from graphs.research_agent import research_agent_graph

# 加载环境变量
load_dotenv(override=True)

# 初始化LangSmith客户端
client = Client()

app_graph = research_agent_graph
