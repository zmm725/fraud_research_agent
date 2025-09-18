from fraud_research_agent.agent.chain_builder import run_category_extraction_chain
from fraud_research_agent.tools.categorization_tool import categorize_and_map_field

def paper_classification_agent(query, paper_list):
    paper_extract = []
    for paper in paper_list:
        paper_ = run_category_extraction_chain(query, paper)
        paper_extract.append(paper_)

    field_mapping = {}

    for field in ['data_source_type','fraud_type','technical_approach_category']:
        new_field = field+'_clean'
        category_result = categorize_and_map_field(paper_list, field, new_field, 20)
        field_mapping[field] = category_result['mapping']
        paper_list = category_result['data']
    
    return (field_mapping, paper_list)

    