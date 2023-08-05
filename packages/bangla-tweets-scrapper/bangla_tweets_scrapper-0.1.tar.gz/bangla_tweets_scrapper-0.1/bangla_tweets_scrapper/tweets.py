import json
import sys
import tweepy
from collections import defaultdict
from argparse import ArgumentParser
from decouple import config
consumer_key=config('consumer_key',default='')
consumer_secret=config('consumer_secret',default='')
access_token=config('access_token',default='')
access_token_secret=config('access_token_secret',default='')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


def get_tweets_context(data,*self,**kwargs):
    #Get all tweets context by using a keyword
    tweets= api.search(data,lang="bn",count=200)
    all_tweets=[]
    for tweet in tweets:
      if tweet.in_reply_to_status_id_str == None:
        all_tweets.append(tweet)
    return all_tweets
def get_tweets_text(data,*args,**kwargs):
    #Get all tweets text by using a keyword
    tweets= api.search(data,lang="bn",count=200)
    all_tweets=[]
    for tweet in tweets:
      if tweet.in_reply_to_status_id_str == None:
        all_tweets.append(tweet.text)
    return all_tweets

def get_tweets_from_user(screen_name,*args,**kwargs):
    #Get all tweets of a particular user by using username
    all_tweets=[]
    new_tweets=api.user_timeline(screen_name=screen_name,count=200)
    print("Newly Collected: ",len(new_tweets))
    all_tweets.extend(new_tweets)
    oldest=all_tweets[-1].id -1
    while len(new_tweets)>0:
        new_tweets=api.user_timeline(screen_name=screen_name,count=200,max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest=all_tweets[-1].id -1
        print("Collected tweets: ",len(all_tweets))
    print("Total Collected tweets: ",len(all_tweets))
    return all_tweets
def get_banglatweets_by_country(country_name,*args,**kwargs):
    #Get all tweets of a particular contry by using country name
    places=api.geo_search(query=country_name,granularity="country")
    place_id=places[0].id
    tweets=api.search(q="place:%s" % place_id,lang='bn')
    all_tweets=[]
    for tweet in tweets:
      if tweet.in_reply_to_status_id_str == None:
        all_tweets.append(tweet)
        print(tweet.text+" | "+tweet.place.name if tweet.place else "Undefined Place")
    return all_tweets

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-m", "--method")
    parser.add_argument("-d", "--data")
    # parser.add_argument("filename")
    args = vars(parser.parse_args())
    function=getattr(sys.modules[__name__], args['method'])
    data=args['data']
    output=function(data)
    if args['method']=='get_tweets_text':
        fname='tweets_texts.txt'
        with open(fname, "w",encoding='utf-8') as f:
            for item in output:
                f.write("%s\n" % item)
            f.close()
    elif args['method']=='get_tweets_context':
        fname='tweets_contexts.json'
        with open(fname, "w",encoding='utf-8') as f:
            for item in output:
                json.dump(item._json,f,sort_keys=True,indent=4)
            f.close()
    elif args['method']=='get_banglatweets_by_country':
        fname='tweets_contexts_of_country.json'
        with open(fname, "w",encoding='utf-8') as f:
            for item in output:
                json.dump(item._json,f,sort_keys=True,indent=4)
            f.close()
    else:
        fname='tweets_contexts_of_user.json'
        with open(fname, "w",encoding='utf-8') as f:
            for item in output:
                json.dump(item._json,f,sort_keys=True,indent=4)
            f.close()
