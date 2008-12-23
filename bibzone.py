#!/usr/bin/env python

import sys
import os.path
from pyaws import ecs
"""
http://pyaws.sf.net
"""

__version__ = "0.2"


def main():
    from optparse import OptionParser
    cmnd = os.path.basename(sys.argv[0])
    
    parser = OptionParser(version="%prog "+__version__)

    parser.add_option("-k", "--awskey", dest="awskey", help="specify your AWS-key")
    parser.add_option("-a", "--author", dest="author", help="search by Author")
    parser.add_option("-t", "--title", dest="title", help="search by Title")
    parser.add_option("-i", "--isbn", dest="isbn", help="search by ISBN")
    parser.add_option("-c", "--count", dest="count", help="show this number of items")
    parser.add_option("-l", "--language", default="us", metavar="LOCALE", 
                      help="search language: fr, ca, de, jp, us, "
                      "or uk [default: %default]")

    (options, args) = parser.parse_args()

    if options.awskey:
        ecs.setLicenseKey(options.awskey)
    else:
        print "You have to specify an AWS key!"
        print "Get one at: http://aws.amazon.com"
        print "run", cmnd, "--help for additional help"
        sys.exit(1)

    try:
        ecs.setLocale(options.language)
    except ecs.BadLocale:
        ecs.setLocale("us")

    if options.count:
        count = int(options.count)
    else:
        count = 20

    # options are mutually exclusive. isbn >> titel >> author
    if options.isbn:
        books = ecs.ItemLookup(ItemId=options.isbn, IdType='ISBN', SearchIndex='Books', 
                              ResponseGroup="Medium")
    elif options.title:
        books = ecs.ItemSearch('', SearchIndex='Books', Title=options.title,
                               ResponseGroup="Medium")
    elif options.author:
        books = ecs.ItemSearch('', SearchIndex='Books', Author=options.author,
                              ResponseGroup="Medium")
    else:
        print "You have to specify a search query!"
        print "run", cmnd, "--help for additional help"
        sys.exit(1)

    if len(books) == 0:
        print "Sorry, nothing found"
        sys.exit(0)

    count = min(count, len(books))

    #print dir(books[0])
    #sys.exit(0)

    for i in range(count):
        print "%d) %s" % (i+1,  books[i].Title)
        if type(books[i].Author) == list:
            print "\tby ", " and ".join(books[i].Author)
        else:
            print "\tby %s" % (books[i].Author)

    itemnumber = int(raw_input("Which item do you want? "))
    itemnumber -= 1

    if type(books[itemnumber].Author) == list:
        author = " and ".join(books[itemnumber].Author)
        author = author.strip()
    else:
        author = books[itemnumber].Author.strip()

    author_lastname = author.split()[-1] # last author wins
    title = books[itemnumber].Title.strip()
    publisher = books[itemnumber].Publisher.strip()
    year = books[itemnumber].PublicationDate.strip().split('-')[0]
    isbn = books[itemnumber].ISBN.strip()


    # output entry:
    print "BibTex-entry:"
    print "@book{%s%s," % (author_lastname.lower()[:3], year[2:])
    print '   author = "%s",' % (author)
    print '   title = "%s",' % (title)
    print '   publisher = "%s",' % (publisher)
    print '   year = "%s",' % (year)
    print '   isbn = "%s"' % (isbn)
    print "}"

if __name__ == "__main__":
    main()
