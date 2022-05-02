from flask import *
import json
import uuid
import random

app = Flask(__name__)

# Line 9 creates  some default articles which the user can test the API with without having to POST articles.
Articles = [
    {'id': "0", "title": "my 0 title", "date": "2016-09-22", "body": "Some Text", "tags": ["Health", "Fitness"]},
    {'id': "1", "title": "my 1 title", "date": "2016-09-22", "body": "Some Text", "tags": ["Sport", "Health"]},
    {'id': "2", "title": "my 2 title", "date": "2016-09-22", "body": "Some Text",
     "tags": ["Computers", "Fitness", "Tech"]}]
TempArticles = []
TempArticleIDs = []
TempTags = []


# Displays A Welcome Message in the form of a JSON
@app.route('/', methods=['GET'])
def home_page():
    welcomeMessage = {'Page': 'Home', 'Message': "This is the home Page of this API"}
    return welcomeMessage


# Displays all articles to the user
@app.route('/articlesall', methods=['GET'])
def returnArticles():
    return jsonify(Articles)


# Displays the article which contains the same ID entered by the user
@app.route('/articles/<string:id>', methods=['GET'])
def returnMatched(id):
    matchedArticle = [article for article in Articles if article['id'] == id]
    return jsonify(matchedArticle)


# Displays a list of articles which contain the Tag and Date provided by the user
@app.route('/tags/<string:tag>/<string:date>', methods=['GET'])
def returnMatchedArticle(tag, date):
    resetLists()
    matchedArticle = [article for article in Articles if article['date'].replace("-", "") == date]
    for articles in matchedArticle:
        for tags in articles['tags']:
            if tags == tag:
                TempArticles.append(articles)
                # TempTags.append(articles["tags"])
                TempArticleIDs.append(articles["id"])
    data_Set = {'tag': tag, 'count': TempArticles.__len__(), "articles": TempArticleIDs,
                "related_tags": articles['tags']}
    return jsonify(data_Set)


# Responsible for adding an Article to the article list above, and returning an updated version to the user
@app.route('/articles', methods=['POST'])
def addArticles():
    newID = request.json['id']
    existingArticle = [article for article in Articles if article['id'] == newID]
    if existingArticle.__len__() != 0:
        newID += "-" + str(random.randint(0, 100))
    articleToAdd = {'id': newID, "title": request.json['title'], "date": request.json['date'],
                    "body": request.json['body'], "tags": request.json['tags']}
    Articles.append(articleToAdd)
    return jsonify(Articles)


# A simple function responsible for resetting the list after each Query
def resetLists():
    TempArticles.clear()
    TempArticleIDs.clear()


if __name__ == '__main__':
    app.run()
