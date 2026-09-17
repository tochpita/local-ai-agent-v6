from urllib.parse import quote_plus, urlparse, parse_qs, unquote
import requests
from bs4 import BeautifulSoup
def web_search(query):
    if not query.strip():return {"success":False,"error":"Search query is empty."}
    try:
        response=requests.get("https://html.duckduckgo.com/html/?q="+quote_plus(query),headers={"User-Agent":"Mozilla/5.0"},timeout=12);response.raise_for_status();results=[]
        for row in BeautifulSoup(response.text,"html.parser").select(".result"):
            link=row.select_one(".result__a")
            if link:
                url=link.get("href","")
                # DuckDuckGo returns a tracking redirect; give the model the real
                # destination so it can compare sources and navigate directly.
                params=parse_qs(urlparse(url).query)
                url=unquote(params.get("uddg",[url])[0])
                results.append({"title":link.get_text(" ",strip=True),"url":url,"snippet":(row.select_one(".result__snippet").get_text(" ",strip=True) if row.select_one(".result__snippet") else "")[:400]})
            if len(results)==8:break
        return {"success":bool(results),"results":results} if results else {"success":False,"error":"No results found."}
    except Exception as e:return {"success":False,"error":f"Search failed: {e}"}
