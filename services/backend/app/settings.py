import os
from typing import Dict

from llama_index.core.settings import Settings


def init_settings():
    model_provider = os.getenv("MODEL_PROVIDER")
    match model_provider:
        case "openai":
            init_openai()
        case "groq":
            init_groq()
        case "ollama":
            init_ollama()
        case "anthropic":
            init_anthropic()
        case "gemini":
            init_gemini()
        case "azure-openai":
            init_azure_openai()
        case "gigachat":
            init_gigachat()
        case "yandexgpt":
            init_yandexgpt()
        case _:
            raise ValueError(f"Invalid model provider: {model_provider}")
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))


def init_ollama():
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama.base import DEFAULT_REQUEST_TIMEOUT, Ollama

    base_url = os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434"
    request_timeout = float(
        os.getenv("OLLAMA_REQUEST_TIMEOUT", DEFAULT_REQUEST_TIMEOUT)
    )
    Settings.embed_model = OllamaEmbedding(
        base_url=base_url,
        model_name=os.getenv("EMBEDDING_MODEL"),
    )
    Settings.llm = Ollama(
        base_url=base_url, model=os.getenv("MODEL"), request_timeout=request_timeout
    )

def init_gigachat():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI
    
    class GigaChat(OpenAI):
        ...
    
    class GigaChatEmbedding(OpenAIEmbedding):
        ...

    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = GigaChat(**config)

    dimensions = os.getenv("EMBEDDING_DIM")
    config = {
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = GigaChatEmbedding(**config)


def init_yandexgpt():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI
    
    class YandexGPT(OpenAI):
        ...
    
    class YandexGPTEmbedding(OpenAIEmbedding):
        ...

    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = YandexGPT(**config)

    dimensions = os.getenv("EMBEDDING_DIM")
    config = {
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = YandexGPTEmbedding(**config)

def init_openai():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI

    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = OpenAI(**config)

    dimensions = os.getenv("EMBEDDING_DIM")
    config = {
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = OpenAIEmbedding(**config)


def init_azure_openai():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
    from llama_index.llms.azure_openai import AzureOpenAI

    llm_deployment = os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT")
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    max_tokens = os.getenv("LLM_MAX_TOKENS")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    llm_config = {
        "api_key": api_key,
        "deployment_name": llm_deployment,
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = AzureOpenAI(**llm_config)

    dimensions = os.getenv("EMBEDDING_DIM")
    embedding_config = {
        "api_key": api_key,
        "deployment_name": embedding_deployment,
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = AzureOpenAIEmbedding(**embedding_config)


def init_groq():
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.groq import Groq

    model_map: Dict[str, str] = {
        "llama3-8b": "llama3-8b-8192",
        "llama3-70b": "llama3-70b-8192",
        "mixtral-8x7b": "mixtral-8x7b-32768",
    }

    embed_model_map: Dict[str, str] = {
        "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
        "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
    }

    Settings.llm = Groq(model=model_map[os.getenv("MODEL")])
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embed_model_map[os.getenv("EMBEDDING_MODEL")]
    )


def init_anthropic():
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.anthropic import Anthropic

    model_map: Dict[str, str] = {
        "claude-3-opus": "claude-3-opus-20240229",
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        "claude-3-haiku": "claude-3-haiku-20240307",
        "claude-2.1": "claude-2.1",
        "claude-instant-1.2": "claude-instant-1.2",
    }

    embed_model_map: Dict[str, str] = {
        "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
        "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
    }

    Settings.llm = Anthropic(model=model_map[os.getenv("MODEL")])
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embed_model_map[os.getenv("EMBEDDING_MODEL")]
    )


def init_gemini():
    from llama_index.embeddings.gemini import GeminiEmbedding
    from llama_index.llms.gemini import Gemini

    model_name = f"models/{os.getenv('MODEL')}"
    embed_model_name = f"models/{os.getenv('EMBEDDING_MODEL')}"

    Settings.llm = Gemini(model=model_name)
    Settings.embed_model = GeminiEmbedding(model_name=embed_model_name)
