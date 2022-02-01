from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import sys

import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk import sent_tokenize, word_tokenize
from nltk import PunktSentenceTokenizer
import codecs
import string


#----------------------------------------------------------------------------#

# AUTHOR : Fahad A. Munir

# CODE FLOW :
# Get the source of main zoning page -> (if childcontent found) retrieve it and don't search for any other links -> (if childcontent not found) 
# find all the links of chapters in the main zoning page -> visit each page -> (if childcontent found) retrieve data and don't search for any 
# other links -> (if childcontent not found) find all the links of subchapters in the chapter of a zoning page.

# INPUT ARGUMENTS : 
# [0] -> filename
# [1] -> URL of zoning page
# [2] -> Name of output file with file extension

# OUTPUT :
# Text file containg all text.

# NOTE : 
# The data for allsublinks is recorded in a single chapter.

#----------------------------------------------------------------------------#
def clean_text(raw_text):
                raw_text = raw_text.replace("\xa0"," ")
                raw_text = raw_text.replace("  "," ")
                raw_text = raw_text.replace("\\\"","\"")
                raw_text = raw_text.replace("\\'","'")
                raw_text = raw_text.replace("newLineCharacter", "\n")

                return raw_text

def hack_text(input_text):
        all_alphabets = list(string.ascii_uppercase)
        for alphabet in all_alphabets:

                # Donot break sentences at "A. "
                sub_string_pattern = alphabet + ". "
                rep_string_pattern = alphabet + "._"
                input_text = input_text.replace(sub_string_pattern,rep_string_pattern)

                # Break sentences at "some word] A."
                sub_string_pattern = "] " + alphabet + "."
                rep_string_pattern = "]. " + alphabet + "."
                input_text = input_text.replace(sub_string_pattern,rep_string_pattern)

                # Break sentences at "some word: A."
                sub_string_pattern = ": " + alphabet + "."
                rep_string_pattern = ":. " + alphabet + "."
                input_text = input_text.replace(sub_string_pattern,rep_string_pattern)

        # Break sentences at ":"
        input_text = input_text.replace(":", ":.")

        #print(input_text)
        input_text = input_text.replace("No. ","No._")
        input_text = input_text.replace(". [","._[")
        input_text = input_text.replace("] ", "]. ")

        # Break sentences at "some word (a)"
        # input_text = input_text.replace(" (", ". (")
        # input_text = input_text.replace("..", ".")

        return input_text

def unhack_text(hacked_sentence):
        all_alphabets = list(string.ascii_uppercase)
        for alphabet in all_alphabets:
                sub_string_pattern = alphabet + "._"
                rep_string_pattern = alphabet + ". "
                hacked_sentence = hacked_sentence.replace(sub_string_pattern,rep_string_pattern)

        #print(input_text)
        #hacked_sentence = hacked_sentence.replace("]. ","] ")
        hacked_sentence = hacked_sentence.replace(":.",": ")
        hacked_sentence = hacked_sentence.replace("No._","No. ")
        hacked_sentence = hacked_sentence.replace("._[",". [")
        hacked_sentence = hacked_sentence.replace(": _",":\n")
        hacked_sentence = hacked_sentence.replace(". [", ".\n[")

        return hacked_sentence

def getNextPageLinksData(sub_heading_links):

	pages_data = []
	pages_html = []
	for sublink in sub_heading_links:
		driver.get(sublink)

		# Get the title of the page
		partial_title1 = driver.find_elements_by_xpath("(//div[@id='pageTitle']/a/span[1])")
		partial_title1 = partial_title1[0].text
		partial_title2 = driver.find_elements_by_xpath("(//div[@id='pageTitle']/a/span[2])")
		partial_title2 = partial_title2[0].text

		if partial_title1 is not None and partial_title2 is not None:
			page_title = partial_title1 + " " + partial_title2
		page_title = page_title.replace("/","SpecialCharacterSLASHForwarD")

		pages_data.append(page_title)
		pages_data.append("\n")

		# Get the html of the all sub-pages and concatenate them
		next_page_data = driver.find_elements_by_xpath("//div[@id='childContent']")
		pages_data.append(next_page_data[0].text)
		pages_html.append(next_page_data[0].get_attribute('innerHTML'))

		time.sleep(2)

	pages_data = ' '.join(pages_data)
	pages_html = ' '.join(pages_html)

	return [pages_data, pages_html]

