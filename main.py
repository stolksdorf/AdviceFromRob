from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
  import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache


from google.appengine.ext.webapp import util

import urllib2
import sys
import tweepy
import logging

consumer_token = '5VAX9gC5n7OuyCqKLKVA'
consumer_secret = 's8xrzrlvTKPnJ3v6R9k6UTnGTnAUqxJ3wC1ZWFSRg'


access_key = '236067505-XctaSAfX7VMHle6w6zLNyXkBhT9BaWwzTGHZ3yt8'
access_secret = 'f6ErGFeoGcKWgKo1vqu3Lzb8YDCUaOK5CelDIf9nqM'

#Check out booleans for the morning
class AdviceTweets(db.Model):
	advice = db.StringProperty(required=True)
	
class SentTweets(db.Model):
	advice = db.StringProperty(required=True)
	dateTweeted = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
		
	def get(self):		
		pre_tweets = db.GqlQuery('SELECT * FROM AdviceTweets')
		post_tweets = db.GqlQuery('SELECT * FROM SentTweets ORDER BY dateTweeted DESC')
		values = {	'pre_tweets':pre_tweets, 
					'post_tweets':post_tweets
				}
		self.response.out.write(template.render('main.html', values))
		
	def post(self):
		tempTweets = self.request.get('adviceTweet')
		tempTweets = tempTweets.split('\n')
		for tweet in tempTweets:	
			if tweet != "":
				adviceTweet = AdviceTweets(advice = tweet )
				adviceTweet.put()
		self.redirect('/')
		
		
		
class Cron(webapp.RequestHandler):
	def get(self):
		tweet_to_send = db.GqlQuery('SELECT * FROM AdviceTweets LIMIT 1')
		for tweet in tweet_to_send:
			tweet_to_add = SentTweets(advice=tweet.advice)
			tweet_to_add.put()
			PublishTweet(tweet.advice)
			tweet.delete()
		#Send email if there are no more rob tweets left
		tweets_left = db.GqlQuery('SELECT * FROM AdviceTweets')
		if tweets_left.count() == 0:
			mail.send_mail(sender="theTweetBaron@advicefromrob.appspotmail.com",
              to="ekmccann@uwaterloo.ca",
              subject="Your Tweets are running low!",
              body= "Right now there's currently no advice for Rob to dispense. Be sure to rectify this situation!")
		
##### Creates Page where the user can store the request token and provides a link to authorize
class CreateAuth(webapp.RequestHandler):
	def get(self):
		#create the auth object and get the auth url
		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
		auth_url = auth.get_authorization_url()
		
		#extract out the request token, and have the user store it, then click the URL
		request_key = auth.request_token.key
		request_secret = auth.request_token.secret
			
		values = {	'auth_url':auth_url,
					'request_key':request_key,
					'request_secret':request_secret
				}
		self.response.out.write(template.render('create_auth.html', values))
	
#### Callback from the auth url, provides a verifier. This will produce the access token
class SetAuth(webapp.RequestHandler):
	def get(self):
		#After the user clicks the allow we'll get a verifier
		#Have the user input in the verifier and the request toekn we had them store earlier
		request_verifier= self.request.get('oauth_verifier')		
		values = {'verifier':request_verifier }
		self.response.out.write(template.render('set_auth.html', values))
		
	def post(self):
		#pull out the request token and the verifier
		request_key = self.request.get('request_key') 
		request_secret = self.request.get('request_secret') 
		verifier = self.request.get('verifier') 
		
		#create the auth object and set the request token in it
		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)		
		auth.set_request_token(request_key, request_secret)
		
		#Use the verifier to get the access token
		auth.get_access_token(verifier)
		
		#Display it!
		access_key = auth.access_token.key
		access_secret = auth.access_token.secret
		
		values = {	'access_key': access_key,
					'access_secret': access_secret
				}
		self.response.out.write(template.render('set_auth.html', values))		
		
				
def PublishTweet(tweet):
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	api.update_status(tweet)
	
		

application = webapp.WSGIApplication(
                                     [									 
									 ('/cron', Cron),
									 ('/create',CreateAuth),
									 ('/auth', SetAuth),
									 ('/', MainPage)
									 ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()