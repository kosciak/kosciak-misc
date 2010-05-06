#!/usr/bin/env python
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
__version__ = "0.3"



import sys
import os

import re


class Stack(object):
    
    def __init__(self):
        self.data = []
    
    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return repr(self.data)
    
    def next(self):
        if not self.data:
            raise StopIteration
        return self.data.pop()
    
    def peek(self, depth=1):
        if not len(self.data) >= depth:
            return None
        return self.data[-depth]
    
    def pop(self):
        return self.data.pop()
    
    def push(self, value):
        self.data.append(value)
        return value


#
#   block elements
#
block_elements = {
    'header':   r'\s*(?P<header_level>=+)\s(?P<header_text>.+?)\s*=*\s*',
    'blank':    r'\s*',
    'hr':       r'\s*-{4,}\s*',
    'pre':      r'\{{3,}\s*',
    'ul':       r'(?P<ul_indent>\s*)\*\s(?P<ul_item>.*)',
    'ol':       r'(?P<ol_indent>\s*)#\s(?P<ol_item>.*)',
    'blockquote': r'(?P<quote_indent>(?:\s*\>)+)\s(?P<quote_text>.*)',
    }

BLOCK_RE = re.compile(
    r'|'.join([r'^(?<!\\)(?P<%s>%s)$' % (name, char) for name, char in block_elements.iteritems()]) + \
    r'|.*')

END_PRE_RE = re.compile(r'^\}{3,}\s*$')


#
#   inline elements
#
inline_elements = {
    'strong':   r'\*',
    'em':       r'(?<!:)/',
    'del':      r'~',
    'code':     r'`',
    'sup':      r'\^',
    'sub':      r',',
    'img':      r'\{{2}(?P<img_src>.+?)(?:\s*\|\s*(?P<img_alt>.+?)\s*)?\}',
    'a':        r'\[{2}(?P<a_href>.+?)(?:\s*\|\s*(?P<a_description>.+?)\s*)?\]',
    }

INLINE_RE = re.compile(
    r'(?<!\\)(?P<nowiki>\{{3}(?P<nowiki_contents>.+?\}*)\}{3})|' + \
    r'(?P<escaped>\\[*/~`^,{[\]\}-]{2}|' +\
                r'^\s*\\[*#=-]\s|' +\
                r'\\&gt;\s|' +\
                r'\\{3,})|' + \
    r'(?P<br>\\{2})\s*|' + \
    r'|'.join([r'(?P<%s>%s{2})' % (name, char) for name, char in inline_elements.iteritems()])
    )


