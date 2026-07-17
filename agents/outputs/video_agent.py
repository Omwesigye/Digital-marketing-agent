from agentscope.agents import ReActAgent
from config.prompts import VIDEO_AGENT_PROMPT

def build_video_agent(model_config_name: str = "gemini_config"):
    """
    Builds the Video Content & TikTok/Reels Script Agent using AgentScope.
    """
    agent = ReActAgent(
        name="video_agent",
        model_config_name=model_config_name,
        sys_prompt=VIDEO_AGENT_PROMPT
    )
    return agent
