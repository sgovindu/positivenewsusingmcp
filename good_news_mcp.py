from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import requests

mcp = FastMCP("Good News Server")

@mcp.tool()
#def fetch_news_from_indian_express() -> list[dict]:
def fetch_news_from_indian_express() -> str:
    '''Fetches news articles from Indian Express and returns a list of dictionaries with title and href.'''   
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get('https://indianexpress.com/latest-news/', headers=headers)  
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('div', class_='articles')
    news_items = []
    for element in elements:
        # Get all <a> tags inside the element
        links = element.find_all('a', href=True)
        for link in links:
            href = link['href']
            title = link.get_text(strip=True)
            news_item = {
                'title': title,
                'href': href
            }
            news_items.append(news_item)     
    #return news_items
    return get_good_news(news_items)

@mcp.tool()
def fetch_news_from_hindu() -> str:
    '''Fetches news articles from The Hindu and returns a list of dictionaries with title and href.'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get('https://www.thehindu.com/latest-news/', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('div', class_='right-content')
    news_items = []
    for element in elements:
        # Get all <a> tags inside the element
        links = element.find_all('a', href=True)
        for link in links:
            href = link['href']
            title = link.get_text(strip=True)
            news_item = {
                'title': title,
                'href': href
            }
            news_items.append(news_item)
    return get_good_news(news_items)

@mcp.prompt()
def get_good_news(articles: list[dict]) -> str:
    return "You are a helpful assistant that summarizes news articles. Here are some recent news articles:\n" + \
           "\n".join([f"- {article['title']}: {article['href']}" for article in articles]) + \
           "\nPlease return only articles that emote positive or neutral sentiments.\n" + \
           "\nCategorize the articles as Positive, Neutral, or Negative based on their titles." +\
           "\nProvide a consicse information of each article as to why its categorized as positive or neutral." +\
           "\nReturn the href link for each article as Source" +\
           "\nFormat the response in markdown with categories if applicable." +\
           "\nIf no articles are positive or neutral, respond with 'No good news found today.'"
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')
