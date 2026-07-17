# agents/processing/sentiment_agent.py

import json
import logging
from agentscope.agents import ReActAgent
from config.prompts import SENTIMENT_AGENT_PROMPT

logger = logging.getLogger(__name__)

def build_sentiment_agent(model_config_name: str = "gemini_config") -> ReActAgent:
    """
    Builds the Sentiment & Customer Needs Analyzer Agent using AgentScope.
    """
    agent = ReActAgent(
        name="sentiment_agent",
        model_config_name=model_config_name,
        toolkit=None,  # Pure analysis role; no external tools needed initially
        sys_prompt=SENTIMENT_AGENT_PROMPT
    )
    return agent


class SentimentAgentWrapper:
    """
    A processing wrapper around the AgentScope Sentiment Agent to safely
    execute NLP extraction and parse standard metrics for downstream consumers.
    """
    def __init__(self, model_config_name: str = "gemini_config"):
        self.agent = build_sentiment_agent(model_config_name)

    def analyze_text(self, text_content: str) -> dict:
        """
        Passes a single social post, review, or article headline to the agent 
        and extracts strict structured metrics regarding sentiment and customer needs.
        """
        logger.info("Executing Sentiment Agent text analysis...")
        
        # Format a clear execution message for the AgentScope instance
        task_msg = f"Analyze the following text content and return the structured JSON results:\n\n{text_content}"
        
        agent_response = self.agent(task_msg)
        raw_content = agent_response.content if hasattr(agent_response, 'content') else str(agent_response)

        try:
            # Enforce data shape and convert to native dictionary
            structured_json = json.loads(raw_content)
            return structured_json
        except json.JSONDecodeError:
            logger.error("SentimentAgent returned a non-JSON string. Falling back to default payload.")
            # Fallback schema to keep the pipeline moving without crashes
            return {
                "sentiment_label": "neutral",
                "sentiment_score": 0.0,
                "emotions": {"unknown": 1.0},
                "key_phrases": [],
                "customer_needs": [],
                "is_urgent": False
            }
