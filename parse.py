# -*- coding: utf-8 -*-

import re
import codecs
import sys
from xml.sax import make_parser, handler

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def add_to_unkown_log(noun):
    with codecs.open('data/unkown.log', 'a', 'utf-8') as f:
        f.write("=======\n")
        f.write(noun.title + "\n")
        f.write(noun.text + "\n")

class Noun:
    def __init__(self):
        self.title = ""
        self.gender = ""
        self.namespace = ""
        self.text = ""

    def is_german_noun(self):
        return "{{Wortart|Substantiv|Deutsch}}" in self.text

    def article(self):
        try:
            raw = re.search(r'Nominativ Singular( \d)?=(.*?)( |<)', self.text).group(2)
            return raw.replace("(", " ").replace(")", " ").replace(" ", "")
        except:
            add_to_unkown_log(self)
            return "??"

class DeWiktionaryXmlHandler(handler.ContentHandler):
    def __init__(self):
        self.noun = Noun()
        self.content = ""

    def characters(self, content):
        self.content += content.strip()

    def startElement(self, name, attrs):
        self.content = ""

    def endElement(self, name):
        if name == "ns":
            self.noun.namespace = int(self.content)

        if name == "title":
            self.noun.title = self.content

        if name == "text":
            self.noun.text = self.content

        if name == "page":
            if self.noun.namespace is 0 and self.noun.is_german_noun():
                print "%s,%s" % (self.noun.title, self.noun.article())
                self.noun = Noun()

        self.content = ""

parser = make_parser()
b = DeWiktionaryXmlHandler()
parser.setContentHandler(b)
parser.parse("data/dewiktionary.xml")
