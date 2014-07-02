from suds.client import Client
from suds.sax.element import Element
from suds.xsd.sxbasic import Import
import urllib
import json
import logging
import sys
import xmltodict, json
from pprint import pprint

class bingapi:
	
	def soapStrArr(self, api, arr):
		val = api.factory.create('ns2:ArrayOfstring')
		val.string = arr
		return val

	def soapDate(self, api, year, month, day):
		val = api.factory.create('ns0:DayMonthAndYear')
		val.Year = year
		val.Month = month
		val.Day = day		
		return val

	""" Convert XML returned from the Bing Ads API to prettier json """	
	def toPrettyJson(self, xmlDict):	
		retval = json.dumps(xmlDict)
		# remove the ugly xml prefixes
		for c in list("qwertyuiopasdfghjklzxcvbnm"):
			retval = retval.replace("\"{0}:".format(c), "\"")
		return retval

	""" Returns a suds Bing Ads API client"""
	def getapi(self, developer_token, customer_id, account_id, client_id, client_secret):

		DEVELOPER_TOKEN = developer_token
		CUSTOMER_ID = customer_id
		CUSTOMER_ACCOUNT_ID = account_id

		# enable logging
		#logging.basicConfig(level=logging.INFO)
		#logging.getLogger('suds.client').setLevel(logging.DEBUG)

		#print "Obtaining new Access Token"
		# Obtain a refresh token using the authorization code grant flow: http://msdn.microsoft.com/en-us/library/dn277356.aspx
		with open("refreshtoken", "r+") as tokenfile:
		    # get current refresh token from file
		    refresh_token = tokenfile.read().replace('\n', '')
		    
		    # obtain access token and new refresh token
		    refresh_token_url = "https://login.live.com/oauth20_token.srf?client_id={0}&client_secret={1}&grant_type=refresh_token&redirect_uri=https://login.live.com/oauth20_desktop.srf&refresh_token={2}".format(client_id, client_secret, refresh_token)
		    refresh_token_url_file = urllib.urlopen(refresh_token_url)
		    refresh_token_res = json.loads( refresh_token_url_file.read() )
		    new_refresh_token = refresh_token_res['refresh_token']
		    access_token = refresh_token_res['access_token']

		    # write refresh token back to file
		    tokenfile.seek(0)
		    tokenfile.write(new_refresh_token)
		    tokenfile.truncate()
		    
		#print "Fetching Yesterdays queries"

		#Import.bind("v9", "https://bingads.microsoft.com/AdIntelligence/v9")
		api = Client("https://api.bingads.microsoft.com/Api/Advertiser/AdIntelligence/V9/AdIntelligenceService.svc?singleWsdl", retxml=True)


		#print _soapDate(2014, 05, 30)
		#print api
		#sys.exit(0)

		# add authentication headers to client
		devtoken = Element('ns0:DeveloperToken').setText(DEVELOPER_TOKEN)
		cid = Element('ns0:CustomerId').setText(CUSTOMER_ID)
		aid = Element('ns0:CustomerAccountId').setText(CUSTOMER_ACCOUNT_ID)
		authtoken = Element('ns0:AuthenticationToken').setText(access_token)

		api.set_options(soapheaders=(devtoken,cid,aid,authtoken))

		return api

