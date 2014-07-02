== Bing Ads Keywords Scraper

Contains a Python Bing Ads SOAP/WSDL class (see `bingapi.py`) toher with a script that uses this API to scrape keyword information on a daily basis (`scrape.py`). 

While this code is fairly specific to the task at hand, it's a good starting point if you want to query the Bing Ads API in python. Be warned of the code quality in this script. No error checking or anything like that. Use at your own risk!

=== Data scraped

Given a start and end date, and a set of keywords, this script queries the Bing Ads API for three endpoints:

- **Historical Search Count**: Daily amount of times the query was issued in the UK. Likely normalised, but results should hopefully be comparable across dates. See http://msdn.microsoft.com/en-US/library/dn336988.aspx
- **Keyword Demographics**: Scrapes the keyword UK demographics (age, gender) daily. The documentation does not specify which time period this data is based on, but this script scrapes it daily, just in case it'll change over time. See http://msdn.microsoft.com/en-US/library/dn336994.aspx
- **Keyword Locations**: Scrapes the amount of times the query was issued in different UK locations. The API will only return the top 10 locations, so the script scrapes three geographical "levels", regional (1),metropolitan (2), city (3) ). Like with demographics, no time period is specified in the documentation, so the endpoint is also scraped daily. See http://msdn.microsoft.com/en-us/library/dn336993.aspx

=== Usage

Install dependencies in `requirements.txt`.

Move `config.py.example` to `config.py` and fill in values.

Place a valid OAuth refresh token in `refreshtoken`. This file will be updated every time the script is run, so make sure it's writable.

Run using `python scrape.py`