from agentscope.agents import ReActAgent
from config.prompts import INSIGHTS_AGENT_PROMPT

def build_insights_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Marketing Insights & Recommendation Agent using AgentScope.
    """
    agent = ReActAgent(
        name="insights_agent",
        model_config_name=model_config_name,
        sys_prompt=INSIGHTS_AGENT_PROMPT
    )
    return agent
