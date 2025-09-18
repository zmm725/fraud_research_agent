# from typing import List, Dict, Optional
# from datetime import datetime
# from collections import Counter
# from langchain.tools import tool


# class DistributionCounter:
#     def __init__(self, data: List[Dict]):
#         self.data = data

#     def count_distribution(self, field: str, strategy: Optional[str] = None) -> Dict[str, int]:
#         """核心统计逻辑"""
#         values = []
#         raw_values = [record.get(field) for record in self.data if record.get(field) is not None]

#         # Auto 模式
#         if strategy is None or strategy == "auto":
#             if all(self._is_date(v) for v in raw_values):
#                 strategy = "year"
#             elif any(isinstance(v, list) for v in raw_values):
#                 strategy = "list"
#             elif all(isinstance(v, str) for v in raw_values):
#                 strategy = "string"
#             else:
#                 raise ValueError(f"无法自动推断 {field} 的统计方式")

#         # 根据 strategy 处理
#         if strategy == "year":
#             for v in raw_values:
#                 dt = self._to_datetime(v)
#                 if dt:
#                     values.append(str(dt.year))

#         elif strategy == "string":
#             values = [v for v in raw_values if isinstance(v, str)]

#         elif strategy == "list":
#             for v in raw_values:
#                 if isinstance(v, list):
#                     values.extend(v)
#                 else:
#                     values.append(v)

#         else:
#             raise ValueError(f"未知 strategy: {strategy}")

#         return dict(Counter(values))

#     def _is_date(self, v) -> bool:
#         if isinstance(v, datetime):
#             return True
#         if isinstance(v, str):
#             try:
#                 datetime.fromisoformat(v)
#                 return True
#             except ValueError:
#                 return False
#         return False

#     def _to_datetime(self, v) -> Optional[datetime]:
#         if isinstance(v, datetime):
#             return v
#         if isinstance(v, str):
#             try:
#                 return datetime.fromisoformat(v)
#             except ValueError:
#                 return None
#         return None


# # === LangChain Tool 封装 ===
# @tool
# def count_distribution_tool(field_type: str, paper_list: List[Dict], strategy: Optional[str] = "auto") -> Dict[str, int]:
#     """
#     统计某个字段的分布情况。
#     参数:
#     - field_type: 需要统计的字段名 (如 published_date, fraud_type, technical_approach_category, data_source_type)
#     - paper_list: 输入的论文数据列表
#     - strategy: 统计策略 (auto/year/string/list)
#     返回:
#     - dict: {值: 计数}
#     """
#     counter = DistributionCounter(paper_list)
#     return counter.count_distribution(field_type, strategy)


# # === 示例调用 ===
# # if __name__ == "__main__":
# #     papers = [
# #         {
# #             "published_date": "2023-05-01",
# #             "fraud_type": "信用卡欺诈",
# #             "technical_approach_category": ["ML", "DL"],
# #             "data_source_type": ["银行", "社交网络"]
# #         },
# #         {
# #             "published_date": "2024-06-01",
# #             "fraud_type": "洗钱",
# #             "technical_approach_category": ["规则"],
# #             "data_source_type": ["交易日志"]
# #         },
# #         {
# #             "published_date": "2023-07-15",
# #             "fraud_type": "信用卡欺诈",
# #             "technical_approach_category": ["ML"],
# #             "data_source_type": ["银行"]
# #         }
# #     ]

# #     print(count_distribution_tool("fraud_type", papers))  # -> {'信用卡欺诈': 2, '洗钱': 1}
# #     print(count_distribution_tool("published_date", papers))  # -> {2023: 2, 2024: 1}


from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter
from langchain.tools import tool
from pydantic import BaseModel, Field
from fraud_research_agent.utils.global_state import get_global_papers

# 全局变量，用于存储论文数据
# global_papers = []
global_papers = get_global_papers()

class DistributionCounter:
    def __init__(self):
        # 不再需要传入数据，使用全局变量
        pass

    def count_distribution(self, field: str, strategy: Optional[str] = None) -> Dict[str, int]:
        """核心统计逻辑"""
        values = []
        # 使用全局变量 global_papers
        raw_values = [record.get(field) for record in global_papers if record.get(field) is not None]

        # Auto 模式
        if strategy is None or strategy == "auto":
            if all(self._is_date(v) for v in raw_values):
                strategy = "year"
            elif any(isinstance(v, list) for v in raw_values):
                strategy = "list"
            elif all(isinstance(v, str) for v in raw_values):
                strategy = "string"
            else:
                raise ValueError(f"无法自动推断 {field} 的统计方式")

        # 根据 strategy 处理
        if strategy == "year":
            for v in raw_values:
                dt = self._to_datetime(v)
                if dt:
                    values.append(str(dt.year))

        elif strategy == "string":
            values = [v for v in raw_values if isinstance(v, str)]

        elif strategy == "list":
            for v in raw_values:
                if isinstance(v, list):
                    values.extend(v)
                else:
                    values.append(v)

        else:
            raise ValueError(f"未知 strategy: {strategy}")

        return dict(Counter(values))

    def _is_date(self, v) -> bool:
        if isinstance(v, datetime):
            return True
        if isinstance(v, str):
            try:
                datetime.fromisoformat(v)
                return True
            except ValueError:
                return False
        return False

    def _to_datetime(self, v) -> Optional[datetime]:
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                return None
        return None


# === LangChain Tool 输入 schema ===
class CountDistributionInput(BaseModel):
    field_type: str = Field(..., description="需要统计的字段名 (如 published, fraud_type_clean, technical_approach_category_clean, data_source_type_clean)")
    strategy: Optional[str] = Field("auto", description="统计策略 (auto/year/string/list)")


# === LangChain Tool 封装 ===
@tool(args_schema=CountDistributionInput)
def count_distribution_tool(field_type: str, strategy: Optional[str] = "auto") -> Dict[str, int]:
    """
    统计某个字段的分布情况。使用全局论文数据进行统计。
    """
    counter = DistributionCounter()
    return counter.count_distribution(field_type, strategy)
