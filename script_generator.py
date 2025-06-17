import re
import os
from news_scraper import get_trending_news

def generate_script_from_news(title, description, url=None):
    if not description or description.lower() == "None":
        description = "Full details on this story are emerging. Stay tuned for more updates as the situation develops."

    script = (
        f"Breaking News!\n\n"
        f"*{title}*\n\n"
        f"{description}\n\n"
        f"This development has sparked significant interest in the tech community. "
        f"Experts suggest this could mark a notable shift in industry trends.\n\n"
        f"To dive deeper, check the full article at: {url if url else 'source unavailable'}\n\n"
        f"That’s all for now! For more quick updates like this, stay tuned and subscribe!"
    )

    return script

def save_script_to_file(title, script, folder="assets/generated_scripts"):
    os.makedirs(folder, exist_ok=True)

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = os.path.join(folder, f"{safe_title[:50]}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"Script saved to {filename}")


# if __name__ == "__main__":
#     news_items = get_trending_news()

#     print("\n Trending News Articles:\n")
#     for idx, news in enumerate(news_items, start=1):
#         print(f"{idx}. {news['title']}")
#         print(f"   {news['description']}\n")
