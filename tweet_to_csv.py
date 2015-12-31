import json
from nltk.tokenize import TweetTokenizer
import csv
import sys
import argparse
import getopt

def usage():
	print 'tweet_to_csv.py [OPTIONS] -i <input_file> -o <output_file>'

#Given a tweet, get_hashtags will return a list of the hashtags (text).
#If there are no hashtags, it will return False
def get_hashtags(tweet):
	tmp_list = []
	hashtag_json_list = tweet.get("entities").get('hashtags') #get a list of the hashtags (in json format)
	if hashtag_json_list == []:
		return False
	for tag in hashtag_json_list:
		tmp_list.append(tag.get("text"))
	return tmp_list

def get_parser():

	parser = argparse.ArgumentParser(description="Storge data from JSON Tweet to .csv")
	parser.add_argument('-i',
						'--input',
						dest="input_file",
						help="Input file")
	parser.add_argument('-o',
						'--output',
						dest="output_file",
						help="Output file")	
	parser.add_argument('-t',
						'--tokenize',
						dest="token",
						default=False,
						action="store_true",
						help="Tokenize tweet text")
	parser.add_argument('-l',
						'--links',
						dest="links",
						default=False,
						action="store_true",
						help="Store tweets with links/media")
	return parser

def main(args):
	text = None
	processed_text = None

	in_file = open(args.input_file, 'r')
	out_file = open(args.output_file, 'w')
	f = csv.writer(out_file)

	#Write headers for .csv
	fields = ['Text', 'hashtags']
	f.writerow(fields)

	#loop for lines in .json (assuming each line is a tweet)
	for line in in_file:
		tweet = json.loads(line)

		#Get tweet text, and tokenize
		if tweet.get('text'):
			text = tweet.get('text').encode('unicode_escape')
			if args.token:
				processed_text = TweetTokenizer().tokenize(text)
			else:
				processed_text = text
		#print(processed_tweet)

		#Get favorite and retweet count
		# fav_count = tweet.get('favorite_count')
		# retweet_count = tweet.get('retweet_count')

		#Write data to csv
		entities = tweet.get("entities")
		if entities: #if entities != None

			#HASHTAGS
			hashtag_list = get_hashtags(tweet)

			if not args.links:
				if entities.get("urls") == [] or not entities.get("media"): #if no urls or media
					f.writerow([processed_text, hashtag_list])
			else:
				f.writerow([processed_text, hashtag_list])

	#Close files when done
	out_file.close()
	in_file.close()

if __name__ == "__main__":
	parser = get_parser()
	args = parser.parse_args()
	main(args)