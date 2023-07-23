import json

from bson import ObjectId
from mongoengine import *
from pymongo import MongoClient

client = MongoClient("mongodb+srv://ghost85:567234@cluster-1.0jyalqj.mongodb.net/?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


authors_collection = client['web12']['authors']

with open('authors.json') as fd:
    authors_data = json.load(fd)

for author_data in authors_data:
    author = Author(
        fullname=author_data['fullname'],
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()

quotes_collection = client['web12']['quotes']

with open('quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = authors_collection.authors.find_one({'fullname': quote['author']})
    if author:
        authors_collection.quotes.insert({
            'tags': quote['tags'],
            'author': ObjectId(author['_id']),
            'quote': quote['quote']
        })

client.close()
