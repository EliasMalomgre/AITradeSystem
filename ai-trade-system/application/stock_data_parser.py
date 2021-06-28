from domain.frequency import Frequency
from domain.share_entry import ShareEntry
from properties.properties import Properties


class StockDataParser:
    def __init__(self):
        self.properties: Properties = Properties()

    def df_to_share_entry_array(self, df, stock_name: str, freq: Frequency) -> [ShareEntry]:
        """Parser pulled stock data to ShareEntries"""
        share_entries: [] = []

        if freq is None:
            freq = self.properties.default_freq

        # Iterate over all data in the dataframe
        for index, row in df.iterrows():
            # Calculate the ratio correct the stock information
            ratio = row['Adj Close'] / row['Close']
            # Parse to ShareEntry
            document = ShareEntry(name=stock_name, date=row.name, freq=freq, open=row['Open'] * ratio,
                                  high=row['High'] * ratio, low=row['Low'] * ratio,
                                  close=row['Close'], adj_close=row['Adj Close'], volume=row['Volume'])
            share_entries.append(document)
        return share_entries
