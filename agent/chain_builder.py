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


def normalize_match_output(match_str: str) -> int:
    """将模型输出转换为 0 或 1"""
    match_str = match_str.strip().lower()
    if match_str in ["1", "yes", "true"]:
        return 1
    elif match_str in ["0", "no", "false"]:
        return 0
    else:
        # 异常情况，默认不相关
        return 0

def run_generate_queries_chain(user_topic: str, llm) -> List[str]:
    """
    根据用户提供的研究子领域主题，生成覆盖该主题的 arXiv 查询列表。
    使用 LLM | Prompt 风格调用。
    
    Args:
        user_topic: 用户输入的研究子领域
    
    Returns:
        查询列表（List[str]）
    """

    class QueriesListParser(BaseOutputParser):
        def parse(self, text: str) -> list[str]:
            try:
                # 移除可能的 Markdown 包裹
                if text.startswith("```") and text.endswith("```"):
                    text = "\n".join(text.split("\n")[1:-1])
                data = json.loads(text)
                queries = data.get("queries", [])
                if not isinstance(queries, list):
                    raise ValueError(f"'queries' 不是列表: {queries}")
                return queries
            except Exception as e:
                print("解析 queries 失败:", e)
                print("原始文本:", text)
                return []


    chat_prompt = ChatPromptTemplate.from_template(query_prompt.generate_search_query.content)
        
    # 构建链式调用
    parser = QueriesListParser()
    querry_chain = chat_prompt | llm | parser

    queries = querry_chain.invoke({"topic": user_topic})
    return queries


def run_category_extraction_chain(query, llm, paper: Dict) -> Dict:
    """
    对单篇论文进行分类，提取结构化信息。
    
    Args:
        paper: 包含 "title" 和 "abstract" 等论文信息
    Returns:
        分类结果的字典（JSON）
    """
    
    # 判断找到的文章是否与用户查询语义相关，过滤不相关文章
    paper_str = json.dumps(paper, ensure_ascii=False, indent=2)
    prompt = '''
        判断这篇论文是否与用户查询 '{query}' 相关: '{paper}'，
        ⚠️ **只输出 0 或 1，且不要加任何解释、符号或空格**：
        - 如果相关，输出 1
        - 如果不相关，输出 0'''.format(query=query, paper=paper_str)
    match_str = llm.invoke(prompt).content
    match = normalize_match_output(match_str)

    print(paper['title'], match)
    if not match:
        return {}


    response_schemas = [
        ResponseSchema(
            name="data_source_type",
            description="Data source category (industry or platform type of the data used, e.g., e-commerce, payment, banking). Infer if not explicitly mentioned. Output as a list."
        ),
        ResponseSchema(
            name="data_source_name",
            description="Specific data source name (e.g., Taobao, eBay, Binance). Output as a list."
        ),
        ResponseSchema(
            name="fraud_type",
            description="Specific fraud or risk scenario addressed (e.g., 'credit card fraud', 'fake account registration'). If non-fraud, specify the problem scenario. Output as a string."
        ),
        ResponseSchema(
            name="technical_approach_category",
            description="Broad technical categories used in the paper (e.g., feature engineering, RNN/LSTM, Transformer, GNN, anomaly detection, GAN, multimodal fusion, explainable AI). Include any other relevant approaches. Output as a list."
        ),
        ResponseSchema(
            name="technical_approach_method",
            description="Specific technical methods used (e.g., 'Bi-LSTM', 'Temporal Graph Network'). Output as a list."
        ),
        ResponseSchema(
            name="technical_approach_description",
            description="Core method description (objective summary from abstract, max 100 words). Output as a string."
        ),
        ResponseSchema(
            name="innovation_points",
            description="Explicit innovation points stated in abstract (max 100 words). Output as a string."
        ),
        ResponseSchema(
            name="github_repo",
            description="GitHub repository URL if explicitly mentioned, else leave empty. Output as a string."
        ),
    ]

    # 构建 parser
    # parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # prompt = PromptTemplate.from_template(
    #     "请从以下文本中提取论文信息，并严格按照 JSON 输出：\n{paper}\n\n{format_instructions}"
    # )

    # classification_chain = (
    #     prompt.partial(format_instructions=parser.get_format_instructions())
    #     | llm
    #     | parser
    # )
    
    # classification_result = classification_chain.invoke({'paper': paper})
    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # prompt_template = PromptTemplate.from_template(
    #     "请从以下文本中提取论文信息，并严格按照 JSON 输出：\n{paper}\n\n{format_instructions}"
    # )
    prompt_text = classify_prompt.classification_prompt.template.format(paper=paper_str)
    resp = llm.invoke(prompt_text)

    # 兼容不同返回类型
    if hasattr(resp, "content"):  # DeepSeek ChatResult
        raw_output = resp.content
    elif hasattr(resp, "text"):   # 某些 LangChain Generation
        raw_output = resp.text
    else:  # 直接返回字符串
        raw_output = str(resp)

    # 去掉前后空格
    raw_output = raw_output.strip()
    
    # 如果返回 JSON 被 ```json 包裹，去掉 ```json ``` 前后标记
    if raw_output.startswith("```json"):
        raw_output = "\n".join(raw_output.split("\n")[1:-1])
    
    try:
        classification_result = parser.parse(raw_output)
    except Exception as e:
        print(f"[WARN] LLM 输出无法解析为 JSON, 返回空字典. 错误: {e}")
        classification_result = {}

    return classification_result

