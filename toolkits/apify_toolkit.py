from agentscope.tool import Toolkit
from tools.apify_tools import ApifyTools


class ApifyToolkit:

    def __init__(self):
        self.api = ApifyTools()

    def build(self):

        toolkit = Toolkit()

        #  CORE listening function (recommended first)
        toolkit.register_tool_function(
            self.api.collect_all_sources
        )

        # Optional granular control (better later)
        toolkit.register_tool_function(self.api.fetch_x_data)
        toolkit.register_tool_function(self.api.fetch_tiktok_data)
        toolkit.register_tool_function(self.api.fetch_instagram_hashtags)
        toolkit.register_tool_function(self.api.fetch_google_reviews)
        toolkit.register_tool_function(self.api.fetch_google_trends)
        toolkit.register_tool_function(self.api.fetch_local_news)
        toolkit.register_tool_function(self.api.fetch_weather)

        return toolkit