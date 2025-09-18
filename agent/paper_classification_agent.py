import os
import json
from fraud_research_agent.agent.chain_builder import run_category_extraction_chain
from fraud_research_agent.tools.categorization_tool import categorize_and_map_field
from fraud_research_agent.utils.llm_utils import get_llm


def paper_classification_agent(query, paper_list):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'processed')
    save_path = os.path.join(file_path, 'arxiv_results.json')
    
    llm = get_llm()
    paper_extract = []
    with open(save_path, "w", encoding="utf-8") as f:
        for paper in paper_list:
            paper_ = run_category_extraction_chain(query, llm, paper)
            if paper_:
                merged_data = {**paper, **paper_}
                paper_extract.append(merged_data)
                f.write(json.dumps(merged_data, ensure_ascii=False) + "\n")
                f.flush()  # 立刻写入磁盘，防止程序中途崩溃丢数据 
        
    paper_list = paper_extract
    print("去掉不相关论文后，还剩论文数量： ", len(paper_list))

    field_mapping = {}

    for field in ['data_source_type','fraud_type','technical_approach_category']:
        print(field)
        new_field = field+'_clean'
        category_result = categorize_and_map_field(paper_list, field, new_field, 20)
        field_mapping[field] = category_result['mapping']
        paper_list = category_result['data']
    
    clean_save_path = os.path.join(file_path, 'arxiv_results_clean.json')
    with open(clean_save_path, 'w', encoding='utf-8') as f:
        json.dump(paper_list, f, ensure_ascii=False, indent=4)
    
    return (field_mapping, paper_list)




