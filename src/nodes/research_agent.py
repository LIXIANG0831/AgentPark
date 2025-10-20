from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from src.tools.web_search import web_search as search_tool

from src.state.research_agent import ResearchAgentState

llm = ChatOpenAI(model="Qwen3-Coder-30B-A3B-Instruct", temperature=0)


def research_node(state: ResearchAgentState):
    """执行研究搜索"""
    topic_extract_prompt = f"""
        请从用户的输入中梳理出1条用于网络检索的词条。
        用户的输入如下：
        {state['messages'][-1]}

        用一条词条完整概括，不要啰嗦，直接输出词条。
    """

    response = llm.invoke(topic_extract_prompt)
    research_topic = response.content
    print(f"正在搜索: {research_topic}")

    # 使用搜索工具获取信息
    search_query = f"{research_topic} 最新发展"
    results = search_tool.invoke(search_query).get("results", [])

    # 提取搜索结果
    search_contents = []
    for result in results:
        search_contents.append(f"标题: {result['title']}\n内容: {result['content']}\n链接: {result['url']}")

    # 更新状态
    return {
        "research_topic": research_topic,
        "search_results": search_contents,
        "messages": state["messages"] + [
            AIMessage(content=f"已完成对'{research_topic}'的搜索，获得了{len(search_contents)}条结果。")]
    }


def analysis_node(state: ResearchAgentState):
    """分析搜索结果并提取关键信息"""
    print("正在分析搜索结果...")

    # 组合搜索内容
    search_content = "\n\n".join(state["search_results"])

    # 使用LLM分析结果
    analysis_prompt = f"""
    请分析以下关于"{state['research_topic']}"的搜索结果，提取关键信息和要点：

    {search_content}

    请提供5-7个最重要的关键点，每个点用一句话概括。
    """

    response = llm.invoke(analysis_prompt)
    key_points = response.content.split("\n")
    # 过滤空行
    key_points = [kp for kp in key_points if kp != ""]

    return {
        "key_points": key_points,
        "messages": state["messages"] + [AIMessage(content="已分析搜索结果并提取关键信息。")]
    }


def report_generation_node(state: ResearchAgentState):
    """生成研究报告"""
    print("正在生成研究报告...")

    # 基于关键点生成报告
    key_points_text = "\n".join([f"- {point}" for point in state["key_points"]])

    report_prompt = f"""
    基于以下关于"{state['research_topic']}"的关键点，生成一份简洁的研究报告：

    {key_points_text}

    报告应包括：
    1. 简要介绍
    2. 主要发现/关键点
    3. 结论或未来展望

    报告长度应在300-500字之间。
    """

    response = llm.invoke(report_prompt)
    report = response.content

    return {
        "messages": state["messages"] + [AIMessage(content=f"# 研究报告: {state['research_topic']}\n\n{report}")]
    }


def feedback_node(state: ResearchAgentState):
    """请求用户反馈"""
    print("请求用户反馈...")
    # 确保 state 包含所有必要的字段

    feedback_request = "您对这份研究报告满意吗？如果有需要修改或补充的地方，请提供反馈。如果您满意，请输入'满意'或'yes'。"

    return {
        "messages": state["messages"] + [AIMessage(content=feedback_request)]
    }


def revision_node(state: ResearchAgentState):
    """根据用户反馈修改报告"""

    # 获取用户最后一条消息作为反馈
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        feedback = last_message.content
    else:
        feedback = state.get("user_feedback", "")

    # 基于反馈修改报告
    revision_prompt = f"""
    根据以下用户反馈修改关于"{state['research_topic']}"的研究报告：

    用户反馈: {feedback}

    请生成修改后的报告，保持相同的格式和长度要求。
    """

    response = llm.invoke(revision_prompt)
    revised_report = response.content

    return {
        "messages": state["messages"][:-2] + [
            AIMessage(content=f"# 修订后的研究报告: {state['research_topic']}\n\n{revised_report}")],
        "user_feedback": feedback
    }
