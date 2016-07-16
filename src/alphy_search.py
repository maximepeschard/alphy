#!/usr/bin/python
# encoding: utf-8

import sys
import os
import re
import urllib2
import unicodedata

from workflow import Workflow3, web
from alphy import search, CACHE_MAX_AGE

log = None
current_query = None
search_limit = None


def populate_alfred_results(search_results,query):
    """Build Alfred result list from the search result JSON"""

    # Add search results
    for result in search_results:
        gif_id = result['id']
        gif_slug_stripped = result['slug'].rsplit("-",1)[0]
        gif_title = gif_slug_stripped if len(gif_slug_stripped)>0 else gif_id
        gif_date = result['import_datetime'].rsplit(" ",1)[0]
        gif_width = result['images']['original']['width']
        gif_height = result['images']['original']['height']

        wf.add_item(title=gif_title,
                subtitle=gif_date + ' | ' + gif_width + 'x' + gif_height,
                arg=result['embed_url'],
                valid=True,
                icon='giphy_logo.png')

    # Add fallback
    wf.add_item(title='Search on Giphy.com',
            subtitle='Open search in browser',
            arg='searchongiphy:'+ re.sub(r"\s+",'-',re.sub(r"[^\w\s-]",'',query)),
            valid=True,
            icon='giphy_search.png')


def search_query():
    """Actually perform a search with the current query and search limit"""
    
    return search(current_query,search_limit)


def main(wf):
    # Get args and query from Workflow as normalized Unicode
    args = wf.args
    global current_query
    current_query = unicodedata.normalize('NFKD',args[0]).encode('ascii','ignore')

    # Get search limit
    global search_limit
    search_limit = os.environ['GIPHY_SEARCH_LIMIT']

    # Cache the query for later
    wf.cache_data('.thecurrentquery', current_query)

    try:
        # Get search results from cache if possible, perform the search otherwise
        search_results = wf.cached_data(current_query, search_query, max_age=CACHE_MAX_AGE)

        # Populate Alfred results
        populate_alfred_results(search_results,current_query)
    except urllib2.URLError, urllib2.HTTPError:
        wf.add_item(title='Error',
                subtitle='Unable to fetch results :-(',
                valid=False,
                icon='giphy_search.png')


    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    wf.magic_prefix = ':'

    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))

