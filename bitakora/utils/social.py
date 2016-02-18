import tweepy
from django.conf import settings
from bitakora.accounts.models import BitakoraUser as User

def send_to_twitter(obj):
    textua = obj.getTweetText()
    user = User.objects.get(username=settings.BITAKORA_TWITTER_USER)
    access_token = user.social_auth.filter(provider='twitter')[0].extra_data['access_token']

    oauth_token_secret = access_token['oauth_token_secret']                
    oauth_token = access_token['oauth_token']
    auth = tweepy.OAuthHandler(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)
    auth.set_access_token(oauth_token, oauth_token_secret)
    
    #auth = tweepy.OAuthHandler(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)
    #auth.set_access_token(settings.SOCIAL_TWITTER_ACCESS_TOKEN, settings.SOCIAL_TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)  
    api.update_status(status=textua)
    return True