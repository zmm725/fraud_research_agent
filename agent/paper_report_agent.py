# fraud_research_agent/agent/paper_report_agent.py
import os
import json
from langchain.agents import create_tool_calling_agent
from fraud_research_agent.tools.count_tool import count_distribution_tool
from fraud_research_agent.tools.plot_tool import plot_histogram_tool
from fraud_research_agent.tools.report_tool import table_tool, filter_nonempty_tool
from fraud_research_agent.utils.llm_utils import get_llm
from fraud_research_agent.prompts.report_prompt import report_prompt_template
from langchain.agents import AgentExecutor
from fraud_research_agent.utils.global_state import set_global_papers


def sanitize_papers(paper_list):
    safe = []
    for p in paper_list:
        clean_p = {}
        for k, v in p.items():
            if isinstance(v, str):
                clean_p[k] = v.replace("\n", " ").replace("\r", " ")
            else:
                clean_p[k] = v
        safe.append(clean_p)
    return safe

def minimal_papers(paper_list):
    keys = ["published", "data_source_type_clean","fraud_type_clean","technical_approach_category_clean","github_repo"]
    return [{k: v for k, v in p.items() if k in keys} for p in paper_list]


def set_global_papers(papers):
    """设置全局论文数据"""
    global global_papers
    global_papers = papers


def paper_report_agent(query, paper_list):
    paper_list = minimal_papers(paper_list)
    set_global_papers(paper_list)

    llm = get_llm()
    tools = [count_distribution_tool, plot_histogram_tool, table_tool, filter_nonempty_tool]

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=report_prompt_template
    )

    # 创建 AgentExecutor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 使用 AgentExecutor 来运行
    response = agent_executor.invoke({
        "query": query
        # "intermediate_steps": []
    })
    
    return response

    # response = agent.invoke({
    #     "input": f"生成关于'{query}'的研究报告",  # 添加一个input字段
    #     "query": query,
    #     # "papers": sanitize_papers(paper_list),  # ✅ 预处理
    #     "intermediate_steps": []  # 添加这个必需的字段
    # })
    
    # return response