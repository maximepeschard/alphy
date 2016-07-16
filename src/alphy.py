#!/usr/bin/python
# encoding: utf-8

from workflow import Workflow3, web

GIPHY_API_KEY = "dc6zaTOxFJmzC"     # beta key
GIPHY_API_HOST = "http://api.giphy.com"
GIPHY_GET_ENDPOINT = "/v1/gifs/"
GIPHY_SEARCH_ENDPOINT = "/v1/gifs/search"
CACHE_MAX_AGE = 300  # seconds

GIF_URL = "GIF_URL"
GIPHY_URL = "GIPHY_URL"
BROWSE = "BROWSE"

def get(gif_id, the_workflow):
    """Get metadata about a chosen GIF by providing its ID"""

    # Retrieve the current query from cache
    current_query = the_workflow.cached_data('.thecurrentquery',max_age=0)
    
    # Retrieve the list of results from cache
    search_results = the_workflow.cached_data(current_query,max_age=0)

    # Search the chosen gif (JSON) in the list
    for gif in search_results:
        if gif['id'] == gif_id:
            get_result = gif
            break

    return get_result


def search(query,search_limit):
    """Search GIFs for 'query'

    Search results number is limited by the 'search_limit' parameter
    """

    # Send search request to Giphy API
    url = GIPHY_API_HOST + GIPHY_SEARCH_ENDPOINT
    params = dict(q=query, limit=search_limit, api_key=GIPHY_API_KEY)
    response = web.get(url, params)

    # Throw error if request failed
    response.raise_for_status()

    # Parse response JSON
    result = response.json()
    search_results = result['data']

    return search_results

