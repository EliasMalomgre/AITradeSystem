from mongoengine import connect

from properties.properties import Properties


class Repository:
    def __init__(self):
        properties: Properties = Properties()
        connect(host=properties.db_uri)
