#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Wojciech 'KosciaK' Pietrzok
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = "Wojciech 'KosciaK' Pietrzok (kosciak@kosciak.net)"
__version__ = "0.1"

import os
import sys
import locale
import re
from getpass import getpass
from datetime import datetime
import xmlrpclib


API_URL = 'http://www.blox.pl/xmlrpc'

locale.setlocale(locale.LC_ALL, '')
LANG, ENCODING = locale.getlocale()

ALL = '---ALL---'

HTML_STYLE = '''
    <style>
    </style>'''

HTML_JAVASCRIPT = '''
    <!--<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>-->
    <script>
    </script>'''


HTML_START = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=%(ENCODING)s"/> 
    <title>%(TITLE)s</title>
    %(HTML_STYLE)s
    %(HTML_JAVASCRIPT)s
</head>
<body>
'''

HTML_LIST_ITEM = '\t<li>%(day).2d %(draft)s<a href="%(year)s/%(month).2d/%(url_title)s">%(title)s</a> <a href="%(url)s">&rarr;</a>, %(author)s, %(date)s, [<em>%(category)s</em>]</li>\n'

HTML_POST = '''
<h1>%(draft)s<a href="%(url)s">%(title)s</a></h1>
<div id="blognote_info">
    <span id="blognote_date">%(date)s</span>
    <span id="blognote_author">%(author)s</span>
    <span id="blognote_category">%(category)s</span>
</div>
<div id="blognote_lead">\n%(lead)s\n</div>
<hr />
<div id="blognote_content">\n%(content)s\n</div>
'''

HTML_END = '''
</body>
</html>'''


class Post(object):
    
    __draft_count = 1
    
    def __init__(self, post_info, blog_name):
        self.blog_name = blog_name
        self.id = post_info['postid']
        self.url = post_info['entryUrl']
        print self.url
        self.url_title = self.url[self.url.rfind('/')+1:]
        self.author = post_info['userid']
        self.title = post_info['title'].encode('utf-8')  
        
        self.draft = ''
        if '20null.html' in self.url:
            self.draft = '<strong>[SZKIC!]</strong> '
            self.url_title = 'szkic_%.3d.html' % Post.__draft_count
            Post.__draft_count += 1
        
        self.date = datetime.strptime(post_info['dateCreated'], '%Y-%m-%dT%H:%M:%S')
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        
        post_info = SERVER.metaWeblog.getPost(self.id, LOGIN, PASS)
        
        self.lead = post_info['lead'].encode('utf-8')
        self.content = post_info['description'].encode('utf-8')
        try:
            self.category = post_info['categories'][0].encode('utf-8')
        except IndexError:
            self.category = '-brak-'
        
        # TODO: Blox tags
        
        self.img_re = re.compile('<img [^>]*?src=[\'"]?([^\'" ]+)')
        self.link_re = re.compile('<a [^>]*?href=[\'"]?((?:http://%s.blox.pl)?/resource/[^\'" ]+)' % blog_name)

    
    
    def archive(self, path):
        year_path = os.path.join(path, self.blog_name, str(self.year))
        if not os.path.exists(year_path):
            os.mkdir(year_path)
        month_path = os.path.join(year_path, '%.2d' % self.month)
        if not os.path.exists(month_path):
            os.mkdir(month_path)
        post_path = os.path.join(month_path, self.url_title)
        post_index = open(post_path, 'w')
        global TITLE
        TITLE = self.title
        post_index.write(HTML_START % globals())
        post_index.write(HTML_POST % self)
        post_index.write(HTML_END)
    
    
    @property
    def files(self):
        files = self.img_re.findall(self.lead) + self.img_re.findall(self.content) + \
                self.link_re.findall(self.lead) + self.link_re.findall(self.content)
        return files
    
    
    def __getitem__(self, key):
        return self.__getattribute__(key)



def export_blog(blog_name, blog_id):
    print "Pobieram blog %s" % blog_name
    path = os.getcwd()
    blog_path = os.path.join(path, blog_name)
    if not os.path.exists(blog_path):
        os.mkdir(blog_path)
    
    resources = open(os.path.join(path, blog_name, 'resources.txt'), 'w')
    resources.write('#\n#\twget -i resources.txt -P resource\n#\n\n')
    
    index = open(os.path.join(path, blog_name, 'index.html'), 'w')
    global TITLE
    TITLE = blog_name
    index.write(HTML_START % globals())
    
    posts = SERVER.mt.getRecentPostTitles(blog_id, LOGIN, PASS, -1)
    posts.reverse()
    
    prev_year = 0
    prev_month = 0
    for post in posts:
        post = Post(post, blog_name)
        year_changed = False
        if not post.year == prev_year:
            if prev_year is not 0:
                index.write('</ul>\n')
            prev_year = post.year
            year_changed = True
            index.write('<h2>%s</h2>\n' % post.year)
        if not post.month == prev_month:
            if prev_month is not 0 and not year_changed:
                index.write('</ul>\n')
            prev_month = post.month
            index.write('<h3>%d-%.2d</h3>\n' % (post.year, post.month))
            index.write('<ul>\n')
        
        index.write(HTML_LIST_ITEM % post)
        
        post.archive(path)
        
        files = post.files
        if files:
            resources.write('#' + post.url + '\n')
            for file in files:
                resources.write(file + '\n')
            resources.write('\n')
    
    index.write('</ul>')
    index.write(HTML_END)



def check_blogs(choosen_blog=None):
    try:
        blogs = SERVER.blogger.getUsersBlogs('', LOGIN, PASS)
    except xmlrpclib.Fault, fault:
        if 'Invalid user' in fault.faultString:
            print "BŁĄD! Niepoprawny login lub hasło!"
        else:
            print "Nastąpił nieoczekiwany błąd."
        sys.exit()
    
    for blog in blogs:
        blog_id = blog['blogid']
        blog_name = blog['blogName']
        if not choosen_blog:
            answer = raw_input('Pobrać blog %s? (tak/nie)\n' % blog_name)
            if answer.lower() in ['t', 'tak']:
                export_blog(blog_name, blog_id)
        elif blog_name == choosen_blog:
            export_blog(blog_name, blog_id)
            break
        elif choosen_blog == ALL:
            export_blog(blog_name, blog_id)


if __name__ == '__main__':
    
    HELP = '''Użycie: blox-exporter.py [opcje]
