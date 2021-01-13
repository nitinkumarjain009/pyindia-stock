import pandas as pd
import matplotlib.pyplot as plt
import requests
from fbprophet import Prophet
import time
import os
from datetime import datetime

CURRENT_DIR = os.getcwd()


class StockAnalysis:
    r"""Understanding and Analyzing Indian Stock with Graphs. 

    Args:
        index: NSE index name
        period_from: starting date to consider for evaluation. Date in "%d/%m/%Y,%H" format, H: should be in 24hrs format.
        period_from: Specific/present date to consider for evaluation. Date in "%d/%m/%Y,%H" format, H: should be in 24hrs format.Default: Sets present date and time. 

    Attributes:
        fbprophet: Instance of class FBProphet with daily seasonality.
        read_data: Read stock Dataframe 
        is_data_available: if data has loaded to dataframe and has suitable format, then in is true

    Examples:: 

        >>> m = StockAnalysis("SBIN",period_from="01/01/2000,15")
        >>> m.fit_plot(save_output=True)
    """

    def __init__(self, index: str, period_from, period_to: str = None):
        now = datetime.now()
        self.index = index.upper()
        self.period_from = time.mktime(datetime.strptime(
            period_from, "%d/%m/%Y,%H").timetuple())
        period_to = now.strftime("%d/%m/%Y,%H")
        if period_to is not None:
            self.period_to = time.mktime(datetime.strptime(
                period_to, "%d/%m/%Y,%H").timetuple())
        else:
            self.period_to = time.mktime(datetime.strptime(
                period_to, "%d/%m/%Y,%H").timetuple())
        self.is_data_available = False
        try:
            url = f'https://query1.finance.yahoo.com/v7/finance/download/{self.index}.NS?period1={int(self.period_from)}&period2={int(self.period_to)}&interval=1d&events=history&includeAdjustedClose=true'
            r = requests.get(url, allow_redirects=True)
            self.data_file = os.sep.join([CURRENT_DIR, f"{self.index}.csv"])
            open(self.data_file, 'wb').write(r.content)
            self.read_data = pd.read_csv(self.data_file)
            self.data = self.read_data[["Date", "Close"]]
            self.data = self.data.rename(columns={"Date": "ds", "Close": "y"})
            self.is_data_available = True
        except:
            print(
                "index Provided is not correct [No data found,  symbol may be delisted] Data has no Columns(Date,Close)")
        self.fbprophet = Prophet(daily_seasonality=True)

    def fit(self):
        if self.is_data_available:
            try:
                self.fbprophet.fit(self.data)
            except:
                print("something went wrong with class-instance")
        else:
            print("Data is not available")

    def plot(self, save_output):
        future = self.fbprophet.make_future_dataframe(periods=30)
        prediction = self.fbprophet.predict(future)
        self.fbprophet.plot(prediction)
        plt.title(f"prediction of {self.index} stock price")
        plt.xlabel("date")
        plt.ylabel("close stock price")
        plt.show()
        self.fbprophet.plot_components(prediction)
        if save_output:
            future.to_csv(f"{self.index}_output.csv", index=False)
            plt.savefig(f"{self.index}_prediction.png")
            self.fbprophet.plot_components(prediction)
            plt.savefig(f"{self.index}_trends.png")

    def fit_plot(self, save_output=False):
        self.fit()
        self.plot(save_output)