class KoMarParser(object):
    
    def __init__(self):
        self.__inline = Stack()
        self.__block = Stack()
        self.__list_level = Stack()
        self.__quote_level = Stack()
        self.__line_cont = False
    
    
    def parse(self, input, output):
        for line in input:
            line = self.__parse_block(line)
            if line: 
                output.write(line)
                self.__line_cont = not line.endswith('>\n')
        output.write(self.__start())
    
    
    def __escape_html(self, line):
        return line.replace('&', '&amp;') \
                   .replace('<', '&lt;') \
                   .replace('>', '&gt;')
    

    def __replace_inline(self, match):
        name = match.lastgroup
        if name == 'nowiki':
            return '%s' % match.group('nowiki_contents')
        
        if name == 'escaped':
            return match.group('escaped')[1:]
        
        if name == 'br':
            return '<br />\n'
        
        if name == 'img':
            src = match.group('img_src').strip()
            alt = match.group('img_alt')
            if alt:
                return '<img src="%s" alt="%s" />' % (src, alt)
            return '<img src="%s" />' % src
        
        if name == 'a':
            href = match.group('a_href').strip()
            description = match.group('a_description')
            if description:
                description = INLINE_RE.sub(self.__replace_inline, description)
            else:
                description = href
            return '<a href="%s">%s</a>' % (href, description)
        
        if self.__inline.peek() == name:
            return '</%s>' % self.__inline.pop()
        else:
            return '<%s>' % self.__inline.push(name)
    
    
    def __parse_inline(self, text):
        text = self.__escape_html(text)
        return INLINE_RE.sub(self.__replace_inline, text)
    
    
    def __close_inline(self):
        line = ''
        while self.__inline:
            line += '</%s>' % self.__inline.pop()
        
        return line
    
    
    def __start(self, block='blank', indent=None):
        line = ''
        if self.__block.peek() in ('li', 'blockquote'):
            line += self.__close_inline()
        
        if block in ('pre', 'ol', 'ul'):
            while self.__block.peek() in ('p', 'blockquote'):
                line += self.__end()
            if self.__line_cont:
                line += '\n'
        elif block == 'blockquote':
            while not self.__block.peek() in (None, 'blockquote'):
                line += self.__end()
            if self.__line_cont:
                line += '\n'
        elif not block in ('li'):
            while self.__block:
                line += self.__end()
        
        if block == 'blank':
            return line
        if block == 'hr':
            return line + '<hr />\n'
        
        if block in ('ul', 'ol'):
            self.__list_level.push(indent)
        elif block == 'blockquote':
            self.__quote_level.push(indent)
        
        self.__line_cont = False
        return line + '<%s>' % self.__block.push(block)
    
    
    def __end(self):
        line = self.__close_inline()
        
        if self.__block.peek() in ('ol', 'ul'):
            self.__list_level.pop()
        elif self.__block.peek() == 'blockquote':
            self.__quote_level.pop()
        
        self.__line_cont = False
        return line + '</%s>\n' % self.__block.pop()
    
    
    def __parse_block(self, line):
        if self.__block.peek() == 'pre':
            if END_PRE_RE.match(line):
                return self.__end()
            return self.__escape_html(line)
    
        match = BLOCK_RE.match(line)
        name = match.lastgroup
        
        if name == 'pre':
            return self.__start(name) + '\n'
           
        elif name == 'header': 
            text = self.__parse_inline(match.group('header_text'))
            level = min(len(match.group('header_level')), 6)
            
            return self.__start('h%d' % level) + \
                   text + \
                   self.__end()
            
        elif name == 'hr':
            return self.__start(name)
            
        elif name == 'blank':
            return self.__start()
            
        elif name in ('ol', 'ul'):
            item = match.group('ol_item') or match.group('ul_item')
            indent = len(match.group('ol_indent') or match.group('ul_indent') or '')
            line = ''
            
            while self.__list_level.peek() > indent:
                line += self.__end()
            
            if indent > self.__list_level.peek():
                line += self.__start(name, indent) + '\n'
                
            if self.__block.peek() == 'li':
                line += self.__end()
                if not self.__block.peek() == name:
                    line += self.__end()
                    line += self.__start(name, indent) + '\n'
            
            return line + \
                   self.__start('li') + \
                   self.__parse_inline(item)
            
        elif name == 'blockquote':
            line = ''
            text = match.group('quote_text').strip()
            indent = match.group('quote_indent').count('>')
            while self.__quote_level.peek() > indent:
                line += self.__end()
            
            while indent > self.__quote_level.peek():
                level = (self.__quote_level.peek() or 0) + 1
                line += self.__start(name, level)
            
            if self.__line_cont:
                line += ' '    
            
            return line + \
                   self.__parse_inline(text)
            
        else:
            text = line.strip()
            line = ''
            
            if not self.__block:
                line += self.__start('p')
            elif self.__line_cont:
                line += ' '            
            
            return line + \
                   self.__parse_inline(text)


if __name__=="__main__":
    
    HELP = '''KoMar Parser version %s
Usage: komar.py <input> [<output>]
       cat <input> | komar.py [<output>]
       cat <input> | komar.py [<output>]

If no output file is specified standard output stream is used.
''' % __version__

    output = sys.stdout
    
    if sys.stdin.isatty():
        if len(sys.argv) <= 1:
            print HELP
            sys.exit()
        if not os.path.isfile(sys.argv[1]):
            print 'ERROR: Invalid input file'
            sys.exit()
        input = open(sys.argv[1])
        if len(sys.argv) > 2:
            output = open(sys.argv[2], 'w')
    
    else:
        input = sys.stdin
        if len(sys.argv) > 1:
            output = open(sys.argv[1], 'w')

    parser = KoMarParser()    
    parser.parse(input, output)
