from mcp.types import Prompt, PromptArgument

classification_prompt = Prompt(
    name="academic_paper_classification",
    description="Structured information extraction from academic papers for anti-fraud research analysis",
    args=[
        PromptArgument(name="paper", type="str", description="Paper information"),
    ],
    template="""
        You are an academic paper information extraction expert. 
        Please strictly analyze the paper title and abstract, and output the following structured information in a **pure JSON object**, without any extra explanations or formatting.

        # Output JSON Structure
        {{
            "data_source_type": [],           # Data source category (industry or platform type of the data used, e.g., e-commerce, payment, banking; infer if not explicitly mentioned)
            "data_source_name": [],           # Specific data source name (e.g., Taobao, eBay, Binance)
            "fraud_type": "",                 # Specific fraud or risk scenario addressed (e.g., "credit card fraud", "fake account registration"); if non-fraud, specify the problem scenario
            "technical_approach_category": [],# Broad technical categories used in the paper (e.g., feature engineering, RNN/LSTM, Transformer, GNN, anomaly detection, GAN, multimodal fusion, explainable AI); include any other relevant approaches, not limited to examples
            "technical_approach_method": [],  # Specific technical methods used (use standard academic terms, e.g., "Bi-LSTM", "Temporal Graph Network")
            "technical_approach_description": "",  # Core method description (objective summary from abstract, max 100 words)
            "innovation_points": "",          # Explicit innovation points stated in abstract (max 100 words)
            "github_repo": ""                 # GitHub repository URL if explicitly mentioned, else leave empty
        }}

        # Extraction Guidelines
        1. Output must be **strict JSON only**, no extra text.
        2. Unmentioned fields should be filled with an empty string `""` or empty list `[]` as appropriate.
        3. Fraud type must be specific to the scenario level.
        4. Technical approach method and description should objectively summarize the abstract content.
        5. Innovation points should be directly based on statements in the abstract.
        6. GitHub repo should be included only if explicitly mentioned.
        7. Broad technical categories should be summarized freely; reference common techniques if helpful, but do not restrict to any predefined list.
        8. List fields (`[]`) can contain **multiple items**; include **all relevant elements mentioned in the text**.

        Please analyze the following paper:

        Paper: {paper}  
    """
)


