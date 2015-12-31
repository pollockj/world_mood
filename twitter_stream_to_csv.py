# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python twitter_stream_download.py -q apple -d data
# 
# It will produce the list of tweets for the query "apple" 
# in the file data/stream_apple.json
# Code modified from http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/ 

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import argparse
import string
import config
import csv

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    parser.add_argument("-l",
                        "--filter_level",
                        dest="level",
                        help="Filter Level")
    parser.add_argument("-m",
                        "--Max",
                        dest="max_tweets",
                        type=int,
                        help="Maximum number of tweets to save")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, query, fLevel):
        super(MyListener, self).__init__() #call to the init of the base class
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s_%s.csv" % (data_dir, query_fname, fLevel)
        self.tweet_number = 0
        with open(self.outfile, 'a') as f:
            csv_f = csv.writer(f)
            csv_f.writerow(["Text","Retweet","Created at"])

    def on_status(self, status):
        self.tweet_number += 1
        if hasattr (status, 'retweeted_status'):
            retweet = True
            text = status.retweeted_status.text
        else:
            retweet = False
            text = status.text
        if self.tweet_number < args.max_tweets:
            with open(self.outfile, 'a') as f:
                    csv_f = csv.writer(f)
                    csv_f.writerow([text.encode("unicode_escape"),retweet,status.created_at])
                    print(text)
            return True
        else:
            return False

    def on_error(self, status):
        if status == 420:
            return False
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.

    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.

    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query, args.level))
    twitter_stream.filter(track=[args.query], languages=['en'], filter_level=args.level)

