from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
from ollama import chat
import re
import logging
import time
logging.basicConfig(level=logging.INFO)

async def main(query:str):
    sse_url = "http://localhost:8000/sse"

    # 1) Open SSE → yields (in_stream, out_stream)
    async with sse_client(url=sse_url) as (in_stream, out_stream):
        # 2) Create an MCP session over those streams
        async with ClientSession(in_stream, out_stream) as session:
            # 3) Initialize
            info = await session.initialize()
            logging.info(f"Connected to {info.serverInfo.name} v{info.serverInfo.version}")

            # 4) List tools
            tools = (await session.list_tools())
            logging.debug(tools)

            # 5) Call a tool
            # Here we call the tool 'fetch_news_from_indian_express'
            result = await session.call_tool('fetch_news_from_indian_express', arguments={})
            logging.debug("Tool result:", result)
            response = chat(model='qwen3:8b', messages=[{"role": "user", "content": result.content[0].text}])
            data = response['message']['content']
            # Remove all content between <think> and </think>
            actual_response = re.sub(r'<think>.*?</think>', '', data, flags=re.DOTALL)
            # Write results to a markdown file
            timestamp = int(time.time())
            with open(f"positve_new{timestamp}.md", "w", encoding="utf-8") as f:
                f.write(actual_response)

            result = await session.call_tool('fetch_news_from_hindu', arguments={})
            logging.debug("Tool result:", result)
            response = chat(model='qwen3:8b', messages=[{"role": "user", "content": result.content[0].text}])
            data = response['message']['content']
            # Remove all content between <think> and </think>
            actual_response = re.sub(r'<think>.*?</think>', '', data, flags=re.DOTALL)
            
            # Append results to the same markdown file
            with open(f"positve_new{timestamp}.md", "a", encoding="utf-8") as f:
                f.write(actual_response)

            logging.info(f"Positive and neutral news saved to positve_new{timestamp}.md.")            


if __name__ == "__main__":
     asyncio.run(main("get good news from Indian Express"))