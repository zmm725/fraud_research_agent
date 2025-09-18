from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel


def get_llm(model_name: str = "deepseek-chat", model_provider: str = "deepseek") -> BaseChatModel:
    """
    初始化一个 LLM（这里默认是 DeepSeek）。
    
    Args:
        model_name: 模型名称，例如 "deepseek-chat"
        model_provider: 模型提供商，例如 "deepseek"
    Returns:
        已初始化的 LangChain ChatModel
    """
    # 加载环境变量（读取 .env 文件中的 DEEPSEEK_API_KEY）
    load_dotenv(override=True)
    return init_chat_model(model=model_name, model_provider=model_provider)

