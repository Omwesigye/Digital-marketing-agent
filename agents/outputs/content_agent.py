from agentscope.agents import ReActAgent
from config.prompts import CONTENT_AGENT_PROMPT

def build_content_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Creative Content Generator & Copywriter Agent using AgentScope.
    """
    agent = ReActAgent(
        name="content_agent",
        model_config_name=model_config_name,
        sys_prompt=CONTENT_AGENT_PROMPT
    )
    return agent
