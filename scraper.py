from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq()

# change this keyword for what keyword you want to use.
item = "Coronavirus"
kw_list = [item]
print(kw_list)

# payload string. cat is category, 
# timeframe is the time from today during which this term has been searched.
# geo defaults to world. if you want a certain country, refer to list of countries in c_codes.csv
# look on pytrends documentation for more info.
pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='', gprop='')

# scrape all info by country based on above payload.
# the pytrends calls return a panda dataframe. geocode is included to simplify adding to a database. 
# we then reset the index so it is indexed by number rather
# than by country name.
# we also remove any items with an interest level of 0 in the dataframe (because then the country dkidnt
# search that term)

countriesdf = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=False, inc_geo_code=True)
countriesdf = countriesdf[countriesdf[item] != 0].reset_index()

# generates a CSV named <keyword>_countries.csv which is a list of all countries that have
# searched the term, their country code, and the interest level 1-100 of the search term relative
# to other countries
countriesdf.to_csv(item + "_countries.csv")

# this line is optional, can technically remove it.
countriesdf = pd.read_csv(item + "_countries.csv")

# goes over every country by countrycode in the file we just made
for code in countriesdf.geoCode:
	try:
		
		# searches for the keyword with a new type of payload with location set ONLY to the country code.
		pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo=code, gprop='')

		# returns a panda dataframe with info similar to the country dataframe, but this time for every subregion
		# of the country defined by country code
		regions = pytrends.interest_by_region(resolution='region', inc_low_vol=False, inc_geo_code=True)
		
		# once again reset index to make the csv nicer and remove all 0 interest values
		regions = regions[regions[item] != 0].reset_index()

		# add table in csv that corresponds to the country of the subregion
		regions["country_code"] = code

		# format filename as <keyword>_<countrycode>.csv and create the csv.
		filename = item + "_" + code + ".csv"
		regions.to_csv(filename)

	except:
		continue

	
