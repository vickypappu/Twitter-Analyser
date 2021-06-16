# Python Script to Extract tweets of a
# particular Hashtag using Tweepy and Pandas


# import modules
import pandas as pd
import tweepy
import csv



# function to perform data extraction
def scrape(words, numtweet):
	
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                                                    'followers', 'totaltweets', 'retweetcount', 'Tweet', 'hashtags'])
    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)
    tweets = tweepy.Cursor(api.search, q=words, lang="en", tweet_mode='extended').items(numtweet)#since=date_since
    
    # .Cursor() returns an iterable object. Each item in
    # the iterator has various attributes that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]
    
    # Counter to maintain Tweet Count
    i = 1
	
    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        
        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username, description, location, following, followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet
        # Function call to print tweet data on screen
        i = i+1
    db.to_csv('scraped_tweets.csv')
    
                


if __name__ == '__main__':
	
    # Enter your own credentials obtained
    # from your developer account
    consumer_key = "OIzAvzLwIV0rvIILvPDYxr9Op"
    consumer_secret = "4aRXzlqqe0ksvyEdIZmre21P1isFZ46MrH3XBRfk390yrRhM6I"
    access_key = "1342826884103503876-pRU6yuw8B8cmhecsjEi0quZ89PmfxS"
    access_secret = "CxFRJPlOtjDdsy5tZE1wuCBMmduTOBdkM4g0wUgAjeBaA"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    # Enter Hashtag and initial date
    print("Enter Twitter HashTag to search for")
    words = input()
    
    # number of tweets you want to extract in one run
    numtweet = 100
    scrape(words, numtweet)
    print('Scraping has completed!')



