import anthropic as ap
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/surch', methods=['POST'])
def surch():
    tags = request.form.get("tag").split()
    request_message = request.form.get("request_message")
    query = "".join([f"tag:{tag}" for tag in tags])

    print(tags)
    print(request_message)

    url = f"https://qiita.com/api/v2/items"
    params = {
        "query": query,
        "per_page": 10,
        "page": 1
    }

    print(params)
    response = requests.get(url, params=params)
    articles = response.json()

    titles = []
    urls = []

    for article in articles:
        titles.append(article['title'])
        urls.append(article['url'])
    
    title_query = "".join([f"title:{title}" for title in titles])
    url_query = "".join([f"url:{url}" for url in urls])

    load_dotenv()

    client = ap.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=4096,
        messages = [{
            "role":"user",
            "content":f"titleとurlの一覧からピックアップして要望に沿った教材とロードマップを作成してください\n title:{title_query}\n url:{url_query}\n {request_message}"
        }]
    )

    output = (message.content[0].text)

    return render_template(
        "index.html",
        output = output
    )