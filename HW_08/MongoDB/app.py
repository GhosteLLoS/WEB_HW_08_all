import argparse

from mongoengine import *
from pymongo import MongoClient

client = MongoClient("mongodb+srv://ghost85:567234@cluster-1.0jyalqj.mongodb.net/?retryWrites=true&w=majority")

parser = argparse.ArgumentParser(description='Authors APP')
parser.add_argument('--action', help='Command: find')
parser.add_argument('--fullname')
parser.add_argument('--tags')

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
full_name = my_arg.get('fullname')
tags = my_arg.get('tags')


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


def find():
    author = client.authors.find()
    return author


def main(action=None):
    match action:

        case 'find':
            result = find()

            [print(r.to_mongo().to_dict()) for r in result]

        case _:
            print("Unknown command")


if __name__ == '__main__':
    main()
    # print(find_by_id("649b1a8bc48b832dfb7146f8"))
