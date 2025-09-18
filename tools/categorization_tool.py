# tools/categorization_tool.py
import json
import traceback
from typing import List, Dict, Literal
from langchain.tools import tool
from fraud_research_agent.utils import llm_utils


llm = llm_utils.get_llm()


def categorize_and_map_field(
    data: List[Dict],
    field: str,
    new_field: str,
    max_categories: int = 20
) -> Dict[str, any]:
    """
    LLM 将字段分成不超过 max_categories 类别，并生成新字段
    输入:
        - data: JSON list
        - field: 原始字段
        - new_field: 新字段名
        - max_categories: 最大类别数
    输出:
        {
            "mapping": {原始值: 类别名},
            "data": 新字段已生成的数据列表
        }
    """
    # 1. 收集原始值（list 类型展开）
    raw_values = []
    for record in data:
        value = record.get(field)
        if value is None:
            continue
        if isinstance(value, list):
            raw_values.extend(value)
        else:
            raw_values.append(value)
    raw_values = list(set(raw_values))
    print(raw_values)

    # 2. LLM 生成类别映射
    prompt = f"""
        你是一名学术研究分析助手。
        请将以下 {field} 字段的取值，归纳为不超过 {max_categories} 个简洁类别：
        - 类别名称要简短清晰。
        - 前沿或重要技术应单独保留为独立类别，不要笼统归入“其他”。
        - 避免使用含糊、冗长的类别。

        输出要求：
        1. 结果必须是严格合法的 JSON 对象。
        2. 格式为：{{ "原始值": "类别" }} 的映射表。
        3. 不要输出解释说明或额外文字。

        字段取值列表：
        {raw_values}
    """
    response = llm.invoke(prompt)
    try:
        response_str = response.content if hasattr(response, "content") else str(response)
        # 去掉前后空格
        response_str = response_str.strip()
    
        # 如果返回 JSON 被 ```json 包裹，去掉 ```json ``` 前后标记
        if response_str.startswith("```json"):
            response_str = "\n".join(response_str.split("\n")[1:-1])

        mapping = json.loads(response_str)
    except Exception as e:
        print("[ERROR] JSON 解析失败:", e)
        print("[RAW RESPONSE]", response)  # 打印 LLM 原始输出
        traceback.print_exc()  # 打印完整堆栈，便于定位
        # fallback: 每个值单独成一类
        mapping = {v: v for v in raw_values}

    # 3. 生成新字段
    new_data = []
    # 直接在原始 data 上添加新字段
    for record in data:
        value = record.get(field)
        if value is None:
            record[new_field] = None
        elif isinstance(value, list):
            record[new_field] = [mapping.get(v, v) for v in value]
        else:
            record[new_field] = mapping.get(value, value)


    return {"mapping": mapping, "data": data}



