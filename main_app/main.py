import anthropic as ap
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests
import os


app = Flask(__name__)

error_mes = "出力に失敗しました。入力内容を確認してください。"

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/surch', methods=['POST'])
def surch():
    tags = request.form.get("tag").split()
    request_message = request.form.get("request_message")
    query = " ".join([f"tag:{tag}" for tag in tags])

    if not query:
        output = error_mes
        render_template(
            'index.html',
            output = output
        )

    url = f"https://qiita.com/api/v2/items"
    params = {
        "query": query,
        "per_page": 10,
        "page": 1
    }

    print(params)
    response = requests.get(url, params=params)
    articles = response.json()

    print(articles)

    titles = []
    urls = []
    bodys = []

    for article in articles:
        titles.append(article['title'])
        urls.append(article['url'])
        # bodys.append(article['body'])
    
    title_query = "".join([f"title:{title}" for title in titles])
    url_query = "".join([f"url:{url}" for url in urls])
    # body_query = "".join([f"body:{body}" for body in bodys])

    if not title_query:
        output = error_mes
        return render_template(
            'index.html',
            output = output
        )
    
    elif not url_query:
        output = error_mes
        return render_template(
            'index.html',
            output = output
        )
    
    # elif not body_query:
    #     output = error_mes
    #     return render_template(
    #         'index.html',
    #         output = output
    #     )

    load_dotenv()

    client = ap.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=5000,
        messages = [{
            "role":"user",
            "content":f"titleとurlの一覧からピックアップして要望に沿った教材とロードマップをHTML記述で作成してください（urlをaタグで囲って出力等）\n title:{title_query}\n url:{url_query}\n {request_message}"
        }]
    )

    output = (message.content[0].text)

    return render_template(
        "index.html",
        output = output
    )

@app.route('/next', methods=['POST'])
def next():
    return render_template(
        'index_next.html'
    )