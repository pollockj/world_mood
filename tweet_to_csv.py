import json
from nltk.tokenize import TweetTokenizer
import csv
import sys
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

def main(argv):
	input_file = None
	output_file = None
	token = False
	text = None
	processed_text = None
	links = False
	try:
		opts, args = getopt.getopt(argv,"hi:o:",['help', "input=","output="])
		if not opts:
			print 'No options suppled'
			usage()
			sys.exit(2)
	except getopt.GetoptError:
		print 'Here'
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			usage()
			sys.exit()
		elif opt in ("-i", "--input"):
			input_file = arg
		elif opt in ("-o", "--output"):		
			output_file = arg
		elif opt in ("-t", "--tokenize"):
			token = True
		elif opt in ("-l" "--links"):
			links = True
		else:
			usage()
			sys.exit(2)

	# print 'Input file is ', input_file
   	# print 'Output file is ', output_file
	in_file = open(input_file, 'r')
	out_file = open(output_file, 'w')
	f = csv.writer(out_file)
	#Write headers for .csv


	#fields = ['Text', 'hashtags', 'favorite_count', 'retweet_count']
	fields = ['Text', 'hashtags']
	f.writerow(fields)

	#loop for lines in .json (assuming get line is a tweet)
	for line in in_file:
		tweet = json.loads(line)

		#Get tweet text, and tokenize
		if tweet.get('text'):
			text = tweet.get('text').encode('unicode_escape')
			if token:
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

			if not links:
				if entities.get("urls") == [] or not entities.get("media"): #if no urls
					# if not entities.get("media"): #if no media entity
					f.writerow([processed_text, hashtag_list])
			else:
				f.writerow([processed_text, hashtag_list])

	#Close files when done
	out_file.close()
	in_file.close()

if __name__ == "__main__":
	main(sys.argv[1:])