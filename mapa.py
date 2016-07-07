import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import numpy as np
from matplotlib import style
import datetime as dt
import json
import matplotlib.animation as animation
import time

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
tweets['location'] = list(map(lambda tweet: tweet['user']['location'], tweets_data))
tweets['country_code'] = list(map(lambda tweet: tweet['place']['country_code'] if tweet['place'] != None else '', tweets_data))
tweets['long'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][0] if tweet['coordinates'] != None else 'NaN', tweets_data))
tweets['latt'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][1] if tweet['coordinates'] != None else 'NaN', tweets_data))
 
from mpl_toolkits.basemap import Basemap
 
# plot the blank world map
my_map = Basemap(projection='merc', lat_0=50, lon_0=-100,
                     resolution = 'l', area_thresh = 5000.0,
                     llcrnrlon=-140, llcrnrlat=-55,
                     urcrnrlon=160, urcrnrlat=70)
# set resolution='h' for high quality
 
# draw elements onto the world map
my_map.drawcountries()
#my_map.drawstates()
my_map.drawcoastlines(antialiased=False,
                      linewidth=0.005)
 
# add coordinates as red dots
longs = list(tweets.loc[(tweets.long != 'NaN')].long)
latts = list(tweets.loc[tweets.latt != 'NaN'].latt)
x, y = my_map(longs, latts)
my_map.plot(x, y, 'ro', markersize=6, alpha=0.5)

plt.title('Mapa Tweets')
plt.grid()
plt.savefig('mapa.png', dpi=300)
