import json
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
import time
import seaborn as sns
from mpltools import style
from matplotlib import rcParams
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#graphic styles
sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (8, 4)})
style.use('ggplot')
rcParams['axes.labelsize'] = 9
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 7
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = False
rcParams['figure.figsize'] = 20, 10

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

def plot_tweets_per_category(category, title, x_title, y_title, top_n=5, output_filename="plot.png"):
    tweets_by_cat = category.value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x')
    ax.tick_params(axis='y')
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(title)
    tweets_by_cat[:top_n].plot(ax=ax, kind='bar')
    fig.savefig(output_filename)

def plot_distribution(category, title, x_title, y_title, output_filename="plot.png"):
    fig, ax = plt.subplots()
    ax.tick_params(axis='x')
    ax.tick_params(axis='y')
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(title)
    sns.distplot(category.values, rug=True, hist=True);
    fig.savefig(output_filename)

def main():


	#Read Tweets
	print 'Reading Tweets\n'
	tweets_data_path = 'mou.txt'

	tweets_data = []
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
	    try:
	        tweet = json.loads(line)
	        tweets_data.append(tweet)
	    except:
	        continue

	#Structuring Tweets
	print 'Structuring Tweets\n'
	tweets = pd.DataFrame()
	# We want to know when a tweet was sent
	tweets['created_at'] = map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), tweets_data)
	# Who is the tweet owner
	tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], tweets_data)
	# How many follower this user has
	tweets['user_followers_count'] = map(lambda tweet: tweet['user']['followers_count'], tweets_data)
	# What is the tweet's content
	tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), tweets_data)
	# If available what is the language the tweet is written in
	tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
	# If available, where was the tweet sent from ?
	tweets['Location'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
	# How many times this tweet was retweeted and favorited
	tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], tweets_data)
	tweets['favorite_count'] = map(lambda tweet: tweet['favorite_count'], tweets_data)

	tweets['chelsea'] = tweets['text'].apply(lambda tweet: word_in_text('chelsea', tweet))
	tweets['arsenal'] = tweets['text'].apply(lambda tweet: word_in_text('arsenal', tweet))
	tweets['manchester'] = tweets['text'].apply(lambda tweet: word_in_text('manchester', tweet))
	
	
	#Tweets by language
	plot_tweets_per_category(tweets['lang'], 
			 "#MouTweets by Language", 
                         "Language", 
                         "Number of Tweets", 
                         5,
                         "Mou_tweets_per_language.png")

	#Tweets by Country
	plot_tweets_per_category(tweets['Location'], 
                         "#MouTweets by Location", 
                         "Location", 
                         "Number of Tweets", 10,
                         "Mou_tweets_per_location.png")


	#Tweets by user
	plot_tweets_per_category(tweets['user'], 
                         "#Tweets active users", 
                         "Users", 
                         "Number of Tweets", 20,
                         "Mou_tweets_users.png")

	#Number of retweets by user
	plot_distribution(tweets['Location'].value_counts(), 
		          "#MouTweets retweets distribution", "", "",
		          "Mou_retweets_distribution.png")

	

	#Word Cloud 
	text = " ".join(tweets['text'].values.astype(str))

	maskCloud = imread("twitter_mask.png", flatten=True)
	no_urls_no_tags = " ".join([word for word in text.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                            ])
	wordcloud = WordCloud(
                      stopwords=STOPWORDS,
                      background_color='white',
                      width=1800,
                      height=1400,
                      mask=maskCloud
            ).generate(no_urls_no_tags)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.savefig('cloudmourinho.png', dpi=300)

	
	# tweets with clubs	
	teams = ['chelsea', 'arsenal', 'manchester']
	tweets_by_teams = [tweets['chelsea'].value_counts()[True], tweets['arsenal'].value_counts()[True], tweets['manchester'].value_counts()[True]]

	x_pos = list(range(len(teams)))
	width = 0.8
	fig, ax = plt.subplots()
	plt.bar(x_pos, tweets_by_teams, width, alpha=1, color='g')

	# Setting axis labels and ticks
	ax.set_ylabel('Number of tweets', fontsize=15)
	ax.set_title('Ranking: chelsea vs. arsenal vs. manchester united (Raw data)', fontsize=10, fontweight='bold')
	ax.set_xticks([p + 0.4 * width for p in x_pos])
	ax.set_xticklabels(teams)
	plt.grid()
	plt.savefig('clubs.png', dpi=300)


	cols = ['c','m','r']

	plt.pie(tweets_by_teams,
		labels = teams,
		colors=cols,
		autopct='%1.1f%%')

	plt.title('Ranking: chelsea vs. arsenal vs. manchester united (Raw data)')
	plt.grid()
	plt.savefig('pie.png', dpi=300)


if __name__=='__main__':
	main()





