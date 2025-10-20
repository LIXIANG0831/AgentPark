from typing import TypedDict, Annotated, List

from langgraph.graph import add_messages


class ResearchAgentState(TypedDict):
    # 消息历史
    messages: Annotated[List, add_messages]
    # 研究主题
    research_topic: str
    # 搜索结果的原始内容
    search_results: List[str]
    # 分析后的关键点
    key_points: List[str]
    # 用户反馈
    user_feedback: str
