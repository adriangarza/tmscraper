# usage: tmscraper.py [URL] [NUM_TRACKS]

import argparse
import urllib.request
from html.parser import HTMLParser
import re

parser = argparse.ArgumentParser(description="Scrape mania-exchange track files.")
parser.add_argument('target', type=str, help="The URL to scrape tracks from (e.g. https://tm.mania-exchange.com/tracksearch2?mode=5&priord=8 or https://united.tm-exchange.com/main.aspx?action=tracksearch&mode=8). Make sure it's in quotes.")
parser.add_argument("num_tracks", type=int, help="The number of tracks to download from the page.")

args = parser.parse_args()

"""
So the page link looks like this:
    https://tm.mania-exchange.com/tracksearch2?mode=5&priord=8
But the actual table is fetched on load, via this url:
    https://tm.mania-exchange.com/tracksearch2/search?mode=5&priord=8

So we need to add "/search" before "?mode" in the url
"""
insert_pos = args.target.index("?mode")

actual_url = args.target[:insert_pos] + "/search" + args.target[insert_pos:]

the_page = ""
req = urllib.request.Request(actual_url)
with urllib.request.urlopen(req) as response:
    for line in response:
        the_page += line.decode('utf8')

# create a subclass and override the handler methods
"""
We want an <a> with href="/tracks/download/some_digits"
Unfortunately the title is contained in a slightly different link:
    "/tracks/trackID/title"
""" 
download_links = []

def format_dl(link):
    # the link is given as /tracks/NUMBERS/TITLE
    # we want /tracks/download/136538
    linklist = link.split('/')
    # the first element of the list is an empty string
    return "https://tm.mania-exchange.com"+"/tracks/download/"+str(linklist[2])

def format_name(link):
    # the link is given as /tracks/NUMBERS/TITLE
    # we want TITLE
    return link.split('/')[3]

# create a very sloppy HTML parser to grab the links
class NewHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            # get the link href
            tag_link = ""
            for name, val in attrs:
                if name == 'href':
                    tag_link = val

            # we want the track link with the names
            if re.match('^/tracks/\d+/.+$', tag_link):
                download_links.append({
                    "dl": format_dl(tag_link),
                    "title": format_name(tag_link) 
                    })

parser = NewHTMLParser()
parser.feed(the_page)

# cut the list to the specified number
download_links = download_links[:args.num_tracks]

#then download the actual tracks
counter = 0
for link in download_links:
    counter += 1
    print("Downloading track {}: {}".format(counter, link["title"]))
    urllib.request.urlretrieve(link["dl"],'{}.Map.gbx'.format(link["title"]))

print("done!")
