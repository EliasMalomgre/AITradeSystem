from mongoengine import Document, DateTimeField, FloatField, IntField, StringField


class ShareEntry(Document):
    name = StringField()
    date = DateTimeField()
    freq = StringField()
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    adj_close = FloatField()
    volume = IntField()

    def __str__(self):
        return self.name + " " + str(self.date)
