import spacy
import string
import numpy as np
import pandas as pd
from ZoneUtils.html_processing_utils import punctuation_remover
from ZoneUtils.html_processing_utils import similarity_index
from ZoneUtils.html_processing_utils import remove_punctuation
from ZoneUtils.html_processing_utils import transform_control_keywords
from ZoneUtils.ecode_control_html_utils import find_controls


def extract_control_html(text_file_name, city_zone_names):

        # read raw test
        with open(f"./scrapy-result/{text_file_name}.html", 'r') as f:
                raw_text = f.read()

        raw_text = raw_text.split("\n")
        raw_text = transform_control_keywords(raw_text)


        base_zone_names = ["residential", "commercial", "agricultural", "business", "office", "industrial", "highway", "institutional", "specific plan", "open space", "apartment", "overlay"]

        for base_zone_name in base_zone_names:
                city_zone_names.append(base_zone_name)
                

        zone_names = []
        zone_sentences = []
        zone_locations = []

        for zone in city_zone_names:
                actual_zone_name = str(zone)
                zone = punctuation_remover(str(zone))
                zone = zone.lower()
                for iteration, item in enumerate(raw_text):
                        sentence = punctuation_remover(str(item))
                        sentence = sentence.lower()

                        previous_sentence = punctuation_remover(raw_text[iteration - 1])
                        previous_sentence = previous_sentence.lower()

                        second_previous_sentence = punctuation_remover(raw_text[iteration - 2])
                        second_previous_sentence = second_previous_sentence.lower()

                        third_previous_sentence = punctuation_remover(raw_text[iteration - 4])
                        third_previous_sentence = third_previous_sentence.lower()

                        fourth_previous_sentence = punctuation_remover(raw_text[iteration - 5])
                        fourth_previous_sentence = fourth_previous_sentence.lower()

                        fifth_previous_sentence = punctuation_remover(raw_text[iteration - 6])
                        fifth_previous_sentence = fifth_previous_sentence.lower()

                        if iteration == 6246:
                                x = 1

                
                        zone_in_sentence_flag = sentence.find(zone)
                        if zone_in_sentence_flag != -1 and zone_in_sentence_flag < 41 and len(sentence) < 120: # 41 is based on analysis

                                find_target_flag = sentence.find('data full title="')
                                find_previous_target_flag = previous_sentence.find('<div class="bartitle sectiontitle')

                                if find_target_flag != -1 and find_target_flag < 5:
                                        if find_previous_target_flag != -1 and find_target_flag < 5:
                                                if second_previous_sentence == "":
                                                        if iteration not in zone_locations:
                                                                zone_names.append(actual_zone_name)
                                                                zone_sentences.append(item)
                                                                zone_locations.append(iteration)

                        elif zone_in_sentence_flag == -1 and len(sentence) < 120:
                                zone = zone.replace("districts", "")
                                zone = zone.replace("district", "")
                                zone_tokens = zone.split(sep = " ")
                                sentence_tokens = sentence.split(sep = " ")

                                # Match 1st word of zone name in a sentence and find the word's location in the sentence
                                word_found_flag = 0
                                for iteration2, item2 in enumerate(sentence_tokens):
                                        corr = similarity_index(zone_tokens[0], item2)
                                        if corr >= 0.75:
                                                word_found_flag = 1
                                                break

                                # Calculate the number of words that should be available in sentence and zone to calculate corr        
                                number_of_sentence_tokens = len(sentence_tokens)
                                number_of_zone_tokens = len(zone_tokens)
                                difference = number_of_sentence_tokens - (iteration2 + 1)
                                difference_comparison = number_of_zone_tokens - 1

                                # Calculate the correlation of words ocuuring after the first matched word
                                if word_found_flag == 1 and difference >= difference_comparison and number_of_zone_tokens > 1:
                                        sentence_token_index = iteration2 + 1
                                        for ii in range (1, number_of_zone_tokens):
                                                corr = similarity_index(zone_tokens[ii], sentence_tokens[sentence_token_index])
                                                if corr >= 0.75:
                                                        sentence_token_index += 1
                                                else: 
                                                        break
                                        # IF one more word is matched (total 2 matched) then check if it is a possible zone name        
                                        if ii >= 2:
                                                #print(sentence)
                                                #print(zone)

                                                find_target_flag = sentence.find('data full title="')
                                                find_previous_target_flag = previous_sentence.find('<div class="bartitle sectiontitle')

                                                if find_target_flag != -1 and find_target_flag < 5:
                                                        if find_previous_target_flag != -1 and find_target_flag < 5:
                                                                if second_previous_sentence == "":
                                                                        if iteration not in zone_locations:
                                                                                zone_names.append(actual_zone_name)
                                                                                zone_sentences.append(item)
                                                                                zone_locations.append(iteration)

        # For a different structure of ecode360 website
                        zone_in_sentence_flag = sentence.find(zone)
                        if zone_in_sentence_flag != -1 and zone_in_sentence_flag < 18 and len(sentence) < 120: # 41 is based on analysis

                                find_target_flag = sentence.find("span")
                                find_previous_target_flag = previous_sentence.find('<span class="titletitle">')
                                find_second_previous_target_flag = second_previous_sentence.find("< span>")
                                find_third_previous_target_flag = third_previous_sentence.find('<span class="titlenumber">')
                                find_fourth_previous_target_flag = fourth_previous_sentence.find('<a href="')
                                find_fifth_previous_target_flag = fifth_previous_sentence.find('<div id="pagetitle" class="customertitlecolor">')

                                if find_target_flag != -1 and find_target_flag < 60:
                                        if find_previous_target_flag != -1 and find_previous_target_flag < 5:
                                                if find_second_previous_target_flag != -1 and find_second_previous_target_flag < 5:
                                                        if find_third_previous_target_flag != -1 and find_third_previous_target_flag < 5:
                                                                if find_fourth_previous_target_flag != -1 and find_fourth_previous_target_flag < 5:
                                                                        if find_fifth_previous_target_flag != -1 and find_fifth_previous_target_flag < 5:
                                                                                if iteration not in zone_locations:
                                                                                        zone_names.append(actual_zone_name)
                                                                                        zone_sentences.append(item)
                                                                                        zone_locations.append(iteration)

                        elif zone_in_sentence_flag == -1 and len(sentence) < 120:
                                zone = zone.replace("districts", "")
                                zone = zone.replace("district", "")
                                zone_tokens = zone.split(sep = " ")
                                sentence_tokens = sentence.split(sep = " ")

                                # Match 1st word of zone name in a sentence and find the word's location in the sentence
                                word_found_flag = 0
                                for iteration2, item2 in enumerate(sentence_tokens):
                                        corr = similarity_index(zone_tokens[0], item2)
                                        if corr >= 0.75:
                                                word_found_flag = 1
                                                break

                                # Calculate the number of words that should be available in sentence and zone to calculate corr        
                                number_of_sentence_tokens = len(sentence_tokens)
                                number_of_zone_tokens = len(zone_tokens)
                                difference = number_of_sentence_tokens - (iteration2 + 1)
                                difference_comparison = number_of_zone_tokens - 1

                                # Calculate the correlation of words ocuuring after the first matched word
                                if word_found_flag == 1 and difference >= difference_comparison and number_of_zone_tokens > 1:
                                        sentence_token_index = iteration2 + 1
                                        for ii in range (1, number_of_zone_tokens):
                                                corr = similarity_index(zone_tokens[ii], sentence_tokens[sentence_token_index])
                                                if corr >= 0.75:
                                                        sentence_token_index += 1
                                                else: 
                                                        break
                                        # IF one more word is matched (total 2 matched) then check if it is a possible zone name        
                                        if ii >= 2:
                                                #print(sentence)
                                                #print(zone)

                                                find_target_flag = sentence.find("span")
                                                find_previous_target_flag = previous_sentence.find('<span class="titletitle">')
                                                find_second_previous_target_flag = second_previous_sentence.find("< span>")
                                                find_third_previous_target_flag = third_previous_sentence.find('<span class="titlenumber">')
                                                find_fourth_previous_target_flag = fourth_previous_sentence.find('<a href="')
                                                find_fifth_previous_target_flag = fifth_previous_sentence.find('<div id="pagetitle" class="customertitlecolor">')

                                                if find_target_flag != -1 and find_target_flag < 60:
                                                        if find_previous_target_flag != -1 and find_previous_target_flag < 5:
                                                                if find_second_previous_target_flag != -1 and find_second_previous_target_flag < 5:
                                                                        if find_third_previous_target_flag != -1 and find_third_previous_target_flag < 5:
                                                                                if find_fourth_previous_target_flag != -1 and find_fourth_previous_target_flag < 5:
                                                                                        if find_fifth_previous_target_flag != -1 and find_fifth_previous_target_flag< 5:
                                                                                                if iteration not in zone_locations:
                                                                                                        zone_names.append(actual_zone_name)
                                                                                                        zone_sentences.append(item)
                                                                                                        zone_locations.append(iteration)



        all_controls = find_controls(zone_locations, zone_names, raw_text)
        
        return all_controls


