#!/usr/bin/python
# encoding: utf-8

import sys

if __name__ == '__main__':
    # Input is the "embed URL" of the chosen GIF
    # embed_url = "{query}"
    embed_url = sys.argv[1]

    # Giphy ID is the last part of the URL after '/'
    giphy_id = embed_url.rsplit('/',1)[-1]	

    sys.stdout.write(giphy_id)

