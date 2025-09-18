# fraud_research_agent/agent/orchestrator.py

import os
import json
from typing import List, Dict, Tuple

# 引入子 agent
from fraud_research_agent.agent.paper_search_agent import paper_search_agent
from fraud_research_agent.agent.paper_classification_agent import paper_classification_agent
from fraud_research_agent.agent.paper_report_agent import paper_report_agent


def orchestrator(user_topic: str) -> Dict:
    """
    反欺诈领域论文搜索与研究报告生成 Orchestrator

    执行流程：
    1. 根据用户研究主题搜索论文
    2. 提取分类信息并清洗
    3. 生成最终研究报告

    Args:
        user_topic (str): 用户研究主题，例如 "fraud detection behavior sequence"

    Returns:
        Dict: 包含 field_mapping, clean_papers, report 三部分的结果
    """

    print(f"\n🚀 开始执行 orchestrator，研究主题: {user_topic}")

    # Step 1: 论文搜索
    papers = paper_search_agent(user_topic)
    print(f"✅ 获取论文 {len(papers)} 篇")

    # Step 2: 论文分类与清洗
    field_mapping, clean_papers = paper_classification_agent(user_topic, papers)
    print(f"✅ 分类后论文 {len(clean_papers)} 篇")

    # Step 3: 研究报告生成
    report = paper_report_agent(user_topic, clean_papers)
    print("✅ 已生成研究报告")

    # 聚合结果
    result = {
        "field_mapping": field_mapping,
        "clean_papers": clean_papers,
        "report": report
    }

    # 保存 orchestrator 输出结果
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(current_dir, '..', 'data', 'report', 'report.md')
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n📂 Orchestrator 执行完成，结果已保存至 {save_path}")
    return result


# ===========================
# 示例调用
# ===========================
if __name__ == "__main__":
    query = "fraud detection behavior sequence"
    output = orchestrator(query)
    print("\n--- 最终报告输出 ---")
    print(output["report"])
