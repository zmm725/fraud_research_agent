import os
import json
from typing import Dict, List
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from fraud_research_agent.prompts import (
    query_prompt,
    classify_prompt,
    auto_clustering_prompt,
    report_prompt,
)


# 加载环境变量（读取 .env 文件中的 DEEPSEEK_API_KEY）
load_dotenv(override=True)

def get_llm(model_name: str = "deepseek-chat", model_provider: str = "deepseek") -> BaseChatModel:
    """
    初始化一个 LLM（这里默认是 DeepSeek）。
    
    Args:
        model_name: 模型名称，例如 "deepseek-chat"
        model_provider: 模型提供商，例如 "deepseek"
    Returns:
        已初始化的 LangChain ChatModel
    """
    return init_chat_model(model=model_name, model_provider=model_provider)

llm = get_llm()

# def run_generate_queries_chain(user_topic: str) -> List[str]:
#     """
#     根据用户提供的研究子领域主题，生成覆盖该主题的 arXiv 查询列表。
#     使用 LLM | Prompt 风格调用。
    
#     Args:
#         user_topic: 用户输入的研究子领域
    
#     Returns:
#         查询列表（List[str]）
#     """

#     class QueriesListParser(BaseOutputParser):
#         def parse(self, text: str) -> list[str]:
#             try:
#                 # 移除可能的 Markdown 包裹
#                 if text.startswith("```") and text.endswith("```"):
#                     text = "\n".join(text.split("\n")[1:-1])
#                 data = json.loads(text)
#                 queries = data.get("queries", [])
#                 if not isinstance(queries, list):
#                     raise ValueError(f"'queries' 不是列表: {queries}")
#                 return queries
#             except Exception as e:
#                 print("解析 queries 失败:", e)
#                 print("原始文本:", text)
#                 return []


#     chat_prompt = ChatPromptTemplate.from_template(query_prompt.generate_search_query.content)
        
#     # 构建链式调用
#     parser = QueriesListParser()
#     querry_chain = chat_prompt | llm | parser

#     queries = querry_chain.invoke({"topic": user_topic})
#     return queries


# def run_classification_chain(query, paper: Dict) -> Dict:
#     """
#     对单篇论文进行分类，提取结构化信息。
    
#     Args:
#         paper: 包含 "title" 和 "abstract" 等论文信息
#     Returns:
#         分类结果的字典（JSON）
#     """
#     paper = json.dumps(paper, ensure_ascii=False, indent=2)
    
#     # 判断找到的文章是否与用户查询语义相关，过滤不相关文章
#     papers_str = json.dumps(paper, ensure_ascii=False, indent=2)
#     print(paper['title'])
#     prompt = "判断这篇论文是否与用户查询 '{query}' 相关: '{paper}'，相关输出为1，否则输出0".format(query=query, paper=papers_str)
#     match = llm.invoke(prompt)
#     if not match:
#         return {}


#     response_schemas = [
#         ResponseSchema(
#             name="data_source_type",
#             description="Data source category (industry or platform type of the data used, e.g., e-commerce, payment, banking). Infer if not explicitly mentioned. Output as a list."
#         ),
#         ResponseSchema(
#             name="data_source_name",
#             description="Specific data source name (e.g., Taobao, eBay, Binance). Output as a list."
#         ),
#         ResponseSchema(
#             name="fraud_type",
#             description="Specific fraud or risk scenario addressed (e.g., 'credit card fraud', 'fake account registration'). If non-fraud, specify the problem scenario. Output as a string."
#         ),
#         ResponseSchema(
#             name="technical_approach_category",
#             description="Broad technical categories used in the paper (e.g., feature engineering, RNN/LSTM, Transformer, GNN, anomaly detection, GAN, multimodal fusion, explainable AI). Include any other relevant approaches. Output as a list."
#         ),
#         ResponseSchema(
#             name="technical_approach_method",
#             description="Specific technical methods used (e.g., 'Bi-LSTM', 'Temporal Graph Network'). Output as a list."
#         ),
#         ResponseSchema(
#             name="technical_approach_description",
#             description="Core method description (objective summary from abstract, max 100 words). Output as a string."
#         ),
#         ResponseSchema(
#             name="innovation_points",
#             description="Explicit innovation points stated in abstract (max 100 words). Output as a string."
#         ),
#         ResponseSchema(
#             name="github_repo",
#             description="GitHub repository URL if explicitly mentioned, else leave empty. Output as a string."
#         ),
#     ]

#     # 构建 parser

#     parser = StructuredOutputParser.from_response_schemas(response_schemas)

#     prompt = PromptTemplate.from_template(
#         "请从以下文本中提取论文信息，并严格按照 JSON 输出：\n{paper}\n\n{format_instructions}"
#     )

#     classification_chain = (
#         prompt.partial(format_instructions=parser.get_format_instructions())
#         | llm
#         | parser
#     )
    
#     classification_result = classification_chain.invoke({'paper': paper})
#     return classification_result
