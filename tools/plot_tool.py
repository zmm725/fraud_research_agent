import os
from typing import Dict
import matplotlib.pyplot as plt
from io import BytesIO
from langchain.tools import tool

@tool
def plot_histogram_tool(
    stats: Dict[str, int], 
    title: str = "", 
    save_dir: str = ""
) -> BytesIO:
    """
    根据统计结果画直方图：
    1. 保存 PNG 文件到指定文件夹
    2. 返回 BytesIO（可直接插入 PDF）
    """
    # 创建文件夹
    os.makedirs(save_dir, exist_ok=True)

    # 文件名：优先用 title，否则用 "stats"
    file_name = f"{title if title else 'year_distribution'}.png"
    
    if not os.path.exists(save_dir):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(current_dir, '..', 'data', 'report')

    file_path = os.path.join(save_dir, file_name)

    # 画图
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(stats.keys(), stats.values())
    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel("Category")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存到文件夹
    plt.savefig(file_path, format="png")

    # 保存到 BytesIO（供 PDF 用）
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)

    return buffer
