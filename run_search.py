import json
import pandas as pd
import requests
from datetime import datetime
import urllib.parse as url_parser
import sys


class QueryCustomSearch():
    """
    Class to perform query using a Google's custom search engine.
    """
    with open('API.txt', 'r') as f:
        API_KEY = f.read()
    CX_ID = '002952611959853601935:o02wadftpuk'  # Default search
    API_REST_URL = 'https://www.googleapis.com/customsearch/v1'
    QUERY = ('Workspace Worklife Automation Digital Future' +
             ' -filetype:pdf' + ' inurl:2019')

    def __init__(self, query=None, cx_id=None, api_key=None, run=True):
        if query is None:
            self.query = QueryCustomSearch.QUERY
        if cx_id is None:
            self.cx_id = QueryCustomSearch.CX_ID
        if api_key is None:
            self.api_key = QueryCustomSearch.API_KEY
        self.result = self.get_query_result()

    def _get_api_url(self):
        return (self.API_REST_URL + '?key=' + self.api_key +
                '&cx=' + self.cx_id + '&q=' + url_parser.quote_plus(self.query))

    def get_query_result(self):
        """
        Get the search result query as a dict.

        Return:
            urls: dict with with the URLs and datetime
        """
        # Google's Rest API for Custom Search
        api_url = self._get_api_url()
        page = requests.get(api_url)
        json_data = page.json()
        result = {"url": [],
                  "datetime": datetime.today()}
        try:
            search_results = json_data['items']
            # URLS
            result["url"] = [r['link'] for r in search_results]
        except KeyError:
            print("No results found for query: {}".format(self.query))
            result["url"] = []
        return result

    def create_df(self, save=True, date_format="%Y-%m-%d_%H-%M"):
        """
        Create a DataFrame with the results from the query.

        Args:
            save: Whether save the df as a csv or not.
            date_format: Date format to show datetime object.
        Return:
            df: Pandas DataFrame with the urls and date.
        """
        data = {'url': self.result["url"],
                'datetime': [self.result["datetime"]] * len(self.result["url"])}
        df = pd.DataFrame(data)
        df.datetime = pd.to_datetime(df.datetime)

        # Save result
        if save and len(self.result['url']):
            str_date = self.result["datetime"].strftime(date_format)
            df.to_csv("URLs_" + str_date + ".csv", date_format=date_format,
                      index=False)

        return df

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = None

    # Query object
    qcs = QueryCustomSearch(query)
    qcs.create_df()
