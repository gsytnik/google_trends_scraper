from pytrends.request import TrendReq
import pandas as pd

def gen_top_terms(tframe):
	pytrends = TrendReq()

	# generates topcharts for year or year an month, int formatted as YYYY or YYYYMM (see pytrends documentation)
	topcharts = pytrends.top_charts(tframe, hl='en-US', tz=300, geo='GLOBAL').reset_index()
	topcharts.to_csv("top_terms.csv")
	print(topcharts)


def gen_country_interests(term):
	pytrends = TrendReq()

	# change this keyword for what keyword you want to use.
	kw_list = [term]
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
	countriesdf = countriesdf[countriesdf[term] != 0].reset_index()

	# generates a CSV named <keyword>_countries.csv which is a list of all countries that have
	# searched the term, their country code, and the interest level 1-100 of the search term relative
	# to other countries
	countriesdf.to_csv(term + "_countries.csv")


def gen_subregion_interests(term, country_code):
	pytrends = TrendReq()
	kw_list = [term]
	# goes over every region in country with country_code
	try:
		
		# searches for the keyword with a new type of payload with location set ONLY to the country code.
		pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo=country_code, gprop='')

		# returns a panda dataframe with info similar to the country dataframe, but this time for every subregion
		# of the country defined by country code
		regions = pytrends.interest_by_region(resolution='region', inc_low_vol=False, inc_geo_code=True)
		
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
	gen_top_terms(2020)
	df = pd.read_csv("top_terms.csv")

	for word in df.title:
		gen_country_interests(word)
		countriesdf = pd.read_csv(word + "_countries.csv")
		for code in countriesdf.geoCode:
			gen_subregion_interests(word, code)

	print("finished") 



if __name__ == '__main__':
	main()


