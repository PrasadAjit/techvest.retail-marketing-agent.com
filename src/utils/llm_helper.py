"""
LLM initialization helper
"""
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from ..config.settings import settings


def get_llm(temperature: float = None):
    """
    Get configured LLM instance (Azure or OpenAI)
    
    Args:
        temperature: Optional temperature override
    
    Returns:
        Configured LLM instance
    """
    temp = temperature if temperature is not None else settings.openai.temperature
    
    if settings.openai.use_azure:
        return AzureChatOpenAI(
            azure_deployment=settings.openai.azure_deployment,
            api_version=settings.openai.azure_api_version,
            azure_endpoint=settings.openai.azure_endpoint,
            api_key=settings.openai.azure_api_key,
            temperature=temp,
            max_retries=2,
            request_timeout=30,
            model_kwargs={
                "response_format": {"type": "text"}
            }
        )
    else:
        return ChatOpenAI(
            model=settings.openai.model,
            temperature=temp,
            openai_api_key=settings.openai.api_key
        )
