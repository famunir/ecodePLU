import spacy
import string
import numpy as np

def find_right_uses(zone_locations, zone_names, raw_text):
        # Variation in names for intent of different zones
        uses_by_right_keywords = ["USES BY RIGHT"]

        # list of all the right uses for all the zones
        all_right_uses = {}

        # collect the zone and right uses found to remove false positive
        verified_zone_locations = []
        verified_zone_names = []
        detected_as_of_right_keyword_location = []
        detected_as_of_right_names = []

        # This code is applicable to a single architecture.
        # Loop for zone names detected in raw_text
        for iteration, item in enumerate(zone_names):
                current_zone_name = str(item)
                current_sentence_location = int(zone_locations[iteration])

                # ignore the zone names that lie at the very end of raw text and are possibly false detections
                if (len(raw_text) - int(current_sentence_location)) > 30:
                        next_sentence_location = current_sentence_location + 1
                        sentences_threshold = 25

                        # Loop for "uses by right" keyword
                        for uses_by_right_keyword in uses_by_right_keywords:
                                uses_by_right_keyword_check = 0
                                for sentence_iterator in range(next_sentence_location, next_sentence_location + sentences_threshold):
                                        next_sentence_text = raw_text[sentence_iterator]
                                        uses_by_right_keyword_check = next_sentence_text.find(uses_by_right_keyword)
                                        if uses_by_right_keyword_check != -1:
                                                # the length of sentence in which keyword is found should be less than 40 chars.
                                                if len(str(next_sentence_text)) < 200:
                                                        uses_by_right_keyword_found = str(uses_by_right_keyword)
                                                        sentence_use_by_right_keyword_found = sentence_iterator
                                                        break
                                                # If uses by right keyword exist in a longer sentence, check if it is in the start of the sentence
                                                elif uses_by_right_keyword_check < 5:
                                                        uses_by_right_keyword_found = str(uses_by_right_keyword)
                                                        sentence_use_by_right_keyword_found = sentence_iterator
                                                        break
                                        
                                if uses_by_right_keyword_check != -1:

                                        if zone_locations[iteration] not in verified_zone_locations:  
                                                if sentence_use_by_right_keyword_found not in detected_as_of_right_keyword_location:                              
                                                        verified_zone_locations.append(zone_locations[iteration])
                                                        verified_zone_names.append(item)
                                                        detected_as_of_right_keyword_location.append(sentence_use_by_right_keyword_found)
                                                        detected_as_of_right_names.append(uses_by_right_keyword)
                                                        
                                                        # print("\n")
                                                        # print(item)
                                                        # print(zone_locations[iteration])
                                                        # print(uses_by_right_keyword_found)
                                                        # print(sentence_use_by_right_keyword_found)
                                                        # print(raw_text[sentence_use_by_right_keyword_found])
                                                        # print("\n")
                                                        # break



        # for i in range(0, len(verified_zone_locations) - 2):
        #         for ii in range(i + 1, len(verified_zone_locations) - 1):
        #                 if (int(verified_zone_locations[i]) == int(verified_zone_locations[ii])):
        #                         verified_zone_locations.remove(verified_zone_locations[ii])
        #                         verified_zone_names.remove(verified_zone_names[ii])
        #                         detected_as_of_right_keyword_location.remove(detected_as_of_right_keyword_location[ii])
        #                         detected_as_of_right_names.remove(detected_as_of_right_names[ii])
                

        # print(verified_zone_locations)
        # print(verified_zone_names)
        # print(detected_as_of_right_keyword_location)
        # print(detected_as_of_right_names)


        sorted_zone_locations = np.array(verified_zone_locations)
        sorted_zone_locations = np.sort(sorted_zone_locations)

        for iteration, item in enumerate(verified_zone_names):
                current_zone_name = str(item)
                as_of_right_keyword = detected_as_of_right_names[iteration]
                current_sentence_location = detected_as_of_right_keyword_location[iteration]

                next_sentence_location = current_sentence_location + 1
                next_permit_type_keyword = 9999
                processed_sentences = 0

                # location of zone location in sorted zone locations
                for ii in range(0, len(sorted_zone_locations) - 1):
                        temp_zone_index = 0
                        if int(verified_zone_locations[iteration]) == sorted_zone_locations[ii]:
                                temp_zone_index = ii
                                break

                while True:

                        next_sentence_text = raw_text[next_sentence_location]
                        next_permit_type_keyword = next_sentence_text.find("USES BY SPECIAL EXCEPTION")
                        if next_permit_type_keyword != 9999 and next_permit_type_keyword != -1:
                                final_sentence_location = next_sentence_location
                                break

                        next_permit_type_keyword = next_sentence_text.find("ACCESSORY USES")
                        if next_permit_type_keyword != 9999 and next_permit_type_keyword != -1:
                                final_sentence_location = next_sentence_location
                                break

                        next_permit_type_keyword = next_sentence_text.find("CONDITIONAL USES")
                        if next_permit_type_keyword != 9999 and next_permit_type_keyword != -1:
                                final_sentence_location = next_sentence_location
                                break

                        next_permit_type_keyword = next_sentence_text.find("PROHIBITED USES")
                        if next_permit_type_keyword != 9999 and next_permit_type_keyword != -1:
                                final_sentence_location = next_sentence_location
                                break

                        next_permit_type_keyword = next_sentence_text.find("ENDING KEYWORD")
                        if next_permit_type_keyword != 9999 and next_permit_type_keyword != -1:
                                final_sentence_location = next_sentence_location
                                break

                        next_permit_type_keyword = next_sentence_text.find("ZONE CONTROLS")
                        if next_permit_type_keyword != 9999 and next_permit_type_keyword != -1:
                                final_sentence_location = next_sentence_location
                                break
                        

                        processed_sentences = next_sentence_location - current_sentence_location
                        # NEED TO MODIFY THIS CONDITION as it is not a very good condition
                        if processed_sentences == 80:
                                final_sentence_location = current_sentence_location + 30
                                break

                        # break if end of document reached
                        if next_sentence_location == len(raw_text) - 2:
                                final_sentence_location = current_sentence_location + 30
                                break

                        # break if next zone sentence reached
                        if int(verified_zone_locations[iteration]) != sorted_zone_locations[-1]:
                                if next_sentence_location >= sorted_zone_locations[temp_zone_index + 1]:
                                        # sentences between current zone location and next zone location
                                        sent_diff = sorted_zone_locations[temp_zone_index + 1] - current_sentence_location
                                        if sent_diff >= 30:
                                                final_sentence_location = current_sentence_location + 30
                                                break
                                        elif sent_diff < 30:
                                                final_sentence_location = sorted_zone_locations[temp_zone_index + 1]
                                                break

                        next_sentence_location += 1

                uses_dict = {}
                plu_sentences = raw_text[current_sentence_location:final_sentence_location]
                plu_text = ' '.join(plu_sentences)
                plu_text = plu_text.replace("  ", " ")
                plu_text = plu_text.replace('"','')
                plu_text = plu_text.replace("'","")
                plu_text = plu_text.replace("ZONE CONTROLS", "")
                plu_text = plu_text.replace("ENDING KEYWORD", "")
                uses_dict["Zone name"] = verified_zone_names[iteration]
                uses_dict["Right uses"] = plu_text
                all_right_uses[raw_text[int(verified_zone_locations[iteration])]] = uses_dict
                #print("\n")
                #print(verified_zone_locations[iteration])
                #print(raw_text[int(verified_zone_locations[iteration])])
                #print(item)
                #print(verified_zone_names[iteration])
                #print(current_sentence_location)
                #print(plu_text)
                #print(final_sentence_location)
                #print("\n")

        return all_right_uses
