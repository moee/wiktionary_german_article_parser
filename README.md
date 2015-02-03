# wiktionary_german_article_parser
Q&amp;D python based parser that extracts the articles of German nouns from the public wiktionary dump

How to run
----------

1. download the latest copy of the German wiktionary's dump: curl http://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-meta-current.xml.bz2
2. extract it to data/dewiktionary.xml
3. run python parse.py | tee data/articles.csv

A log of non extractable nouns is stored in data/articles.log

Todo
----

* Look at the log and implement proper handling of special cases (Alternative Schreibweisen, Adjektivische Deklination, ...)
