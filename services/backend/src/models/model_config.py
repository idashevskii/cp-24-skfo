from typing import Any, Self
from pydantic import Field, BaseModel, computed_field
from pydantic_settings import BaseSettings
from src.models.base_env import BaseEnvConfig


class OpenAIConfig(BaseModel):
    openai_api_key: str | None = Field(
        default=None,
        description="The OpenAI API key to use",
        env="OPENAI_API_KEY",
    )


class GeminiConfig(BaseModel):
    google_api_key: str | None = Field(
        default=None,
        description="The Google API key to use",
        env="GOOGLE_API_KEY",
    )


class GroqConfig(BaseModel):
    groq_api_key: str | None = Field(
        default=None,
        description="The Groq API key to use",
        env="GROQ_API_KEY",
    )


class OllamaConfig(BaseModel):
    ollama_base_url: str | None = Field(
        default=None,
        description="The base URL for the Ollama API",
        env="OLLAMA_BASE_URL",
    )
    ollama_request_timeout: float | None = Field(
        default=120.0,
        description="The request timeout for the Ollama API in seconds",
        env="OLLAMA_REQUEST_TIMEOUT",
    )


class AzureOpenAIConfig(BaseModel):
    azure_openai_endpoint: str | None = Field(
        default=None,
        description="The Azure OpenAI endpoint to use",
        env="AZURE_OPENAI_ENDPOINT",
    )
    azure_openai_api_key: str | None = Field(
        default=None,
        description="The Azure OpenAI API key to use",
        env="AZURE_OPENAI_API_KEY",
    )
    openai_api_version: str | None = Field(
        default="2024-02-01",
        description="The Azure OpenAI API version to use",
        env="OPENAI_API_VERSION",
    )
    azure_openai_llm_deployment: str | None = Field(
        default=None,
        description="The Azure OpenAI LLM deployment to use",
        env="AZURE_OPENAI_LLM_DEPLOYMENT",
    )
    azure_openai_embedding_deployment: str | None = Field(
        default=None,
        description="The Azure OpenAI embedding deployment to use",
        env="AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
    )

class YandexGPTConfig(BaseModel):
    yandexgpt_folder_id: str | None = Field(
        default=None,
        description="YandexGPT Folder ID to use",
        env="YANDEXGPT_FOLDER_ID",
    )
    yandexgpt_iam_token: str | None = Field(
        default=None,
        description="YandexGPT IAM Token to use",
        env="YANDEXGPT_IAM_TOKEN",
    )

class GigaChatConfig(BaseModel):
    gigachat_client_id: str | None = Field(
        default=None,
        description="GigaChat Client ID to use",
        env="GIGACHAT_CLIENT_ID",
    )
    gigachat_client_secret: str | None = Field(
        default=None,
        description="GigaChat Client Secret to use",
        env="GIGACHAT_CLIENT_SECRET",
    )


# We're using inheritance to flatten all the fields into a single class
# Todo: Refactor API to nested structure
class ModelConfig(
    BaseEnvConfig,
    OpenAIConfig,
    GroqConfig,
    GeminiConfig,
    OllamaConfig,
    AzureOpenAIConfig,
    YandexGPTConfig,
    GigaChatConfig,
):
    model_provider: str | None = Field(
        default=None,
        description="The name of AI provider.",
        env="MODEL_PROVIDER",
    )
    model: str | None = Field(
        default=None,
        description="The model to use for the LLM.",
        env="MODEL",
    )
    embedding_model: str | None = Field(
        default=None,
        description="The embedding model to use for the LLM.",
        env="EMBEDDING_MODEL",
    )

    class Config:
        extra = "ignore"
        protected_namespaces = ("settings_",)

    def model_post_init(self, __context: dict[str, any]) -> None:
        # llama_index will be conflicted if the AZURE_OPENAI_API_KEY and OPENAI_API_KEY are used together.
        # so we must clean OPENAI_API_KEY if the model_provider is azure-openai
        # Todo: Refactor API to nested structure, clean the unused fields in the respective classes
        if self.model_provider == "azure-openai":
            self.openai_api_key = None

    @computed_field
    @property
    def configured(self) -> bool:
        if self.model_provider == "openai":
            return self.openai_api_key is not None
        elif self.model_provider == "gemini":
            return self.google_api_key is not None
        elif self.model_provider == "ollama":
            return True
        elif self.model_provider == "azure-openai":
            return True
        elif self.model_provider == "groq":
            return self.groq_api_key is not None
        elif self.model_provider == "yandexgpt":
            return self.yandexgpt_iam_token is not None
        elif self.model_provider == "gigachat":
            return self.gigachat_client_secret is not None
        return False

    @classmethod
    def get_config(cls) -> Self:
        return ModelConfig()
