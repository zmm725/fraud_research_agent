from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

report_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """你是一个资深的反欺诈学术研究分析员。你的任务是根据用户给定的研究子领域（query）以及整理好的学术论文元数据（papers），生成一份结构化的中文研究报告。"""),
    ("human", """请根据以下信息生成报告：
        研究子领域: {query}
        论文元数据: 已经加载到工具上下文中，无需在提示中显示。
        
        报告必须严格分为以下七个部分：
        ## 第一部分：数据来源介绍
        介绍数据是怎么获取的：
        - 描述论文是如何通过 {query} 获取的
        - 按照：关键词生成 → arXiv 搜索 → 筛选相关论文 → 信息提取 → 分类统计 → 绘图 → 报告生成 的逻辑

        ## 第二部分：时间分布
        - 使用 `count_field` 工具统计 published 年份分布
        - 分析时间趋势后，根据趋势特点生成一个描述性标题（如"2018-2023年论文发表趋势"）
        - 使用 `plot_histogram` 绘制直方图，并将生成的标题作为参数传入
        - 对趋势进行分析（增长/下降/近期高峰）

        ## 第三部分：欺诈场景分布
        - 使用 `count_field` 工具统计 data_source_type_clean 字段
        - 使用 `make_table` 工具生成表格
        - 写一段分析学术界关注的欺诈场景

        ## 第四部分：欺诈类型分布
        - 使用 `count_field` 工具统计 fraud_type_clean 字段
        - 使用 `make_table` 工具生成表格
        - 写一段分析学术界关注的欺诈类型

        ## 第五部分：技术方案分布
        - 使用 `count_field` 工具统计 technical_approach_category_clean 字段
        - 使用 `make_table` 工具生成表格
        - 写一段分析学术界使用的技术方案
        - 对于一些新的前沿技术，展开写作

        ## 第六部分：开源 github 项目
        - 使用 `filter_nonempty` 工具过滤出 github_repo 字段非空的论文
        - 列举这些项目并简单介绍

        ## 第七部分：总结
        - 总结以上部分的主要发现
        - 强调学术界最常研究的数据源、欺诈类型和技术方法
        - 给出未来趋势展望

        ⚠️ 注意事项：
        1. 请严格使用 JSON 格式输出工具调用参数，所有字符串必须用双引号包裹，不能包含换行符或未转义字符。
        2. 报告必须严格按照七部分结构输出。
        3. 全文使用 **中文**。
        4. 不要输出原始 JSON 或元数据，仅使用工具处理后的结果。
        5. 所有统计结果必须配合解释性文字。
        6. 图表和表格不是用文字描述，而是必须将工具返回的 Markdown 代码块（如 `![标题](图片链接)` 或表格语法）直接插入到报告的相应位置。
        7. 确保输出是完整、格式优美的 Markdown 文档，这将用于直接转换为 PDF 报告。

        【工具使用说明】
        你必须严格使用以下工具来获取数据，不能凭空编造：
        - `count_distribution_tool`: 用于统计某个字段的分布情况。只需要传入字段名，例如：count_distribution_tool("published")
        - `filter_nonempty_tool`: 用于过滤出指定字段非空的论文。只需要传入字段名，例如：filter_nonempty_tool("github_repo")

        ⚠️ 注意：不要传递整个论文列表作为参数，只需要传递字段名！论文数据已经预先加载到工具上下文中。
    """)
    ,MessagesPlaceholder(variable_name="agent_scratchpad")
])