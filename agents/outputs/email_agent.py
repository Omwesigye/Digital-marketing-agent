from agentscope.agents import ReActAgent
from config.prompts import EMAIL_AGENT_PROMPT

def build_email_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Customer Engagement & Retention Email Agent using AgentScope.
    """
    agent = ReActAgent(
        name="email_agent",
        model_config_name=model_config_name,
        sys_prompt=EMAIL_AGENT_PROMPT
    )
    return agent
