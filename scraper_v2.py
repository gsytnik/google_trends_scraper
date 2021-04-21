from pytrends.request import TrendReq
import pandas as pd
pytrends = TrendReq()

# int formatted as YYYY (see pytrends documentation)
# year for list of top searched terms.
timef_for_term = 2019

# timeframe for country/subregion interests in terms
# formats:
# Defaults to last 5yrs, 'today 5-y'.
# Specific dates, 'YYYY-MM-DD YYYY-MM-DD' 
# Everything 'all'
# Specific datetimes, 'YYYY-MM-DDTHH YYYY-MM-DDTHH' example '2017-02-06T10 2017-02-12T07'
# By Month, Day, or hour: 'today #-m', 'now #-d', 'now #-H' 
# where # can be {1, 3, 12} for m; {1, 7} for d; {1, 4} for H
timef_for_loc = '2019-01-01 2019-12-31'

def gen_top_terms(tframe):
	

	# generates topcharts for year or year an month, int formatted as YYYY (see pytrends documentation)
	topcharts = pytrends.top_charts(tframe, hl='en-US', tz=300, geo='GLOBAL').reset_index()
	topcharts.to_csv("top_terms.csv")
	print(topcharts)


def gen_country_interests(term, tframe):
	# change this keyword for what keyword you want to use.
	kw_list = [term]
	print(kw_list)

	# payload string. cat is category, 
	# timeframe is the time from today during which this term has been searched.
	# geo defaults to world. if you want a certain country, refer to list of countries in c_codes.csv
	# look on pytrends documentation for more info.
	pytrends.build_payload(kw_list, cat=0, timeframe=tframe, geo='', gprop='')

	# scrape all info by country based on above payload.
	# the pytrends calls return a panda dataframe. geocode is included to simplify adding to a database. 
	# we then reset the index so it is indexed by number rather
	# than by country name.
	# we also remove any items with an interest level of 0 in the dataframe (because then the country dkidnt
	# search that term)

	countriesdf = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=False, inc_geo_code=True)
	countriesdf = countriesdf[countriesdf[term] != 0].reset_index()

	# generates a CSV named <keyword>_countries.csv which is a list of all countries that have
	# searched the term, their country code, and the interest level 1-100 of the search term relative
	# to other countries
	countriesdf.to_csv(term + "_countries.csv")


def gen_subregion_interests(term, country_code, tframe, ptrend):
	
	kw_list = [term]
	# goes over every region in country with country_code
	try:
		
		# searches for the keyword with a new type of payload with location set ONLY to the country code.
		ptrend.build_payload(kw_list, cat=0, timeframe=tframe, geo=country_code, gprop='')

		# returns a panda dataframe with info similar to the country dataframe, but this time for every subregion
		# of the country defined by country code
		regions = ptrend.interest_by_region(resolution='region', inc_low_vol=False, inc_geo_code=True)
		
		# once again reset index to make the csv nicer and remove all 0 interest values
		regions = regions[regions[term] != 0].reset_index()

		# add table in csv that corresponds to the country of the subregion
		regions["country_code"] = country_code

		# format filename as <keyword>_<countrycode>.csv and create the csv.
		filename = term + "_" + country_code + ".csv"
		regions.to_csv(filename)
	except:
		return


def main():

	gen_top_terms(timef_for_term)
	
	df = pd.read_csv("top_terms.csv")
	words = [word for word in df.title]
	print(words)

	for word in words:
		gen_country_interests(word, timef_for_loc)
		countriesdf = pd.read_csv(word + "_countries.csv")
		pytrends2 = TrendReq()
		for code in countriesdf.geoCode:
			gen_subregion_interests(word, code, timef_for_loc, pytrends2)

	print("finished") 



if __name__ == '__main__':
	main()


