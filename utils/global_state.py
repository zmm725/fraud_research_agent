# fraud_research_agent/utils/global_state.py

# 全局变量存储论文数据
global_papers = []

def set_global_papers(papers):
    """设置全局论文数据"""
    global global_papers
    global_papers = papers

def get_global_papers():
    """获取全局论文数据"""
    return global_papers