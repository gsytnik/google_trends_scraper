# google_trends_scraper
scraper files for google trends using pytrends and pandas.


# instructions
***scraper_v2***
* New and improved, the scraper_v2 is finally here! 
* this will do the same thing as both of the files below but will automate the entire process
* first generates a csv list of top terms based on year you want to search
* for each term generates csvs of (non - 0) interest values in that term within a given timeframe by country and every subregion in it.
* **see below for formatting information. csv files will have the same naming scheme as below.**
* sample files shown in sampleData.zip.
* open python file and see comments inside on what you can change. provides easily changeable values for year of top terms and timeframe for countries.

***top_trends_scraper.py***

* will generate a csv of top terms for a given year (defaulted to 2020).
* the usage is documented inside the file, so you can open it and easily change the data it will give you.

***scraper.py***

* will generate csvs of interest levels for a single given search term 
(which you have to manually plug in via the python code, again well documented)

* **one csv will be formatted as "searchterm_countries.csv"**
	* this csv is a list of interest levels by country

* **the rest of the csv files will be formatted as "searchterm_CC.csv"**
	* this csv is a list of interest levels by subregion of the country with countrycode.
	* the CC (country code) is a corresponding 2 letter country code for the parent country of the subregions in this csv

***insert_generator.py***

* **CREDIT TO Hadi Asemi: https://github.com/Hadiasemi**
* will generate SQL Insert compatible tuples for EVERY file in the same directory that this file is run in.
* **not compatible with scraper generated CSVs. See *"additional included items"* section for compatible versions**

# limitations

1) **too many google http requests in a short time will result in a code 429 - effectively blocking your ip from scraping.**
	* you can easily scrape info on up to ten terms before being banned. **may be less terms if using scraper_v2, but it will print out your list in the console so you can manually run the list into the file if you wish by editing a few pieces of code**.
	* pytrends states:
		* Rate Limit is not publicly known, let me know if you have a consistent estimate.
		* One user reports that 1,400 sequential requests of a 4 hours timeframe got them to the limit. (Replicated on 2 networks)
		* It has been tested, and 60 seconds of sleep between requests (successful or not) is the correct amount once you reach the limit.
	* another way to circumvent this is to use a VPN and switch your IP.

2) **csv files do not get allocated to a new subdirectory when you run the script.**
	* it is up to you to organize all the files into folders thereafter.

3) **currently can't generate csvs for queries with certain special characters.**
	* currently known characters: {':'}
	* potential patch coming in the near future, if requested.


4) **if running scraper.py and not scraper_v2, terms to scrape must be entered manually**
	* open file for instructions on how to do so.


# dependencies
1) pip install pytrends:
	https://github.com/GeneralMills/pytrends
	https://pypi.org/project/pytrends/

2) pip install pandas:
	https://pandas.pydata.org/


# additional included items:

1) **c_codes.csv:**
	* this is a csv file containing two columns for every country in google trends
	* one with the country name
	* the other with the corresponding country code
	* although pytrends does this automatically in the other csvs, this can be a convenient csv file to have for a country + country code database.

2) **two modified SQL insert statement generator files:**
	
	***generate_by_code.py:***

	if you would like to generate the tuples for a sql insert statement for
	files with formatting: "searchterm_CC.csv" (*CC (country code)*), running this will generate in the console

	the tuples as: (geo_code, interest, country_code, term) where

	* geo_code = google trend's geocode for this subregion
	* interest = numeric interest value in search term within this region compared to other regions
	* country_code = google trend's geocode for parent country
	* term = search term whose info is being pulled
	--------------------------------------------------------------------------------

	***generate_by_country.py:***

	if you would like to generate the tuples for a sql insert statement for
	files with formatting: "searchterm_countries.csv", running this will generate in the console

	the tuples as: (geo_code, interest, term) where

	* geo_code = google trend's geocode for this country
	* interest = numeric interest value in search term within this region compared to other regions
	* term = search term whose info is being pulled
	-------------------------------------------------------------------------------
3) **insert_generator.py**

	**CREDIT TO Hadi Asemi: https://github.com/Hadiasemi**

	* this is the original tuple generator for sql insert statements and will not ignore any rows in a csv.
	* it will not work with the scraper generated csv files unless the first row is stripped from each line
	via line[1:] because of the row 0 column 0 slot being a blank value. 
	* will work for most other CSV files though.


# recommendations:

to make things simpler, after running both scrapers: 

1) organize all files with format: "term_countries.csv" into one folder and run **generate_by_country.py** in that folder.

2) then, organize all files with format: "term_CC.csv" (*CC (country code)*) into another folder, or folders by term,
and run the **generate_by_code.py** file in the folder(s) to get the insert statements for these items.


