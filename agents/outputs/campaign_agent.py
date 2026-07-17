from agentscope.agents import ReActAgent
from config.prompts import CAMPAIGN_AGENT_PROMPT

def build_campaign_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Marketing Campaign Workflow Orchestrator Agent using AgentScope.
    """
    agent = ReActAgent(
        name="campaign_agent",
        model_config_name=model_config_name,
        sys_prompt=CAMPAIGN_AGENT_PROMPT
    )
    return agent
