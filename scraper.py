import requests
from bs4 import BeautifulSoup
from readability import Document
import time

# Test mode with sample data
TEST_MODE = False  # Set to False to use real scraping/Tavily

# Tavily API configuration
def get_tavily_api_key():
    import os
    return os.getenv("TAVILY_API_KEY")

# Bangla news sources that work with static HTML
# Bangla news sources that work with static HTML
NEWS_SOURCES = [
    {
        "name": "BBC Bangla",
        "base_url": "https://www.bbc.com",
        "category_url": "https://www.bbc.com/bangla",
        "article_selector": "a[href*='/bangla/articles/']",
        "max_articles": 4
    },
    {
        "name": "Prothom Alo",
        "base_url": "https://www.prothomalo.com",
        "category_url": "https://www.prothomalo.com/bangladesh",
        "article_selector": "a.link_overlay",
        "max_articles": 4
    },
    {
        "name": "The Daily Star Bangla",
        "base_url": "https://bangla.thedailystar.net",
        "category_url": "https://bangla.thedailystar.net/news/bangladesh",
        "article_selector": "h3.title a",
        "max_articles": 3
    }
]

def get_article_links_tavily(query="Top news in Bangladesh last 24 hours in Bangla", days=1):
    """Use Tavily to find the latest Bangla news links from the last 24 hours."""
    api_key = get_tavily_api_key()
    if not api_key:
        print("⚠️ TAVILY_API_KEY not set. Skipping search.")
        return []
    
    try:
        from tavily import TavilyClient
        tavily = TavilyClient(api_key=api_key)
        
        # Search for recent news articles
        print(f"Searching Tavily for: {query}")
        search_result = tavily.search(
            query=query,
            search_depth="advanced",
            include_domains=["prothomalo.com", "bbc.com/bangla", "bangla.thedailystar.net", "kalerkantho.com", "jugantor.com", "samakal.com"],
            max_results=10,
            time_range="day"
        )
        
        links = [result["url"] for result in search_result.get("results", [])]
        return links
    except Exception as e:
        print(f"Error searching Tavily: {e}")
        return []

def fetch_article_text(url):
    """Fetch and extract clean article text from URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, timeout=12, headers=headers)
        response.raise_for_status()
        
        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), "lxml")
        
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30)
        
        title = doc.title()
        
        return {
            "title": title,
            "text": text[:3000], 
            "url": url
        }
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_article_links(source):
    """Get article links from a news source."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(source["category_url"], timeout=12, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        links = []
        
        for link in soup.select(source["article_selector"])[:15]:
            href = link.get("href")
            if href:
                if not href.startswith("http"):
                    href = source["base_url"].rstrip('/') + '/' + href.lstrip('/')
                
                if source["base_url"] in href or "bbc.com/bangla/articles" in href:
                    links.append(href)
        
        return list(dict.fromkeys(links))[:source["max_articles"]]
    except Exception as e:
        print(f"Error getting links from {source['name']}: {e}")
        return []

def scrape_news():
    """Scrape articles from all news sources and Tavily to ensure at least 8-10 articles."""
    
    if TEST_MODE:
        print("🧪 TEST MODE: Using sample articles")
        return SAMPLE_ARTICLES
    
    articles = []
    seen_urls = set()
    
    # 1. Direct scraping from major sources
    for source in NEWS_SOURCES:
        print(f"Scraping {source['name']}...")
        links = get_article_links(source)
        
        for link in links:
            if link not in seen_urls:
                article = fetch_article_text(link)
                if article and len(article["text"]) > 300:
                    articles.append(article)
                    seen_urls.add(link)
                time.sleep(1) 
    
    # 2. Tavily expansion/fallback to hit target
    if len(articles) < 10:
        print(f"Collected {len(articles)} articles. Using Tavily for more...")
        queries = ["Bangladesh top news today", "বাংলাদেশ আজকের ব্রেকিং নিউজ", "Bangladesh politics last 24h"]
        for query in queries:
            if len(articles) >= 12: break
            tavily_links = get_article_links_tavily(query=query)
            for link in tavily_links:
                if len(articles) >= 12: break
                if link not in seen_urls:
                    print(f"Fetching from Tavily: {link}")
                    article = fetch_article_text(link)
                    if article and len(article["text"]) > 300:
                        articles.append(article)
                        seen_urls.add(link)
                    time.sleep(1)
    
    print(f"Scraped {len(articles)} articles total (Direct + Tavily)")
    return articles[:12]

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    articles = scrape_news()
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   {article['url']}")
        print(f"   Text length: {len(article['text'])} chars")
