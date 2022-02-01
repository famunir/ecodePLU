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

                        response_URL = ''.join(self.start_urls)
                        response_URL = response_URL.replace("https://ecode360.com/", "")
                        response_URL_html = f"./scrapy-result/{response_URL}.html"

                                        
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
