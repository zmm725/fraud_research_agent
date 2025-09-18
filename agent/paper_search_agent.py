# fraud_research_agent/agent/paper_search_agent.py
import os
import json
from typing import List, Dict
from fraud_research_agent.agent.chain_builder import run_generate_queries_chain
from fraud_research_agent.tools.arxiv_tool import search_arxiv
from fraud_research_agent.utils.llm_utils import get_llm

def paper_search_agent(user_topic: str) -> List[Dict]:
    """
    高层封装的论文搜索 Agent：
    1. 根据用户主题生成 query 列表
    2. 用 arxiv 工具逐个抓取
    3. 聚合结果并去重
    
    Args:
        user_topic (str): 用户研究主题，比如 "fraud detection behavior sequence"
    
    Returns:
        List[Dict]: 抓取到的论文元数据
    """
    # Step 1: 生成查询列表
    llm = get_llm()
    queries = run_generate_queries_chain(user_topic, llm)
    print(f"🔍 生成 {len(queries)} 个查询: {queries}")

    # all_results = []

    # # Step 2: 逐个查询并抓取
    # for i, q in enumerate(queries):
    #     print(f"\n=== 执行检索 query: {q} ===")
    #     file_name = f"arxiv_results_{i}.json"
    #     results = search_arxiv(q, file_name)
    #     all_results.extend(results)
    
    file_name = 'arxiv_results_raw.json'
    all_results = search_arxiv(queries, file_name)
    # Step 3: 去重（基于论文 ID）
    seen = set()
    unique_results = []
    for paper in all_results:
        if paper["id"] not in seen:
            seen.add(paper["id"])
            unique_results.append(paper)
    

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'raw')
    save_path = os.path.join(file_path, 'arxiv_results.json')

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(unique_results, f, ensure_ascii=False, indent=2)

    print(f"\n📚 最终获取 {len(unique_results)} 篇论文（去重后）")
    return unique_results


# ===========================
# 示例调用
# ===========================

# if __name__ == "__main__":
#     papers = paper_search_agent("fraud detection behavior sequence")
#     print(f"\n示例输出：{papers[:2]}")  # 打印前两篇看看
