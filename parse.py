# -*- coding: utf-8 -*-

import re
import codecs
import sys
import sqlite3
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
            return raw.replace("(", " ").replace(")", " ").replace(" ", "").lower()
        except:
            add_to_unkown_log(self)
            return "??"

class DeWiktionaryXmlHandler(handler.ContentHandler):
    def __init__(self, db):
        self.noun = Noun()
        self.content = ""
        self.word_id = 0
        self.db = db
        c = db.cursor()
        c.execute("DROP TABLE words")
        c.execute('''CREATE TABLE words
                     (_id integer primary key, article text, word text)''')

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
            if self.noun.namespace is 0 and self.noun.is_german_noun() and self.noun.article() in ["der", "die", "das"]:
                self.word_id += 1
                self.db.execute("INSERT INTO words (_id, word, article) VALUES (?, ?, ?)", (self.word_id, self.noun.title, self.noun.article()))
                print "%d,%s,%s" % (self.word_id, self.noun.title, self.noun.article())
                self.noun = Noun()

        self.content = ""

output_db = "./data/articles.db"
conn = sqlite3.connect(output_db)
parser = make_parser()
b = DeWiktionaryXmlHandler(conn)
parser.setContentHandler(b)
output_db = "./data/articles.db"
parser.parse("data/dewiktionary.xml")
conn.commit()
