import spacy
import string
import numpy as np
import pandas as pd
import sys
import json

sys.path.append(".")

from ZoneUtils.text_processing_utils import punctuation_remover
from ZoneUtils.text_processing_utils import similarity_index
from ZoneUtils.text_processing_utils import process_text
from ZoneUtils.text_processing_utils import remove_punctuation
from ZoneUtils.text_processing_utils import transform_keywords
from ZoneUtils.text_processing_utils import transform_control_keywords
from ZoneUtils.ecode_right_utils import find_right_uses
from ZoneUtils.ecode_exception_utils import find_exception_uses
from ZoneUtils.ecode_conditional_utils import find_conditional_uses
from ZoneUtils.ecode_prohibited_utils import find_prohibited_uses
from ZoneUtils.ecode_accessory_utils import find_accessory_uses

# Filenames = [8337502 9647638 10752882 11892117 12179966 12186661 14751411 30859978 31718500 11881518 13033355]
#non functional = [11714908 13159599]
# Validation = [13347161 13159599 30831666 9228557 13282057 10740717 7099439 29938192 12736265 8009217 15296084]

def extract_all_text(text_file, city_zone_names):

        text_file_name = text_file

        # read raw test
        with open(f"./scrapy-result/{text_file_name}.txt", 'r') as f:
                raw_text = f.read()

        ########################################
        #zones_copy_for_controls = city_zone_names
        ########################################

        raw_text = process_text(raw_text)

        # Initialize the model and detect zone names
        # zone_model = spacy.load("./temp_zonename_model")

        # Initialize the model and detect PLUs
        # plu_model = spacy.load("./temp_PLU_model")

        raw_text = raw_text.split("\n")

        for iteration, item in enumerate(raw_text):
                raw_text[iteration] = transform_keywords(item)
                raw_text[iteration] = transform_control_keywords(raw_text[iteration])
                sentence = raw_text[iteration]
                raw_text[iteration] = sentence.replace("ending keyword", "ENDING KEYWORD")

        raw_text = '\n'.join(raw_text)

        raw_text = raw_text.split("\n")


        #======================================

        #city_zone_names = city
        #city_zone_names = f"{city_zone_names}.csv"

        #csv_text = pd.read_csv(f"./city-zones/{city_zone_names}")
        #print(csv_text[["zone_name"]])

        #city_zone_names = csv_text["zone_name"].tolist()
        #print(city_zone_names)

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

                
                        zone_in_sentence_flag = sentence.find(zone)
                        if zone_in_sentence_flag != -1 and len(sentence) < 120:
                                find_target_flag = sentence.find("§")
                                if find_target_flag == -1:
                                        find_target_flag = sentence.find("article")
                                if find_target_flag == -1:
                                        find_target_flag = sentence.find("part")
                                if find_target_flag == -1:
                                        find_target_flag = sentence.find("chapter")
                                if find_target_flag == -1:
                                        find_target_flag = sentence.find("div")
                                if find_target_flag == -1:
                                        find_target_flag = sentence.find("sec")
                                
                                if find_target_flag != -1 and find_target_flag < 2:
                                        if iteration not in zone_locations:
                                                zone_names.append(actual_zone_name)
                                                zone_sentences.append(item)
                                                zone_locations.append(iteration)

                        elif zone_in_sentence_flag == -1 and len(sentence) < 120:
                                zone = zone.replace("districts", "")
                                zone = zone.replace("district", "")
                                zone  = zone.strip()
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

                                                find_target_flag = sentence.find("§")
                                                if find_target_flag == -1:
                                                        find_target_flag = sentence.find("article")
                                                if find_target_flag == -1:
                                                        find_target_flag = sentence.find("part")
                                                if find_target_flag == -1:
                                                        find_target_flag = sentence.find("chapter")
                                                if find_target_flag == -1:
                                                        find_target_flag = sentence.find("div")
                                                if find_target_flag == -1:
                                                        find_target_flag = sentence.find("sec")
                                                
                                                if find_target_flag != -1 and find_target_flag < 2:
                                                        if iteration not in zone_locations:
                                                                zone_names.append(actual_zone_name)
                                                                zone_sentences.append(item)
                                                                zone_locations.append(iteration)


        #print(zone_names)
        #print(zone_sentences)
        #print(zone_locations)

        #Remove the wrongly detcted zone lines by analyzing the first character of each zone sentence
        symbol_count_flag = 0
        article_count_flag = 0
        part_count_flag = 0
        chapter_count_flag = 0
        div_count_flag = 0
        sec_count_flag = 0

        for zone_sent in zone_sentences:

                zone_sent = zone_sent.lower()

                if zone_sent.startswith("§"):
                        symbol_count_flag += 1
                        if "district" in zone_sent or "zone" in zone_sent:
                                symbol_count_flag += 1

                elif zone_sent.startswith("article"):
                        article_count_flag += 1
                        if "district" in zone_sent or "zone" in zone_sent:
                                article_count_flag += 1

                elif zone_sent.startswith("part"):
                        part_count_flag += 1
                        if "district" in zone_sent or "zone" in zone_sent:
                                part_count_flag += 1
                
                elif zone_sent.startswith("chapter"):
                        chapter_count_flag += 1
                        if "district" in zone_sent or "zone" in zone_sent:
                                chapter_count_flag += 1

                elif zone_sent.startswith("div"):
                        div_count_flag += 1
                        if "district" in zone_sent or "zone" in zone_sent:
                                div_count_flag += 1

                elif zone_sent.startswith("sec"):
                        sec_count_flag += 1
                        if "district" in zone_sent or "zone" in zone_sent:
                                sec_count_flag += 1

        if symbol_count_flag >= max(article_count_flag, part_count_flag, chapter_count_flag, div_count_flag, sec_count_flag):
                most_repeatitive_first_word = "§"

        elif article_count_flag >= max(symbol_count_flag, part_count_flag, chapter_count_flag, div_count_flag, sec_count_flag):
                most_repeatitive_first_word = "article"

        elif part_count_flag >= max(symbol_count_flag, article_count_flag, chapter_count_flag, div_count_flag, sec_count_flag):
                most_repeatitive_first_word = "part"

        elif chapter_count_flag >= max(symbol_count_flag, article_count_flag, part_count_flag, div_count_flag, sec_count_flag):
                most_repeatitive_first_word = "chapter"

        elif div_count_flag >= max(symbol_count_flag, article_count_flag, part_count_flag, chapter_count_flag, sec_count_flag):
                most_repeatitive_first_word = "div"

        elif sec_count_flag >= max(symbol_count_flag, article_count_flag, part_count_flag, chapter_count_flag, div_count_flag):
                most_repeatitive_first_word = "sec"

        updated_zone_names = []
        updated_zone_sentences = []
        updated_zone_locations = []

        for iteration, zone_sent in enumerate(zone_sentences):
                zone_sent = zone_sent.lower()
                if zone_sent.startswith(most_repeatitive_first_word):
                        updated_zone_names.append(zone_names[iteration])
                        updated_zone_sentences.append(zone_sentences[iteration])
                        updated_zone_locations.append(zone_locations[iteration])

        # Consider all detected zone names if the ratio is greater than or equal to 0.5
        length_of_original_detected_zones = len(zone_names)
        length_of_updated_zones = len(updated_zone_sentences)
        length_of_updated_zones = length_of_original_detected_zones - length_of_updated_zones
        zone_ratio = length_of_updated_zones/length_of_original_detected_zones

        if zone_ratio < 0.25:
                zone_names = updated_zone_names
                zone_sentences = updated_zone_sentences
                zone_locations = updated_zone_locations


        #--------------------------------------


        # Lists for saving "unique zone names" and "location of sentences containing zone names"
        #potential_zone_names = []

        # Process all sentences and extract the zone names
        # Save zone names which have a string lenght greater than 15 and the sentence in which they occur has a length smaller than 92.
        #for iteration, item in enumerate(raw_text):
        #        raw_sentence = remove_punctuation(str(item))
        #        processed_sentence = zone_model(raw_sentence)
        #        for entity in processed_sentence.ents:
        #                if len(str(entity)) > 15 and len(str(entity)) < 75:
        #                        if (str(entity)) not in potential_zone_names:
                                        #print (entity, entity.label_)
                                        #print(iteration)
        #                                potential_zone_names.append(str(entity))

        #print(potential_zone_names)

        # first loop over all saved zone names
        # second loop over all sentences
        # Extract the exact zone names and corresponding location (which satify the criteria).
        # Ignore the rest of the zone names and rest of the sentences in which zone names were found but did not satify the criteria

        # zone_names = []
        # zone_sentences = []
        # zone_locations = []
        #for zone_name in potential_zone_names:
        #        for iteration, item in enumerate(raw_text):
        #                raw_sentence = remove_punctuation(str(item))

        #                if str(zone_name) in raw_sentence:

        #                        find_target_check = raw_sentence.find("§")
        #                        if find_target_check == -1:
        #                                find_target_check = raw_sentence.find("Article")
        #                        if find_target_check == -1:
        #                                find_target_check = raw_sentence.find("Part")

        #                        if find_target_check != -1 and find_target_check < 2 and len(raw_sentence) < 120:
        #                                if iteration not in zone_locations:
        #                                        zone_names.append(zone_name)
        #                                        zone_locations.append(iteration)
        #                                        zone_sentences.append(raw_sentence)
                                                # print("\n")
                                                # print(zone_name)
                                                # print(raw_sentence)
                                                # print(iteration)
                                                # print("\n")
        #                                        break
        #print(zone_names)
        #print(zone_sentences)
        #print(zone_locations)


        all_right_uses = find_right_uses(zone_locations, zone_names, raw_text)

        all_exception_uses = find_exception_uses(zone_locations, zone_names, raw_text)

        all_conditional_uses = find_conditional_uses(zone_locations, zone_names, raw_text)

        all_prohibited_uses = find_prohibited_uses(zone_locations, zone_names, raw_text)

        all_accessory_uses = find_accessory_uses(zone_locations, zone_names, raw_text)
        

        all_city_plus = {}

        all_city_plus["all_right_uses"] = all_right_uses
        all_city_plus["all_exception_uses"] = all_exception_uses
        all_city_plus["all_conditional_uses"] = all_conditional_uses
        all_city_plus["all_prohibited_uses"] = all_prohibited_uses
        all_city_plus["all_accessory_uses"] = all_accessory_uses

        return all_city_plus



