#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import bingapi
import xmltodict
from datetime import datetime,timedelta

def getall(country_code, countries, language, keywords, fromyear, frommonth, fromday, toyear, tomonth, today):
	# Get Historical Search Count #################################################################################	
	historical_search_count = api.service.GetHistoricalSearchCount(
		Keywords=bing.soapStrArr(api, keywords), 
		Language=language,
		PublisherCountries=bing.soapStrArr(api, countries),
		Devices=bing.soapStrArr(api, ["Computers", "NonSmartphones", "Smartphones", "Tablets"]),
		StartDate=bing.soapDate(api, fromyear, frommonth, fromday),
		EndDate=bing.soapDate(api, toyear, tomonth, today),
		TimePeriodRollup="Daily"
		)

	search_count_dict = xmltodict.parse(historical_search_count)
	jsonout = bing.toPrettyJson(search_count_dict['s:Envelope']['s:Body']['GetHistoricalSearchCountResponse'])

	with open('HistoricalSearchCount_{3}/{0}{1}{2}.json'.format(fromyear,frommonth,fromday,country_code), 'w+') as f:
		f.write(jsonout)
	
	# Get Demographics UK #################################################################################
	demographics_request = api.service.GetKeywordDemographics(
		Keywords=bing.soapStrArr(api, keywords), 
		Devices=bing.soapStrArr(api, ["Computers", "NonSmartphones", "Smartphones", "Tablets"]),
		Language=language,
		PublisherCountries=bing.soapStrArr(api, countries)
		)

	demographics_request_dict = xmltodict.parse(demographics_request)
	jsonout = bing.toPrettyJson(demographics_request_dict['s:Envelope']['s:Body']['GetKeywordDemographicsResponse'])

	with open('KeywordDemographics_{3}/{0}{1}{2}.json'.format(fromyear,frommonth,fromday,country_code), 'w+') as f:
		f.write(jsonout)

	# Get Locations #################################################################################
	for level in xrange(1,4):
		locations_request = api.service.GetKeywordLocations(
			Keywords=bing.soapStrArr(api, keywords), 
			Devices=bing.soapStrArr(api, ["Computers", "NonSmartphones", "Smartphones", "Tablets"]),
			Language=language,
			Level=level,
			ParentCountry=country_code,
			PublisherCountries=bing.soapStrArr(api, countries)
			)

		locations_request_dict = xmltodict.parse(locations_request)
		jsonout = bing.toPrettyJson(locations_request_dict['s:Envelope']['s:Body']['GetKeywordLocationsResponse'])

		with open('KeywordLocations_{4}/{0}{1}{2}_{3}.json'.format(fromyear,frommonth,fromday,level,country_code), 'w+') as f:
			f.write(jsonout)	

##################################################################################################################
##################################################################################################################
##################################################################################################################

bing = bingapi.bingapi()
api = bing.getapi(config.developertoken, config.customerid, config.accountid, config.clientid, config.clientsecret)

# read keywords
with open("keywords.gb") as f:
	keywordsuk = map(str.strip, f.readlines())

with open("keywords.dk") as f:
	keywordsdk = []
	for l in f:		
		keywordsdk.append(l.decode("utf8").strip())

# not sure exactly when the api makes data available. values (counts etc) may be simply be null if the data isn't
# ready yet, so simply fetch the data, and overwrite the last couple of days' files as well, just to make sure
# that "empty" files are overwritten by files with useful data. Be aware of this when actually using the data!
for i in xrange(0, 3):
	yday = datetime.now() - timedelta(days=i)
	tday = datetime.now() - timedelta(days=i)

	fromyear = yday.strftime("%Y")
	frommonth = yday.strftime("%m")
	fromday = yday.strftime("%d")

	toyear = tday.strftime("%Y")
	tomonth = tday.strftime("%m")
	today = tday.strftime("%d")

	getall('GB', ['GB'], 'English', keywordsuk, fromyear, frommonth, fromday, toyear, tomonth, today)
	getall('DK', ['DK'], 'Danish', keywordsdk, fromyear, frommonth, fromday, toyear, tomonth, today)
