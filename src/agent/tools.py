from langchain_community.tools.tavily_search import TavilySearchResults

# For this example, we will use a built-in search tool via Tavily.
# Ensure TAVILY_API_KEY is set in your environment variables.
tools = [TavilySearchResults(max_results=3)]