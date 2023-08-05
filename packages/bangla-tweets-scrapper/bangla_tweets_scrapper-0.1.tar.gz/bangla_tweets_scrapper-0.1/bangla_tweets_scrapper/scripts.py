from tweets import get_tweets_context
a=get_tweets_context('জন্য')
print(a[1])
import json
b=json.loads(open('output.json',encoding='utf-8').read())
