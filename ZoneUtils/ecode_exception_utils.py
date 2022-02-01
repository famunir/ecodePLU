import numpy as np

def find_exception_uses(zone_locations, zone_names, raw_text):

        uses_by_exception_keywords = ["USES BY SPECIAL EXCEPTION"]

        # other_uses_words = ["Use by special exception", "Use by Special Exception", "Use By Special Exception", "use by special exception"]

        # all exception uses for all the zones in the city
        all_exception_uses = {}

        detected_exception_keyword_location = []
        detected_exception_names = []
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
                        sentences_threshold = 350

                        # Loop for "exception uses" keyword
                        for uses_by_exception_keyword in uses_by_exception_keywords:
                                uses_by_exception_keyword_check = 0
                                for sentence_iterator in range(next_sentence_location, next_sentence_location + sentences_threshold):
                                        next_sentence_text = raw_text[sentence_iterator]
                                        uses_by_exception_keyword_check = next_sentence_text.find(uses_by_exception_keyword)

                                        if uses_by_exception_keyword_check != -1:
                                                # the length of sentence in which keyword is found should be less than 150 chars.
                                                if len(str(next_sentence_text)) < 200:
                                                        exception_uses_keyword_found = str(uses_by_exception_keyword)
                                                        sentence_exception_uses_keyword_found = sentence_iterator
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
                                        
                                if uses_by_exception_keyword_check != -1:
                                        if zone_locations[iteration] not in verified_zone_locations:  
                                                if sentence_exception_uses_keyword_found not in detected_exception_keyword_location:

                                                        verified_zone_locations.append(zone_locations[iteration])
                                                        verified_zone_names.append(item)
                                                        detected_exception_keyword_location.append(sentence_exception_uses_keyword_found)
                                                        detected_exception_names.append(uses_by_exception_keyword)
                                                        
        #                                                 print("\n")
        #                                                 print(item)
        #                                                 print(zone_locations[iteration])
        #                                                 print(exception_uses_keyword_found)
        #                                                 print(sentence_exception_uses_keyword_found)
        #                                                 print(raw_text[sentence_exception_uses_keyword_found])
        #                                                 print("\n")
        #                                                 break
        # print(verified_zone_locations)
        # print(verified_zone_names)
        # print(detected_exception_keyword_location)
        # print(detected_exception_names)

        for iteration, item in enumerate(verified_zone_names):
                current_zone_name = str(item)
                exception_right_keyword = detected_exception_names[iteration]
                current_sentence_location = detected_exception_keyword_location[iteration]

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
                        next_permit_type_keyword = next_sentence_text.find("USES BY RIGHT")
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
                                final_sentence_location = current_sentence_location + 20
                                break

                        # break if end of document reached
                        if next_sentence_location == len(raw_text) - 2:
                                final_sentence_location = current_sentence_location + 20
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
                uses_dict["Exception uses"] = plu_text
                all_exception_uses[raw_text[int(verified_zone_locations[iteration])]] = uses_dict
                #print("\n")
                #print(verified_zone_locations[iteration])
                #print(raw_text[int(verified_zone_locations[iteration])])
                #print(item)
                #print(verified_zone_names[iteration])
                #print(current_sentence_location)
                #print(plu_text)
                #print(final_sentence_location)
                #print("\n")

        return all_exception_uses
