from utils.llm_utils import *
from utils.io_utils import *

def main():
    # print("Hello from fraud-research-agent!")
    query = "行为序列在反欺诈领域的研究"
    # query_key_words = run_generate_queries_chain()
    # search_arxiv(query_key_words)
    process_papers_with_classification(query)



if __name__ == "__main__":
    main()
