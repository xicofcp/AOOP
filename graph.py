import json
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import numpy as np
from matplotlib import style

style.use('ggplot')

tweets_data_path = 'mou.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

commentSeries = tweets['text']
comments = np.array([unicodedata.normalize('NFKD', commentSeries[k]).encode('ascii','ignore') for k in range(len(commentSeries))])

counts = np.char.count(comments, "mourinho")
maxCount = max(np.cumsum(counts))
label = "mourinho" + ": " + str(maxCount)
plt.plot(np.cumsum(counts), label=label)
plt.legend(loc=2)
plt.show()
