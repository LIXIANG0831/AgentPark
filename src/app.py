import os
import sys

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from langsmith import Client
from graphs.react_demo import react_demo_graph

# 初始化LangSmith客户端
client = Client()

app_graph = react_demo_graph
