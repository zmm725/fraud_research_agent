from mcp.types import Prompt, PromptArgument

analysis_report_prompt = Prompt(
    name="fraud_research_analysis_report",
    description="Generate a structured anti-fraud academic research report in Chinese",
    args=[
        PromptArgument(name="query", type="str", description="The user’s research sub-domain query, e.g., 'behavior sequence in fraud detection'"),
        PromptArgument(name="papers", type="list", description="List of extracted paper metadata and classification results, including year, data_source_type, fraud_type, technical_approach_category, etc.")
    ],
    template="""
        You are an academic research analysis assistant.  
        Your task is to generate a structured **research report in Chinese** based on the provided research query and academic paper metadata.

        # Report Requirements
        - The report must be written in **Chinese**.  
        - The report must be divided into six clearly labeled sections.  
        - Each section should include **narrative analysis** based on the provided metadata and classification results.  
        - For statistical parts, first perform the aggregation (year, data_source_type, fraud_type, technical_approach_category), then summarize results into **tables or charts** (in text/table form if charts cannot be rendered).  
        - Writing style: academic, concise, analytical.  

        # Report Structure

        ## 第一部分：数据来源介绍  
        - Explain how search terms were constructed (based on the query: {query}).  
        - State on which platforms the papers were retrieved (e.g., arXiv).  
        - Describe the classification process (extracting structured fields like data_source_type, fraud_type, technical_approach_category).  

        ## 第二部分：时间分布  
        - Aggregate the number of papers by year using the `year` field in {papers}.  
        - Present results in a bar chart (or text-based bar visualization).  
        - Provide analysis of trends (e.g., growth, decline, recent peaks).  

        ## 第三部分：研究场景分布  
        - Merge `data_source_type` values from {papers} into broader categories (e.g., 金融服务, 电商, 区块链, 社交网络, 其他).  
        - Count papers in each category and present results in a table.  
        - Based on the table, write an analytical paragraph about “学术上关注的欺诈场景”.  

        ## 第四部分：欺诈类型分布  
        - Merge `fraud_type` values from {papers} into broader categories (e.g., 信用卡欺诈, 虚假账号, 洗钱, 交易欺诈, 其他).  
        - Count papers in each category and present results in a table.  
        - Based on the table, write an analytical paragraph about “学术上关注的欺诈类型”.  

        ## 第五部分：技术方案分布  
        - Merge `technical_approach_category` values from {papers} into broader categories (e.g., 特征工程与统计建模, 序列建模, 图神经网络, 异常检测, 联邦学习, 对抗生成网络, 多模态方法, 其他).  
        - Count papers in each category and present results in a table.  
        - Based on the table, write an analytical paragraph about “学术上使用的技术方案”.  

        ## 第六部分：总结  
        - Summarize key findings from the above sections.  
        - Highlight the most studied data sources, fraud types, and technical approaches.  
        - Provide an outlook for future academic trends in anti-fraud research.  

        # Output Format
        - The report must strictly follow the six-part structure.  
        - Use **Chinese** for all text, tables, and explanations.  
        - Do not include raw JSON or metadata in the report; only use them internally to generate analysis.
        """
)


report_prompt = PromptTemplate(
    input_variables=["query", "tables", "figures", "metadata"],
    template="""
        You are an academic research analysis assistant.  
        Your task is to generate a **structured research report in Chinese** about the topic: "{query}".  

        The input metadata is:
        {metadata}

        The pre-computed statistical results are provided as tables and figures:
        - Tables: {tables}
        - Figures: {figures}

        # Report Writing Rules
        - Write in **academic style**, clear and concise.  
        - The report must be divided into **six sections**:
        1. Data Sources  
        2. Temporal Distribution  
        3. Research Context Distribution  
        4. Fraud Type Distribution  
        5. Technical Approaches Distribution  
        6. Conclusion  

        - Where relevant, reference **tables and figures** naturally in the text, e.g.  
        "As shown in [TABLE_1], most papers are concentrated after 2020."  
        "Figure [FIGURE_1] illustrates the temporal growth trend."  

        - Use the exact placeholders `[TABLE_xxx]` and `[FIGURE_xxx]` where the items should be inserted.  

        - Each section should contain:
        - Analytical text  
        - At least one table or figure reference, if available for that dimension  

        # Output
        Write the **entire six-section report**.  
        Do not output raw JSON.  
        Only output the final report text with placeholders.
"""
)
