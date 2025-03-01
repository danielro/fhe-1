from flask import Flask, jsonify, request
from newspaper import Article, Config
import lxml
from html import unescape
 
app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    json_data = {'Hello': 'World!'}
    return jsonify(json_data)

@app.route('/api/v1/extract', methods=['POST'])
def extract_html():
    print("Inside extract")
    print(request)
    if not request.json or not 'articleUrl' in request.json:
        abort(400)
    article_url = request.json['articleUrl']
    article_html = extract_article_html(article_url)
    response = {'articleHtml': article_html}
    return jsonify(response), 200
 
def extract_article_html(url):
    config = Config()
    config.keep_article_html = True
    article = Article(url, config=config)
 
    article.download()
    article.parse()
 
    article_html = article.article_html
 
    html = lxml.html.fromstring(article_html)
    for tag in html.xpath('//*[@class]'):
        tag.attrib.pop('class')
 
    return lxml.html.tostring(html).decode('utf-8')

if __name__ == '__main__':
    app.run()
