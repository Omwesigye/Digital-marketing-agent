from agentscope.agents import ReActAgent
from config.prompts import COMPETITOR_AGENT_PROMPT

def build_competitor_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Competitor Intelligence & Benchmarking Agent using AgentScope.
    """
    agent = ReActAgent(
        name="competitor_agent",
        model_config_name=model_config_name,
        sys_prompt=COMPETITOR_AGENT_PROMPT
    )
    return agent
