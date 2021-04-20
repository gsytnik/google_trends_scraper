from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360, retries=10, backoff_factor=0.5)

# generates topcharts for year or year an month, int formatted as YYYY or YYYYMM (see pytrends documentation)
topcharts = pytrends.top_charts(2020, hl='en-US', tz=300, geo='GLOBAL').reset_index()
topcharts.to_csv("top_terms.csv")
print(topcharts)

