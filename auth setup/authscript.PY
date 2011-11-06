#!/usr/bin/env python

import tweepy

filename = "auth_url.txt"
filename2 = "auth_access.txt"

CONSUMER_KEY = '5VAX9gC5n7OuyCqKLKVA'
CONSUMER_SECRET = 's8xrzrlvTKPnJ3v6R9k6UTnGTnAUqxJ3wC1ZWFSRg'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url

#Write to a file
FILE = open(filename,"w")
FILE.write("URL: " + auth_url + "\n\n")
FILE.close()


verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret

FILE = open(filename2,"w")
FILE.write("access Key: " + auth.access_token.key + "\n")
FILE.write("access Secret: " + auth.access_token.secret)

FILE.close()