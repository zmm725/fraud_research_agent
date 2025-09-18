from typing import List, Dict, Optional, Union
import pandas as pd
from pydantic import BaseModel, Field
from langchain.tools import tool
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from fraud_research_agent.utils.global_state import get_global_papers

global_papers = get_global_papers()

class PDFReportInput(BaseModel):
    output_path: str = Field(..., description="Path to save the generated PDF file")
    report_text: str = Field(..., description="Report text with placeholders like [FIGURE_1], [TABLE_1]")
    figures: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping figure_id to image path, e.g., { 'FIGURE_1': 'time_dist.png' }"
    )
    tables: Dict[str, Union[dict, list]] = Field(
        default_factory=dict,
        description="Dictionary mapping table_id to tabular data, can be pandas.DataFrame.to_dict() or list[list]"
    )


@tool("generate_pdf_report_with_tables", args_schema=PDFReportInput, return_direct=True)
def generate_pdf_report_tool(
    output_path: str,
    report_text: str,
    figures: Dict[str, str],
    tables: Dict[str, Union[dict, list]]
) -> str:
    """
    Generate a PDF report with text, tables, and figures.
    Report text should contain placeholders like [FIGURE_1] and [TABLE_1].
    """

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # 按段落拆分
    paragraphs = report_text.split("\n")

    for para in paragraphs:
        para = para.strip()
        if not para:
            story.append(Spacer(1, 12))
            continue

        # 插入图表
        if para.startswith("[FIGURE_") and para.endswith("]"):
            fig_id = para.strip("[]")
            if fig_id in figures:
                img = Image(figures[fig_id], width=400, height=250)
                story.append(img)
                story.append(Spacer(1, 12))
            continue

        # 插入表格
        if para.startswith("[TABLE_") and para.endswith("]"):
            table_id = para.strip("[]")
            if table_id in tables:
                data = tables[table_id]

                # 支持 DataFrame.to_dict 格式
                if isinstance(data, dict) and "columns" in data and "data" in data:
                    df = pd.DataFrame(data["data"], columns=data["columns"])
                    data = [list(df.columns)] + df.values.tolist()
                elif isinstance(data, pd.DataFrame):
                    data = [list(data.columns)] + data.values.tolist()
                elif isinstance(data, list):
                    pass
                else:
                    raise ValueError(f"Unsupported table format for {table_id}")

                tbl = Table(data)
                tbl.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(tbl)
                story.append(Spacer(1, 12))
            continue

        # 普通段落
        story.append(Paragraph(para, styles["Normal"]))
        story.append(Spacer(1, 12))

    # 生成 PDF
    doc.build(story)
    return f"✅ PDF report generated at: {output_path}"


@tool
def table_tool(stats: Dict[str, int]) -> str:
    """
    将统计结果字典转为 Markdown 表格。
    
    Args:
        stats: {类别: 数量} 的字典

    Returns:
        Markdown 格式的表格字符串
    """
    if not stats:
        return "（无统计结果）"

    # 表头
    table = "| 类别 | 数量 |\n|------|------|\n"

    # 按数量排序（大到小）
    for key, value in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        table += f"| {key} | {value} |\n"

    return table


@tool
def filter_nonempty_tool(field: str) -> List[Dict]:
    """
    Filters a list of paper dictionaries, returning only those where the specified field is not empty.

    Args:
        papers: A list of dictionaries, each representing a paper.
        field: The name of the field to check for non-empty values.

    Returns:
        A filtered list of paper dictionaries.
    """
    filtered_papers = [paper for paper in global_papers if paper.get(field)]
    return filtered_papers
    