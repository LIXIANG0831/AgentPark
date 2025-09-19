from langchain_tavily import TavilySearch

# 创建Tavily搜索工具
web_search = TavilySearch(max_results=5, topic="general")