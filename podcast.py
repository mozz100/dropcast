import fnmatch, os, urllib
from os.path import join, getsize

DROPBOX_ID = '' # you dropbox ID, like 1111111
BASE_URL = 'http://dl.dropbox.com/u/%s/' % (DROPBOX_ID)

template_head = '\
<?xml version="1.0" encoding="ISO-8859-1"?>\
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">\
<channel>\
<description>Dropcast</description>\
<link>%s</link>\
  <title>My dropcast</title>\
<pubDate> Wed, 21 Apr 2010 10:35:02 +0200 </pubDate>\
' % BASE_URL

def main():

  items = ''
  for dirname, dirnames, files in os.walk('.'):
    dirname_enc = urllib.quote(dirname[2:].replace(u'\\', u'/'))
    for mp3_url, title, size in [(urllib.quote(filename), filename, getsize(join(dirname, filename)) ) for filename in files if fnmatch.fnmatch(filename, '*.mp3')]:
      link = '%s%s/%s' % (BASE_URL, dirname_enc, mp3_url)
      items += '<item>\n\
      <title>%s</title>\n\
      <link>%s</link>\n\
      <enclosure type="audio/mpeg" length="%s" url="%s"/>\
      </item>\n' % (title, link, size, link)  

  content = '%s\n%s\n</channel></rss>' % (template_head, items)
  f = open("feed.xml", 'w')
  f.write(content)
  f.close()

if __name__ == '__main__':
  main()