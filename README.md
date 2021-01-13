# StockAnalysis

## Installation
As ususal installation 
```
$ pip install pyindia-stock
```
It uses FBProphet for analysis and prediction. 

## Getting Started
You can use command-line script. 
`pyindia_stock -h` will give the following.

```
usage: pyindia_stock [-h] --index INDEX --from_date FROM_DATE
                     [--to_date TO_DATE]

Analyzing the Past Behavior of an index from Indian Stock Market

required arguments:
  --index INDEX         NSE index name
  --from_date FROM_DATE
                        starting date to consider for evaluation. Date in
                        d/m/Y,H format, H: should be in 24hrs format

optional arguments:
  --to_date TO_DATE     Specific/present date to consider for evaluation. Date
                        in d/m/Y,H format, H: should be in 24hrs format.
                        Default: Sets to present date and time.
```

You can use it in scripts.
```
# import pyindia_stock
$ from pyindia_stock import StockAnalysis

# run StockAnalysis with index and period_from as arguments.
$ StockAnalysis("SBIN",period_from="01/01/2000,15")

# StockAnalysis has the following arguments:
# - index: Only NSE index name
# - period_from: starting date to consider for evaluation. Date in "%d/%m/%Y,%H" format, H: should be in 24hrs format.
# - period_to: Specific/present date to consider for evaluation. Date in "%d/%m/%Y,%H" format, H: should be in 24hrs 				format.Default: Sets present date and time.
#StockAnalysis has attributes 
# - read_data: Read stock Dataframe
# - fbprophet: Instance of class FBProphet with daily seasonality.
# - is_data_available: if data has loaded to dataframe and has suitable format, then in is true

```

## How to use it?
Colab starter notebook: 

## About FBProphet:
Prophet is a forecasting procedure implementation in R and Python. It is fast and provides completely automated forecasts that can be tuned by hand by data scientists and analysts. \
Prophet follows the sklearn model API. We create an instance of the Prophet class and then call its fit and predict methods.\
The input to Prophet is always a dataframe with two columns: ds and y. The ds (datestamp) column should be of a format expected by Pandas, ideally YYYY-MM-DD for a date or YYYY-MM-DD HH:MM:SS for a timestamp. The y column must be numeric, and represents the measurement we wish to forecast.


