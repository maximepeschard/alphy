#!/usr/bin/python
# encoding: utf-8

import sys
import os

from workflow import Workflow3 
from alphy import get, GIF_URL, GIPHY_URL, BROWSE

log = None


def main_giphy(wf):
    """Get Giphy URL"""

    # Get args from Workflow as normalized Unicode
    args = wf.args

    # Get GIF metadata
    gif = get(args[0],wf)
    # Extract Giphy URL from JSON
    giphy_url = gif['url']

    # Send output to Alfred
    sys.stdout.write(giphy_url)


def main_gif(wf):
    """Get GIF URL"""

    # Get args from Workflow as normalized Unicode
    args = wf.args

    # Get GIF metadata
    gif = get(args[0],wf)
    # Extract GIF URL from JSON
    gif_url = gif['images']['original']['url']

    # Send output to Alfred
    sys.stdout.write(gif_url)


if __name__ == '__main__':
    wf = Workflow3()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger

    # Second argument indicates the action chosen :
    # 'GIF_URL' (default), 'GIPHY_URL', 'BROWSE'
    action = os.environ['action']

    if action == GIPHY_URL or action == BROWSE:
        sys.exit(wf.run(main_giphy))
    else:
        sys.exit(wf.run(main_gif))