start_urls = sys.argv[1]
#output_file_name = sys.argv[2]


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")

driver = webdriver.Chrome(executable_path = "/root/docker-ecode-360/ecode/chromedriver", options = chrome_options)
driver.get(start_urls)

# Check if all the data exists on the main page and there are no links
page_data = driver.find_elements_by_xpath("//div[@id='childContent']")

data = []
if not page_data:

	time.sleep(2)
	main_heading_links = []
	find_main_headings_links = driver.find_elements_by_xpath("//div[starts-with(@class,'mediumTitle')]/a[@class='titleLink']")

	if not find_main_headings_links:
		find_main_headings_links = driver.find_elements_by_xpath("//div[@id='toc']/div[starts-with(@class,'barTitle')]/a[@class='titleLink']")

	for link in find_main_headings_links:
		main_heading_links.append(link.get_attribute("href"))

	for main_heading_link in main_heading_links:

		driver.get(main_heading_link)

		# Get the title of the page
		partial_title1 = driver.find_elements_by_xpath("(//div[@id='pageTitle']/a/span[1])")
		partial_title1 = partial_title1[0].text
		partial_title2 = driver.find_elements_by_xpath("(//div[@id='pageTitle']/a/span[2])")
		partial_title2 = partial_title2[0].text

		if partial_title1 is not None and partial_title2 is not None:
			page_title = partial_title1 + " " + partial_title2
		page_title = page_title.replace("/","SpecialCharacterSLASHForwarD")

		# Get the html of the page
		page_data = driver.find_elements_by_xpath("//div[@id='childContent']")

		# Check the existence of links if page_data (child content) is not found.
		if not page_data:
			next_page_links = driver.find_elements_by_xpath("//div[starts-with(@class,'mediumTitle')]/a[@class='titleLink']")

			if not next_page_links:
				next_page_links = driver.find_elements_by_xpath("//div[@id='toc']/div[starts-with(@class,'barTitle')]/a[@class='titleLink']")

			sub_heading_links = []
			for sublink in next_page_links:
				sub_heading_links.append(sublink.get_attribute("href"))

			total_data = getNextPageLinksData(sub_heading_links)
			page_data = total_data[0]
			page_html = total_data[1]
		else:
			page_html = page_data[0].get_attribute('innerHTML')
			page_data = page_data[0].text

		data.append("newLineCharacter")
		data.append(page_title)
		data.append("newLineCharacter")
		data.append(page_data)

		time.sleep(2)
else:
	# Get the title of the page
	partial_title1 = driver.find_elements_by_xpath("(//div[@id='pageTitle']/a/span[1])")
	partial_title1 = partial_title1[0].text
	partial_title2 = driver.find_elements_by_xpath("(//div[@id='pageTitle']/a/span[2])")
	partial_title2 = partial_title2[0].text

	if partial_title1 is not None and partial_title2 is not None:
		page_title = partial_title1 + " " + partial_title2
	page_title = page_title.replace("/","SpecialCharacterSLASHForwarD")

	page_html = page_data[0].get_attribute('innerHTML')
	page_data = page_data[0].text

	data.append("newLineCharacter")
	data.append(page_title)
	data.append("newLineCharacter")
	data.append(page_data)

data = ''.join(data)
data = data.replace("\n", " ")
all_text = clean_text(data)

train_text = codecs.open("/root/docker-ecode-360/ecode/scrapy-training/train_text.txt","r","utf8").read()
custom_sen_tokenizer = PunktSentenceTokenizer(train_text)

hacked_text = hack_text(all_text)
sentences = custom_sen_tokenizer.tokenize(hacked_text)

response_URL = start_urls.replace("https://ecode360.com/", "")
response_URL = f"/root/docker-ecode-360/ecode/scrapy-result/{response_URL}.txt"

for sentence in sentences:
        processed_sentence = unhack_text(sentence)
        #print(sentence)
        with open(response_URL,"a+") as f:
                f.write(processed_sentence)
                f.write("\n")