Przykład: blox-exporter.py -L login -P hasło -B blog1

Opcje:
  -H, --help             Pokaż pomoc i zakończ działanie
  -V, --version          Pokaż wersję skryptu
  -L, --login <login>    Login dla blox.pl
  -P, --password <hasło> Hasło dla blox.pl
  -A, --all              Pobierz wszystkie blogi
  -B, --blog <blog>      Nazwa bloga do pobrania
''' 
    
    print "blox-exporter %s" % __version__
        
    global SERVER, LOGIN, PASS
    choosen_blog = None
    LOGIN = None
    PASS = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ['-H', '--help']:
            print HELP
            sys.exit()
        if arg in ['-V', '--version']:
            sys.exit()
        
        if arg in ['-L', '--login']:
            try:
                LOGIN = sys.argv[i+1]
            except:
                print "BŁĄD! Nie podałeś loginu"
            i += 1
        elif arg in ['-P', '--password']:
            try:
                PASS = sys.argv[i+1]
            except:
                print "BŁĄD! Nie podałeś hasła"
            i += 1
        elif arg in ['-A', '--all']:
            choosen_blog = ALL
        elif arg in ['-B', '--blog']:
            try:
                choosen_blog = sys.argv[i+1]
            except:
                print "BŁĄD! Nie podałeś nazwy blogu"
            i += 1
            
        i += 1

    if not LOGIN:
        LOGIN = raw_input("Login: ")
    if not PASS:
        PASS = getpass("Hasło: ")
    
    SERVER = xmlrpclib.ServerProxy(API_URL)
    
    check_blogs(choosen_blog)
