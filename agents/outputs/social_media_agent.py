from agentscope.agents import ReActAgent
from config.prompts import SOCIAL_MEDIA_AGENT_PROMPT

def build_social_media_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Social Media Publishing Coordinator Agent using AgentScope.
    """
    agent = ReActAgent(
        name="social_media_agent",
        model_config_name=model_config_name,
        sys_prompt=SOCIAL_MEDIA_AGENT_PROMPT
    )
    return agent
