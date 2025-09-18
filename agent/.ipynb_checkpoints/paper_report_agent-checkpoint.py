# fraud_research_agent/agent/paper_report_agent.py
from typing import List, Dict
from langchain.agents import create_tool_calling_agent
from fraud_research_agent.tools.count_tool import count_distribution_tool
from fraud_research_agent.tools.plot_tool import plot_histogram_tool
from fraud_research_agent.tools.report_tool import table_tool, filter_nonempty_tool
from fraud_research_agent.utils.llm_utils import get_llm
from fraud_research_agent.prompts.report_prompt import report_prompt_template


def paper_report_agent(query, paper_list) -> List[Dict]:
    llm = get_llm()
    tools = [count_distribution_tool, plot_histogram_tool, table_tool, filter_nonempty_tool]

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=report_prompt_template
    )

    response = agent.invoke(
        {
            "query": query,
            "papers": paper_list
       })

    


