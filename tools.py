from langchain.tools import tool
import requests

from bs4 import BeautifulSoup

from tavily import TavilyClient

import os
import sys
from dotenv import load_dotenv
load_dotenv()


tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str, depth: str = 'advanced'):

    try: 
    
        response = tavily.search(query = query, max_results = 5, search_depth=depth)
        out = []
        for r in response['results']:

            out.append(f"title: {r['title']}\n url: {r['url']}\n snippet: {r['content'][:400]}")
    
        res = "\n------\n".join(out)
        return res

    except Exception as e:
        raise(e, sys)
    

@tool
def scrape_url(url: str):

    try:
        resp = requests.get(url = url, timeout=8, headers = {"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", 'nav', 'footer']):
            tag.decompose()

        return soup.get_text(separator=" ", strip = True)[:4000]
    except Exception as e:
        raise(e, sys)