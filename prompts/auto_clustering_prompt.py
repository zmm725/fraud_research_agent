from mcp.types import Prompt

auto_clustering_prompt = Prompt(
    name="auto_clustering",
    description="Automatically group raw values into broader categories and produce a stable mapping. Supports multi-value per article (2D array input).",
    arguments=[],
    content="""
      You are an expert in academic paper analysis.  
      You will be given a list of extracted raw values for the field "{field_name}".  
      The input can be either a **1D list** (one value per entry) or a **2D list** (each sublist corresponds to one article and contains multiple raw values).  
      Your task is to cluster all raw values into a small number of meaningful categories, assign clear labels to categories, and produce a mapping from each raw value to its assigned category.  

      # Instructions
      1. Carefully read all the values.  
      2. Group them into **no more than 8 categories**.  
      3. Assign a short and meaningful category label to each group.  
      4. Each raw value must map to exactly one category.  
      5. Output must be strict JSON, no explanations.  
      6. If values are unclear or too rare, map them to "Other".  

      # Few-shot Examples

      Example 1 (1D array)  
      Input values: ["credit card fraud", "stolen card", "account takeover", "fake account", "money laundering"]  

      Output JSON:
      {
        "categories": ["Credit Card Fraud", "Account Fraud", "Money Laundering"],
        "mapping": {
          "credit card fraud": "Credit Card Fraud",
          "stolen card": "Credit Card Fraud",
          "account takeover": "Account Fraud",
          "fake account": "Account Fraud",
          "money laundering": "Money Laundering"
        }
      }

      Example 2 (2D array)  
      Input values: [
        ["electronic commerce", "credit card"], 
        ["online social networks"], 
        ["Ethereum", "P2P lending platform"], 
        ["health insurance"], 
        ["Yelp", "Amazon"], 
        ["high-frequency trading", "financial transactions"]
      ]  

      Output JSON:
      {
        "categories": ["E-commerce", "Payment Systems", "Social Networks", "Blockchain", "P2P Finance", "Insurance", "Online Platforms", "Trading & Finance"],
        "mapping": {
          "electronic commerce": "E-commerce",
          "credit card": "Payment Systems",
          "online social networks": "Social Networks",
          "Ethereum": "Blockchain",
          "P2P lending platform": "P2P Finance",
          "health insurance": "Insurance",
          "Yelp": "Online Platforms",
          "Amazon": "E-commerce",
          "high-frequency trading": "Trading & Finance",
          "financial transactions": "Trading & Finance"
        }
      }

      # Now process the following values:

{list_of_values}
"""
)
