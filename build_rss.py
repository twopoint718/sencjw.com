import yaml
import hashlib
import time
import sys
from subprocess import *

yaml_file = "posts.yaml"
date_fmt= "%a, %d %b %Y 00:00:00 +0000"
datetime_fmt = "%a, %d %b %Y %H:%M:%S +0000"
ymd_fmt= "%Y-%m-%d"
item_template = """<item>
  <title><![CDATA[%(title)s]]></title>
  <description><![CDATA[%(postbody)s]]></description>
  <link>blog.html#%(ymd_date)s</link>
  <guid>%(guid)s</guid>
  <pubDate>%(date_fmt)s</pubDate>
</item>
"""

header_template = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>sencjw.com - rss feed</title>
<description>recent blog posts from sencjw.com</description>
<link>http://sencjw.com/blog.html</link>
<lastBuildDate>%(build_date)s</lastBuildDate>
<pubDate>%(pub_date)s</pubDate>
"""

foot_template = """</channel>
</rss>
"""

def build_items(outfile):
    with open(yaml_file, "r") as f:
        posts = yaml.load(f.read())
        for post in posts:
            date = post['date']
            post['postbody'] = run_markdown(post['postbody'])
            post['ymd_date'] = date.strftime(ymd_fmt)
            post['date_fmt'] = date.strftime(date_fmt)
            h = hashlib.sha1()
            h.update(post['ymd_date'] + post['title'])
            post['guid'] = h.hexdigest()
            out = item_template % post
            outfile.write(out.encode("utf-8"))

def run_markdown(txt):
    p = Popen("pandoc", shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, close_fds=True)
    p.stdin.write(unicode(txt))
    p.stdin.close()
    output_html = p.stdout.read()
    p.stdout.close()
    return output_html

def build_header(outfile):
    info = dict()
    curr_time = time.strftime(datetime_fmt)
    info['build_date'] = curr_time
    info['pub_date'] = curr_time
    out = header_template % info
    outfile.write(out.encode("utf-8"))

def main():
    f = sys.stdout
    build_header(f)
    build_items(f)
    f.write(foot_template)

if __name__ == "__main__":
    main()
