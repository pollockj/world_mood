import json
from nltk.tokenize import TweetTokenizer
import csv
import sys
import getopt

def usage():
	print 'tweet_to_csv.py -i <input_file> -o <output_file>'

def main(argv):
	input_file = None
	output_file = None
	token = False
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
		else:
			usage()
			sys.exit(2)

	print 'Input file is ', input_file
   	print 'Output file is ', output_file
	in_file = open(input_file, 'r')
	out_file = open(output_file, 'w')
	f = csv.writer(out_file)
	#Write headers for .csv


	#fields = ['Text', 'hashtags', 'favorite_count', 'retweet_count']
	fields = ['Text']
	f.writerow(fields)

	#loop for lines in .json (assuming get line is a tweet)
	for line in in_file:
		#line = in_file.readline()
		tweet = json.loads(line)

		#Get tweet text, and tokenize
		text = tweet.get('text').encode('unicode_escape')
		if token:
			processed_text = TweetTokenizer().tokenize(text)
		else:
			processed_text = text
		#print(processed_tweet)

		#Get favorite and retweet count
		fav_count = tweet.get('favorite_count')
		retweet_count = tweet.get('retweet_count')

		#Get hastags
		hastags = tweet.get('hastags')
		if not hastags:
			hastags = False
		#Write data to csv
		#f.writerow([processed_text,hastags,fav_count,retweet_count])
		f.writerow([processed_text])

	#Close files when done
	out_file.close()
	in_file.close()

if __name__ == "__main__":
	main(sys.argv[1:])