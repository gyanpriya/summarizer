from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import feedparser
from newspaper import Article
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def fetch_news_articles(topic, max_articles=5):
    url = f"https://news.google.com/rss/search?q={topic}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    feed = feedparser.parse(requests.get(url, headers=headers).content)
    return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:max_articles]]

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print("Error extracting article:", e)
        return ""

def summarize_text(text):
    try:
        response = requests.post(
            HF_API_URL,
            headers=HEADERS,
            json={"inputs": text}
        )
        result = response.json()
        return result[0]['summary_text'] if isinstance(result, list) and 'summary_text' in result[0] else "Summary failed."
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def home():
    return {"message": "Flask summarizer running"}

@app.route("/summarize", methods=["POST"])
def summarize():
    topic = request.json.get("topic", "")
    articles = fetch_news_articles(topic)
    summaries = []

    for art in articles:
        text = extract_text_from_url(art["link"])
        summary = summarize_text(text)
        summaries.append({
            "title": art["title"],
            "link": art["link"],
            "summary": summary
        })

    final_text = " ".join([s["summary"] for s in summaries])
    final_summary = summarize_text(final_text)
    return jsonify({
        "summaries": summaries,
        "consolidated": final_summary
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
