import logging
from datetime import datetime

from domain.frequency import Frequency
from domain.share_entry import ShareEntry
from repositories.repository import Repository


class StockRepository(Repository):
    def __init__(self):
        super().__init__()

    @staticmethod
    def save_entry(entry: ShareEntry):

        entry.save()
        logging.debug("Saved entry: {}".format(entry))

    @staticmethod
    def get_all_entries():
        return ShareEntry.objects

    @staticmethod
    def get_entries_for_stock(stock_name: str):
        return ShareEntry.objects(name=stock_name)

    @staticmethod
    def get_entry_for_stock_date(stock_name: str, date: datetime):
        return ShareEntry.objects(name=stock_name, date=date).first()

    @staticmethod
    def get_entries_between(stock_name: str, start_date: datetime, end_date: datetime, freq: Frequency):
        return ShareEntry.objects(freq=freq.value, name=stock_name, date__gte=start_date, date__lte=end_date)

    @staticmethod
    def get_most_recent_entry(stock_name: str, freq: Frequency):
        return ShareEntry.objects(freq=freq.value, name=stock_name).order_by('-date').first()

    def check_if_exists(self, stock_name: str, frequency: Frequency, date: datetime):
        if ShareEntry.objects(freq=frequency, name=stock_name, date=date).first() is not None:
            return True
        else:
            return False
