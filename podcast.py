#!/usr/bin/env python
# Usage: ./podcast.py <base_url> <title> <description>
# e.g. ./podcast.py 'https://dl.dropbox.com/u/1234567' 'My podcast' 'Created with dropcast'

import fnmatch, os, sys, urllib
from os.path import getsize
from urllib2 import quote
from datetime import datetime

BASE_URL, PODCAST_TITLE, DESCRIPTION = sys.argv[1:4]
MATCHES = {
  '*.mp3': 'audio/mpeg',
  '*.m4a': 'audio/x-m4a',
}

# Standardise BASE_URL by removing any / from the end
while BASE_URL.endswith("/"):
  BASE_URL=BASE_URL[0:-1]

feed_template = """<?xml version="1.0" encoding="ISO-8859-1"?>
  <rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
    <channel>
      <description>%s</description>
      <link>%s/feed.xml</link>
      <title>%s</title>
      <pubDate>%s</pubDate>
        <!--data-feed -->
    </channel>
  </rss>
  """ % (DESCRIPTION, BASE_URL, PODCAST_TITLE, datetime.now())

def main():

  feed = ''
  for dirname, dirnames, files in os.walk('.'):
    dirname_enc = urllib.quote(dirname[2:].replace(u'\\', u'/'))
    for filename in files:

      # compare filename against all entries in MATCH
      match = False
      for s in MATCHES.keys():
        if fnmatch.fnmatch(filename, s):
          match = s
          break
      if not match:
        # move on to the next file
        continue

      # filename matches so make entry in xml string
      media_url = quote(filename)
      title = filename.replace('&','&amp;')
      size = getsize(os.path.join(dirname, filename))

      link = os.path.join(BASE_URL, dirname_enc, media_url)
      enctype = MATCHES[match]

      # TODO more metadata.  See https://www.apple.com/uk/itunes/podcasts/specs.html#rss
      # In particular, GUID should probably relate to the file, and can we get
      # pubDate?

      feed += """<item>
                  <title>%s</title>
                  <link>%s</link>
                  <enclosure type="%s" length="%s" url="%s"/>
                  </item>""" % (title, link, enctype, size, link)  

  feed_data = feed_template.replace('<!--data-feed -->',feed)
  f = open("feed.xml", 'w')
  f.write(feed_data)
  f.close()

if __name__ == '__main__':
  main()
