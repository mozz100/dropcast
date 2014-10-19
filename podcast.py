#!/usr/bin/env python
# Usage: ./podcast.py <base_url> <title> <description>
# e.g. ./podcast.py 'https://dl.dropbox.com/u/1234567' 'My podcast' 'Created with dropcast'

import fnmatch, os, sys, urllib, time, hashlib, mutagen
from os.path import getsize
from urllib2 import quote
from datetime import datetime
from email.utils import formatdate  # for RFC 2822 formatting

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
  """ % (DESCRIPTION, BASE_URL, PODCAST_TITLE, formatdate())

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
      # Can we get Album, Title, Comment?

      pubDate = formatdate(os.path.getctime(filename))  # Base pubDate on create date of file.  Imperfect.
      guid = hashlib.md5()
      guid.update(title)
      guid.update(pubDate)

      from mutagen.mp4 import MP4
      if filename.endswith(".m4a"):
        audio = MP4(filename)
        album = audio['\xa9alb'][0].replace('&','&amp;')   # program name *used
        lyrics = audio['\xa9lyr'][0].replace('&','&amp;')  # detailed notes * used
        artist = audio['\xa9ART'][0].replace('&','&amp;')  # radio station * used
        pubDate  = datetime.strptime(audio['\xa9day'][0][0:19], '%Y-%m-%dT%H:%M:%S')  # broadcast date, eg 2014-09-18T23:00:00+01:00 TODO parse timezone
        comment = audio['\xa9cmt'][0].replace('&','&amp;') # comment
        track_title = audio['\xa9nam'][0].replace('&','&amp;') # episode name  * used
        title = album + ' - ' + track_title
        feed += """<item>
                  <title>%s</title>
                  <link>%s</link>
                  <guid>%s</guid>
                  <pubDate>%s</pubDate>
                  <itunes:author>%s</itunes:author>
                  <itunes:summary>%s</itunes:summary>
                  <enclosure type="%s" length="%s" url="%s"/>
                  </item>""" % (title, link, guid.hexdigest(), pubDate, artist, lyrics, enctype, size, link)  
      else:
        feed += """<item>
                  <title>%s</title>
                  <link>%s</link>
                  <guid>%s</guid>
                  <pubDate>%s</pubDate>
                  <enclosure type="%s" length="%s" url="%s"/>
                  </item>""" % (title, link, guid.hexdigest(), pubDate, enctype, size, link)  

  feed_data = feed_template.replace('<!--data-feed -->',feed)
  f = open("feed.xml", 'w')
  f.write(feed_data)
  f.close()

if __name__ == '__main__':
  main()
