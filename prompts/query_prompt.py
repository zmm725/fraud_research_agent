from mcp.types import Prompt, PromptArgument
from mcp.types import Prompt

generate_search_query = Prompt(
    name="generate_search_query",
    description="Generate arXiv search queries for a given research subfield in fraud detection, splitting complex queries into simpler ones if necessary.",
    arguments=[
        PromptArgument(name="topic", description="Research subfield in fraud detection", required=True),
    ],
    content="""
    You are an expert in academic literature search.  
    Your task is to generate search queries for arXiv to cover the given research subfield in fraud detection.  

    # Instructions
    1. The input is a research topic: "{topic}".  
    2. Generate queries that cover as many relevant subtopics as possible.  
    3. arXiv cannot handle very complex queries (e.g., with parentheses, nested AND/OR logic).  
    4. If a query would be too complex, split it into multiple simpler queries.  
    5. Output must be **strict JSON** with the following format:

    Example 1:
    Input topic: "credit card fraud detection"  
    Output JSON:
    {{
      "queries": [
        "credit card fraud detection",
        "credit card fraud prevention",
        "credit card fraud patterns"
      ]
    }}

    # Now generate queries for the following topic:
    "{topic}"
"""
)
