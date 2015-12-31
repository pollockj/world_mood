import json
from nltk.tokenize import TweetTokenizer
import csv
import sys
import argparse

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
	fields = ['Text', 'hashtags', 'retweet?']
	f.writerow(fields)

	#loop for lines in .json (assuming each line is a tweet)
	for line in in_file:
		retweet = False
		tweet = json.loads(line)

		#Check to see if tweet is a retweet 
		if tweet.get("retweeted_status"):
			text = tweet.get("retweeted_status").get("text").encode("unicode_escape") #store retweet text
			retweet = True
		#Else get tweet text
		elif tweet.get('text'):
			text = tweet.get('text').encode('unicode_escape')
			retweet = False
		#Tokenize if necessary
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
					f.writerow([processed_text, hashtag_list, retweet])
			else:
				f.writerow([processed_text, hashtag_list, retweet])


	#Close files when done
	out_file.close()
	in_file.close()

if __name__ == "__main__":
	parser = get_parser()
	args = parser.parse_args()
	main(args)