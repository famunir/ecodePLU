import numpy as np
import string
import spacy

# This method is retired for the find control method which extracts the html of the controls.
def find_controls_text(zone_locations, zone_names, raw_text):


        nlp = spacy.load("en_core_web_sm")

        control_keywords = ["ZONE CONTROLS"]

        # all accessory uses in all the zones in the city
        all_controls = {}


        detected_control_keyword_location = []
        detected_control_names = []
        verified_zone_locations = []
        verified_zone_names = []

        sorted_zone_locations = np.array(zone_locations)
        sorted_zone_locations = np.sort(sorted_zone_locations)

        # This code is applicable to a single architecture.
        # Loop for zone names detected in raw_text
        for iteration, item in enumerate(zone_names):
                current_zone_name = str(item)
                current_sentence_location = int(zone_locations[iteration])

                # ignore the zone names that lie at the very end of raw text and are possibly false detections
                if (len(raw_text) - int(current_sentence_location)) > 30:
                        next_sentence_location = current_sentence_location + 1
                        sentences_threshold = 400

                        # Loop for "accessory uses" keyword
                        for control_keyword in control_keywords:
                                control_keyword_check = 0
                                for sentence_iterator in range(next_sentence_location, next_sentence_location + sentences_threshold):
                                        next_sentence_text = raw_text[sentence_iterator]
                                        control_keyword_check = next_sentence_text.find(control_keyword)

                                        if control_keyword_check != -1:
                                                # the length of sentence in which keyword is found should be less than 150 chars.
                                                if len(str(next_sentence_text)) < 100:
                                                        control_keyword_found = str(control_keyword)
                                                        sentence_control_keyword_found = sentence_iterator
                                                        break

                                        # location of zone location in sorted zone locations
                                        for ii in range(0, len(sorted_zone_locations) - 1):
                                                if current_sentence_location == sorted_zone_locations[ii]:
                                                        temp_zone_index = ii
                                                        break

                                        # break if next zone sentence reached
                                        if int(zone_locations[iteration]) != sorted_zone_locations[-1]:
                                                if sentence_iterator >= sorted_zone_locations[temp_zone_index + 1]:
                                                        break

                                        # break if end of document reached
                                        if sentence_iterator == len(raw_text) - 2:
                                                #print("Exception Use Keyword not Found. End of document.")
                                                break
                                        
                                if control_keyword_check != -1:
                                        if zone_locations[iteration] not in verified_zone_locations:  
                                                if sentence_control_keyword_found not in detected_control_keyword_location:

                                                        verified_zone_locations.append(zone_locations[iteration])
                                                        verified_zone_names.append(item)
                                                        detected_control_keyword_location.append(sentence_control_keyword_found)
                                                        detected_control_names.append(control_keyword)
                                                        
        #                                                 print("\n")
        #                                                 print(item)
        #                                                 print(zone_locations[iteration])
        #                                                 print(control_keyword_found)
        #                                                 print(sentence_control_keyword_found)
        #                                                 print(raw_text[sentence_control_keyword_found])
        #                                                 print("\n")
        #                                                 break
        # print(verified_zone_locations)
        # print(verified_zone_names)
        # print(detected_control_keyword_location)
        # print(detected_control_names)


        for iteration, item in enumerate(verified_zone_names):
                current_zone_name = str(item)
                control_keyword = detected_control_names[iteration]
                current_sentence_location = detected_control_keyword_location[iteration]

                next_sentence_location = current_sentence_location + 1
                next_permit_type_keyword = 9999
                processed_sentences = 0
                control_word_found = 0
                control_word_not_found = 0

                while True:

                        next_sentence_text = raw_text[next_sentence_location]
                        
                        ner_sentence = nlp(next_sentence_text)

                        for entity in ner_sentence.ents:
                                if entity.label_ == "QUANTITY" or entity.label_ == "PERCENT":
                                        final_sentence_location = next_sentence_location
                                        control_word_found = 1
                                        break
                        
                        if control_word_found == 1:
                                control_word_not_found = 0
                                control_word_found = 0
                        else:
                                control_word_not_found += 1

                        if control_word_not_found >= 8:
                                final_sentence_location = next_sentence_location - 7
                                break


                        processed_sentences = next_sentence_location - current_sentence_location
                        # NEED TO MODIFY THIS CONDITION as it is not a very good condition
                        # if processed_sentences == 60:
                        #         final_sentence_location = current_sentence_location + 15
                        #         break

                        # break if end of document reached
                        if next_sentence_location == len(raw_text) - 2:
                                #final_sentence_location = current_sentence_location + 15
                                final_sentence_location = len(raw_text) - 1
                                break

                        # location of zone location in sorted zone locations
                        for ii in range(0, len(sorted_zone_locations) - 1):
                                temp_zone_index = 0
                                if int(verified_zone_locations[iteration]) == sorted_zone_locations[ii]:
                                        temp_zone_index = ii
                                        break

                        # break if next zone sentence reached
                        if int(verified_zone_locations[iteration]) != sorted_zone_locations[-1]:
                                if next_sentence_location >= sorted_zone_locations[temp_zone_index + 1]:
                                        # sentences between current zone location and next zone location
                                        sent_diff = sorted_zone_locations[temp_zone_index + 1] - current_sentence_location
                                        if sent_diff >= 60:
                                                final_sentence_location = current_sentence_location + 30
                                                break
                                        elif sent_diff < 60:
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
                uses_dict["Controls"] = plu_text
                all_controls[raw_text[int(verified_zone_locations[iteration])]] = uses_dict

        return all_controls
