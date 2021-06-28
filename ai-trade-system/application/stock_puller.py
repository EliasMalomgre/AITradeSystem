import logging
from datetime import datetime

import yfinance as yf

from application.stock_data_parser import StockDataParser
from domain.frequency import Frequency
from domain.share_entry import ShareEntry
from repositories.stock_repository import StockRepository


class StockPuller:
    def __init__(self):
        self.repo: StockRepository = StockRepository()
        self.parser: StockDataParser = StockDataParser()

    @staticmethod
    def pull_history(stock_name: str, start_date: datetime, end_date: datetime, frequency: Frequency):
        """Pulls stock inforamation for stock with a given freq and period"""
        logging.info("Start pulling {} stock history between {} and {} with frequency {}"
                     .format(stock_name, start_date, end_date, frequency))

        # Pull data from Yahoo
        data_df = yf.download(stock_name, start=start_date, end=end_date, interval=frequency)

        logging.info("Pulled {} stock history entries form stock {} between {} and {} with frequency {}"
                     .format(len(data_df["Open"]), stock_name, start_date, end_date, frequency))
        return data_df

    def update_history(self, stock_name: str, frequency: Frequency):
        most_recent: ShareEntry = self.repo.get_most_recent_entry(stock_name, frequency)

        needsUpdate = False
        if most_recent != None:
            most_recent_date: datetime = most_recent.date

            if frequency == Frequency.ONE_MONTH:
                if most_recent_date.strftime("%Y-%m") != datetime.now().strftime("%Y-%m"):
                    needsUpdate = True
            if frequency == Frequency.ONE_DAY or frequency == Frequency.ONE_WEEK:
                if most_recent_date.strftime("%Y-%m-%d") != datetime.now().strftime("%Y-%m-%d"):
                    needsUpdate = True
            if frequency == Frequency.ONE_HOUR:
                if most_recent_date.strftime("%Y-%m-%d-%h") != datetime.now().strftime("%Y-%m-%d-%h"):
                    needsUpdate = True
            if frequency == Frequency.ONE_MINUTE:
                if most_recent_date.strftime("%Y-%m-%d-%h-%M") != datetime.now().strftime("%Y-%m-%d-%h-%M"):
                    needsUpdate = True
        else:
            needsUpdate = True

        if (needsUpdate):
            for entry in list(
                    dict.fromkeys(self.parser.df_to_share_entry_array(self.pull_history(stock_name, most_recent.date,
                                                                                        datetime.now(), frequency),
                                                                      stock_name, frequency))):
                self.repo.save_entry(entry)

    @staticmethod
    def get_info(stock_name: str):
        """Returns the information of a stock"""
        return yf.Ticker(stock_name).info

    def pull_data(self, stock_name: str, start_date: datetime, end_date: datetime, freq: Frequency):
        """Pulls and saves data from Yahoo"""
        for entry in self.parser.df_to_share_entry_array(self.pull_history(stock_name, start_date,
                                                                           end_date, freq.value), stock_name,
                                                         freq.value):
            if self.repo.check_if_exists(entry.name, entry.freq, entry.date) == False:
                self.repo.save_entry(entry)
