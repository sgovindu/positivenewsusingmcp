# Positive or neutral news filter
Wanted to build an AI Agent that filters out news articles that evoke negative sentiments. Tried building AI agents that get processed through LLM, however, there was no consistency of the results.

Came across **MCP** and gave it a try, results were positive!!

# MCP Server
_good_news_mcp.py_ implements two tools - _fetch_news_from_indian_express_ and _fetch_news_from_hindu_. These tools fetch latest news headlines from the two popular indian news sites. 
The tools use _BeautifulSoup_ to parse the results and generate content in the format href (link to the news article) and title text. This content is added to a prompt and returned for a LLM to process.

Prompt used to generate the information is:

```
"You are a helpful assistant that summarizes news articles. Here are some recent news articles:\n" + \
"\n".join([f"- {article['title']}: {article['href']}" for article in articles]) + \
"\nPlease return only articles that emote positive or neutral sentiments.\n" + \
"\nCategorize the articles as Positive, Neutral, or Negative based on their titles." +\
"\nProvide a consicse information of each article as to why its categorized as positive or neutral." +\
"\nReturn the href link for each article as Source" +\
"\nFormat the response in markdown with categories if applicable." +\
"\nIf no articles are positive or neutral, respond with 'No good news found today.'"
```

# MCP Client
_good_news_client.py_ establishes a sse session with _good_news_mcp.py_ and invokes the tools. Data returned from tool invocation is processed using Ollama with qwen3:8b. The model qwen returns the thought process as a part of the response, filtered out the thinking process output and stored the results to a markdown file with current timestamp.

# Execute
1. Install Ollama and qwen3:8b model
2. Start the mcp server - ```python good_news_mcp.py```
3. Execute the client - ```python good_news_client.py```

File name will be printed in the output.
