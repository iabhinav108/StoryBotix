import requests
from dotenv import load_dotenv

load_dotenv()
def get_trending_news(api_key = 'API_KEY', country='us', category='technology', num_articles=5):
    url = f"http://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
    
    response = requests.get(url)
    # print("Status Code:", response.status_code)
    
    if response.status_code != 200:
        print("Error:", response.text)
        return []
    
    data = response.json()
    # print("Raw JSON:", data)  # Debug line
    articles = data.get("articles", [])
    print(f"Found {len(articles)} articles")

    trending_news = []
    for article in articles[:num_articles]:
        trending_news.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("url", "")
        })
    
    return trending_news



