from agentscope.agents import ReActAgent
from config.prompts import FLIER_AGENT_PROMPT

def build_flier_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Graphic Design Concept & Flier Agent using AgentScope.
    """
    agent = ReActAgent(
        name="flier_agent",
        model_config_name=model_config_name,
        sys_prompt=FLIER_AGENT_PROMPT
    )
    return agent
