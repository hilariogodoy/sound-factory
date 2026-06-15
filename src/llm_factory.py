import os
import yaml
from langchain_core.language_models.chat_models import BaseChatModel


def get_llm(temperature: float = 0.5) -> BaseChatModel:
    with open("config/llm_config.yaml") as f:
        cfg = yaml.safe_load(f)
    provider = os.environ.get("LLM_PROVIDER", cfg["provider"])

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        pcfg = cfg["anthropic"]
        return ChatAnthropic(
            model=pcfg["model"],
            anthropic_api_key=os.environ[pcfg["api_key_env"]],
            temperature=temperature,
        )
    else:
        from langchain_openai import ChatOpenAI
        pcfg = cfg.get(provider, cfg["openai"])
        kwargs = dict(
            model=pcfg["model"],
            api_key=os.environ[pcfg["api_key_env"]],
            temperature=temperature,
        )
        if "base_url" in pcfg:
            kwargs["base_url"] = pcfg["base_url"]
        return ChatOpenAI(**kwargs)
