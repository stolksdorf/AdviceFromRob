import sys
import tweepy

consumer_token = '5VAX9gC5n7OuyCqKLKVA'
consumer_secret = 's8xrzrlvTKPnJ3v6R9k6UTnGTnAUqxJ3wC1ZWFSRg'
access_key = "18420720-DMID708lIxZfyGu5aTLVnXVanbKnuJxBkPwGZTvuz"
access_secret = "NgDeDar4ZZsfjDwtoZ4YTMM2nSngq0TO2OWxJDHqK4"

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
api.update_status("This is my Second tweet from command line! Woot!")