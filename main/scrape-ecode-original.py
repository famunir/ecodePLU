import scrapy
from scrapy.crawler import CrawlerProcess
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk import PunktSentenceTokenizer
import codecs
from nltk.tokenize.treebank import TreebankWordDetokenizer
import string
import sys

class ecodeExtractAllText(scrapy.Spider):
        name = "ecode-extract-all-print"
        custom_settings = { 'DOWNLOD_DELAY': 1, 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        # ERROR : start_urls = ["https://www.ecode360.com/32025905"]
        start_urls = [sys.argv[1]]


        def parse(self, response):

                partial_urls = response.xpath("//div[starts-with(@class,'mediumTitle')]/a[@class='titleLink']/@href").getall()

                if partial_urls:
                        
                        for url_address in partial_urls:
                                        
                                absolute_url = f"https://ecode360.com{url_address}"
                                
                                yield scrapy.Request(url = absolute_url, callback = self.extract_text)
                
                else:

                        partial_urls = response.xpath("//div[@id='toc']/div[starts-with(@class,'barTitle')]/a[@class='titleLink']/@href").getall()

                        if partial_urls:

                                for url_address in partial_urls:
                                                
                                        absolute_url = f"https://ecode360.com{url_address}"
                                        
                                        yield scrapy.Request(url = absolute_url, callback = self.extract_text)

                        else:

                                partial_urls = response.xpath("//div[starts-with(@class,'barTitle')]/label[@class='selectionLabel']/a/@href").getall()

                                for url_address in partial_urls:
                                                
                                        absolute_url = f"https://ecode360.com{url_address}"
                                        
                                        yield scrapy.Request(url = absolute_url, callback = self.extract_text)
                
        def clean_text(self, raw_text):
                raw_text = raw_text.replace("\xa0"," ")
                raw_text = raw_text.replace("  "," ")
                raw_text = raw_text.replace("\\\"","\"")
                raw_text = raw_text.replace("\\'","'")

                return raw_text

        def hack_text(self, input_text):
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

        def unhack_text(self, hacked_sentence):
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

                return hacked_sentence

        def extract_text(self, response):

                sub_partial_urls = response.xpath("//div[starts-with(@class,'mediumTitle')]/a[@class='titleLink']/@href").getall()

                if sub_partial_urls:
                        
                        for sub_url_address in sub_partial_urls:
                                        
                                absolute_url = f"https://ecode360.com{sub_url_address}"
                                
                                yield scrapy.Request(url = absolute_url, callback = self.extract_text)

                # else:

                #         sub_partial_urls = response.xpath("//div[@id='toc']/div[starts-with(@class,'barTitle')]/a[@class='titleLink']/@href").getall()

                #         if sub_partial_urls:

                #                 for sub_url_address in sub_partial_urls:
                                                
                #                         absolute_url = f"https://ecode360.com{sub_url_address}"
                                        
                #                         yield scrapy.Request(url = absolute_url, callback = self.extract_text)

                else:

                        partial_title1 = response.xpath("normalize-space((//div[@id='pageTitle']/a/span[1])/text())").get()
                        partial_title2 = response.xpath("normalize-space((//div[@id='pageTitle']/a/span[2])/text())").get()

                        if partial_title1 is not None and partial_title2 is not None:
                                page_title = partial_title1 + " " + partial_title2
                                page_title = page_title.replace("/","SpecialCharacterSLASHForwarD")

                        all_text = response.xpath("normalize-space(string(//div[@id='childContent']))").getall()
                        all_text = ''.join(all_text)
                        all_text = self.clean_text(all_text)

                        train_text = codecs.open("./scrapy-training/train_text.txt","r","utf8").read()
                        custom_sen_tokenizer = PunktSentenceTokenizer(train_text)

                        hacked_text = self.hack_text(all_text)
                        sentences = custom_sen_tokenizer.tokenize(hacked_text)

                        response_URL = ''.join(self.start_urls)
                        response_URL = response_URL.replace("https://ecode360.com/", "")
                        response_URL_html = f"./scrapy-result/{response_URL}.html"
                        response_URL = f"./scrapy-result/{response_URL}.txt"

                        with open(response_URL,"a+") as f:
                                f.write(page_title)
                                f.write("\n")

                        for sentence in sentences:
                                processed_sentence = self.unhack_text(sentence)
                                #print(sentence)
                                with open(response_URL,"a+") as f:
                                        f.write(processed_sentence)
                                        f.write("\n")
                                        
                        # Save html of each page                
                        with open(response_URL_html, "a+") as f:
                                f.write(response.text)

                        yield {
                                "Page Title" : page_title,
                                #"Text" : all_text,
                                #"HTML" : response.text,
                                "URL" : ''.join(self.start_urls)
                        }

process = CrawlerProcess()
process.crawl(ecodeExtractAllText)
process.start()
