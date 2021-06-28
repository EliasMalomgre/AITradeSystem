from datetime import datetime

from mongoengine import Document, StringField, FloatField, IntField, DateTimeField


class TransactionLog(Document):
    action = StringField()
    price_per_share = FloatField()
    amount = IntField()
    stock_name = StringField()
    frequency = StringField()
    time_stamp = DateTimeField(default=datetime.now(None))
