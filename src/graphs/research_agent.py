from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

from src.nodes.research_agent import research_node, analysis_node, report_generation_node, feedback_node, revision_node
from src.state.research_agent import ResearchAgentState


def should_continue(state: ResearchAgentState):
    """决定是否继续循环基于用户反馈"""
    last_message = state["messages"][-1]

    # 检查用户是否满意
    if isinstance(last_message, HumanMessage):
        content = last_message.content.lower()
        if "满意" in content or "yes" in content or "good" in content or "可以" in content:
            return END

    # 默认继续修订
    return "revise"


# 创建图
builder = StateGraph(ResearchAgentState)

# 添加节点
builder.add_node("research", research_node)
builder.add_node("analyze", analysis_node)
builder.add_node("generate_report", report_generation_node)
builder.add_node("get_feedback", feedback_node)
builder.add_node("revise", revision_node)

# 设置入口点
builder.set_entry_point("research")

# 添加边
builder.add_edge("research", "analyze")
builder.add_edge("analyze", "generate_report")
builder.add_edge("generate_report", "get_feedback")

# 添加条件边
builder.add_conditional_edges("get_feedback", should_continue, {
    "revise": "revise",
    END: END
})
builder.add_edge("revise", "get_feedback")

# 编译图
research_agent_graph = builder.compile()