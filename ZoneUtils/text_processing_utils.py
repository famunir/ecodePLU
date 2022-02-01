import string
import numpy
from difflib import SequenceMatcher

def process_text(raw_text):
        # Basic formatting for sentence alignment
        for num in range(1, 21):
                sub_string_pattern = "\n" + str(num) + "." + "\n"
                rep_string_pattern = "\n" + str(num) + "." + " "
                raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)
                raw_text = raw_text.replace("SpecialCharacterSLASHForwarD", "/")
                sub_string_pattern = ": . "
                rep_string_pattern = ":" + "\n"
                raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        # Break sentences at particular uppercase and lowercase characters
        all_upper_alphabets = list(string.ascii_uppercase)
        all_lower_alphabets = list(string.ascii_lowercase)

        for iteration, item in enumerate(all_lower_alphabets):
                sub_string_pattern = " " + item + "." + " "
                rep_string_pattern = "\n" + item + "." + " "
                raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

                sub_string_pattern = " " + all_upper_alphabets[iteration] + "." + " "
                rep_string_pattern = "\n" + all_upper_alphabets[iteration] + "." + " "
                raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        # Break sentences at ". § " 
        sub_string_pattern = "." + " " + "§" + " "
        rep_string_pattern = "." + "\n" + "§" + " "
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        # Break sentences at "§"
        sub_string_pattern = "%" + " " + "§"
        rep_string_pattern = "%" + "\n" + "§"
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        # Break sentences at ". [Added"
        sub_string_pattern = "." + " " + "[Added"
        rep_string_pattern = "." + "\n" + " " + "[Added"
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        #raw text processing for special exceptions
        # Break sentences at ". ["
        sub_string_pattern = "." + " " + "["
        rep_string_pattern = "." + "\n" + "["
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        sub_string_pattern = "." + " " + "["
        rep_string_pattern = "." + "\n" + "["
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        sub_string_pattern = "." + " " + "("
        rep_string_pattern = "." + "\n" + "("
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        sub_string_pattern = "feet" + " " + "§"
        rep_string_pattern = "feet" + "\n" + "§"
        raw_text = raw_text.replace(sub_string_pattern, rep_string_pattern)

        # Merge zone name variations
        raw_text = raw_text.replace("Residences", "Residential")
        raw_text = raw_text.replace("Residence", "Residential")
        raw_text = raw_text.replace("Resident ", "Residential")

        raw_text = raw_text.replace("Commerce", "Commercial")

        raw_text = raw_text.replace("Agriculture", "Agricultural")

        raw_text = raw_text.replace("Official", "Office")

        raw_text = raw_text.replace("Industry", "Industrial")
        raw_text = raw_text.replace("Industries", "Industrial")

        raw_text = raw_text.replace("Recreation ", "Recreational")

        raw_text = raw_text.replace("Marijuana", "Cannabis")
        raw_text = raw_text.replace("Marihuana", "Cannabis")
        raw_text = raw_text.replace("MARIJUANA", "CANNABIS")
        raw_text = raw_text.replace("MARIHUANA", "CANNABIS")
        raw_text = raw_text.replace("marijuana", "cannabis")
        raw_text = raw_text.replace("marihuana", "cannabis")

        return raw_text


def remove_punctuation(input_text):
        punctuations = '''!{};:'"\<>?@#$^&*_~'''
        no_punct = ""
        for char in input_text:
                if char not in punctuations:
                        no_punct = no_punct + char
        return no_punct

def punctuation_remover(input_text):
        punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
        no_punct = ""
        for char in input_text:
                if char not in punctuations:
                        no_punct = no_punct + char
                else:
                        no_punct = no_punct + " "
        no_punct = no_punct.replace("   ", " ")
        no_punct = no_punct.replace("  ", " ")

        return no_punct.strip()

def similarity_index(a, b):
    return SequenceMatcher(None, a, b).ratio()

def transform_keywords(input_text):

        uses_by_right_keywords = ["principal permitted land use", "permitted land uses", "buildings and uses allowed by right", "buildings types and uses allowed by right", "principal uses allowed by right", "principal uses permitted by right", "principal uses permitted", "uses by right", "uses-by-right", "uses permitted by right", "uses permitted by-right", "uses allowed by right", "permitted by right uses", "permitted by right", "permitted-by-right", "permitted principal uses and structures", "permitted principal structures and uses", "permitted principal uses", "permitted principal land uses", "principal uses and structure", "principal uses and buildings", "uses and buildings permitted", "principal permitted uses", "principally permitted uses", "permitted uses by right", "principal permitted use", "principal permitted and conditional uses", "principal permitted and accessory uses", "principal and accessory uses", "permitted, accessory and conditional", "principal commercial uses", "primary intended use", "permitted commercial uses", "principal uses", "by right uses", "permitted facilities", "allowable uses", "uses permitted as matter of right", "uses permitted as of right", "uses as of right", "uses allowed without a use permit", "uses allowed without use permit", "allowed uses by right", "uses and development permitted.", "permitted buildings, structures and uses", "permitted structures and uses", "permitted uses and structures", "permitted structures or uses", "permitted uses or structures", "permitted uses, buildings and other structures", "permitted uses and activities", "all permitted uses", "permitted uses and developments", "permitted uses shall be", "authority and permitted uses", "permissible uses", "permitted primary uses", "primary permitted uses", "permitted secondary uses", "all uses permitted", "permitted buidling types", "permitted uses", "allowed uses", "examples of allowed uses", "allowable use", "allowed use", "use by right", "use permitted by right", "by right", "permitted principal use", "permitted principal", "principal use", "permitted use", "permissive use", "by-right", "by right", "uses permitted.", "uses allowed.", "primary uses", "authorized uses", "permitted activities"]
        
        uses_by_right_keywords_long = ["following uses are permitted in", "a lot or premises may be used or occupied for any of the following uses and no other", "a lot may be used or occupied for any of the following uses and no other", "a lot or premises may be used for any of the following purposes and no other", "for any of the following purposes and no other", "a lot may be used or occupied for any of the following purposes", "following uses shall be permitted in", "building or premises shall be used only for the following purpose", "shall be used except for the following permitted uses", "shall be used for only the following purposes", "shall be used for other than any of the following purposes", "building or premises shall be only for the following purpose", "following uses and businesses are permitted", "following principal uses shall be permitted", "following uses and businesses may be conducted", "following uses are permitted in", "following uses are permitted within", "shall be limited to the following uses", "for any purpose except the following", "for any uses except the following", "for any use except the following", "thereof shall be used except for any of the following purposes", "for any of the following purposes", "principal permitted uses", "permitted, conditional and accessory", "permitted, accessory and conditional", "principal uses are as follows", "principal uses shall be as follows", "permitted structures and uses", "permitted uses and structures", "uses shall be permitted", "uses permitted in", "permitted uses shall be", "permitted uses are as follows", "other than one of the uses", "uses listed in the use regulations", "primary permitted uses", "examples of allowed uses", "permitted uses are as follows", "strictly prohibited except", "following principal uses are allowed by right", "the following uses are permitted by right", "the following uses are permitted", "the following are permitted uses", "following principal uses and no others shall be permitted", "only the following principal uses are permitted", "following uses are allowed by right", "the following uses shall be permitted", "except for one or more of the following uses"]

        uses_by_exception_keywords = ["permitted uses by special use permit", "permitted uses subject to special conditions", "permitted principal special land use", "permitted special uses", "uses permitted subject to issuance of a special exception permit", "special permitted uses", "special permit uses", "special permit uses and structures", "special permit temporary uses", "uses permitted only by special exception", "uses permitted only by special permission", "principal uses permitted by special exception", "uses by special exception", "uses permitted by special exception", "uses subject to special exception", "uses permitted by special permit", "special exception uses", "permitted by special exception", "uses requiring a special exception permit", "uses requiring a special use permit", "uses requiring a special permit", "uses subject to director's review and approval", "permitted when special exception", "authorized as a special exception", "use by special exception", "use permitted by special exception", "use requiring a special exception permit", "use requiring a special use permit", "use requiring special use permits", "uses permitted with a special use permit", "uses allowed with special use permit", "uses allowed by special permit", "special use permit", "special use exceptions", "use subject to director's review and approval", "use permitted upon grant of a use permit", "special exception permit", "special case use", "special case approval", "special condition use", "special land use", "special exception use", "special exceptions", "special exception", "special uses permit", "specific permit uses", "special use permit", "special permit", "special uses", "special use", "exceptions"]
        
        uses_by_exception_keywords_long = ["any of the following uses when authorized as a special exception", "special permit", "special exception", "special permission", "special use permit", "special use exception", "special case use", "special case approval", "special condition use", "special land use", "special condition uses"]

        uses_by_accessory_keywords = ["permitted accessory land use", "accessory uses permitted", "accessory permitted uses", "permitted accessory uses", "permitted accessory units", "accessory structures or uses", "accessory uses or structures", "permitted accessory uses and structures", "permitted accessory structures and uses", "permitted accessory uses or structures", "permitted accessory structures or uses", "permitted accessory structures and buildings", "accessory buildings, structures or uses permitted", "accessory buildings, structures and uses", "accessory buildings or uses", "accessory uses or buildings", "accessory buildings and uses", "accessory building and use", "accessory buildings and structures", "accessory uses and buildings", "accessory structures and uses", "accessory uses and structures", "accessory and incidental uses", "accessory land uses and development", "accessory and temporary uses", "accessory uses", "accessorial uses", "ancillary uses", "permitted accessory use", "permitted accessory", "accessory structure or use", "accessory use", "accessory structures"]
        
        uses_by_accessory_keywords_long = ["accessory land use", "accessory use", "accessory structure", "accessory building"]

        uses_by_conditional_keywords = ["uses by conditional use permit", "uses permitted by conditional uses", "uses by conditional approval", "uses by condition approval", "uses by conditional use", "uses allowed as conditional uses", "permitted conditional uses", "uses subject to conditional use", "uses permitted under zoning board", "uses permitted with a conditional use", "use permitted with a conditional use", "uses subject to a major use permit", "uses subject to a minor use permit", "uses subject to an administrative permit", "uses allowed with conditional use permit", "uses permitted subject to a conditional use", "uses permitted subject to conditional use permit", "uses permitted subject to conditional use", "uses permitted upon grant of a use permit", "uses permitted upon grant of use permit", "uses and development permitted by conditional use permit", "uses and development permitted by a conditional use permit", "uses permitted by conditional development permit", "uses permitted by a conditional development permit", "uses requiring a zoning permit", "uses requiring an administrative permit", "uses requiring a conditional use permit", "uses requiring a use permit", "uses subject to a conditional use permit", "uses subject to conditions", "permitted by conditional uses", "uses subject to permit", "use subject to permit", "authorized as a conditional use", "use permitted as conditional use", "uses permitted as conditional use", "permitted as conditional use", "uses permitted by conditional use", "uses permitted by condition", "uses permitted conditionally", "use permitted by conditional use", "use permitted by condition", "use allowed as conditional use", "permitted conditional use", "permitted by conditional use", "conditional land use and development", "conditional uses and structures", "conditionally permitted uses", "conditional permit", "conditional uses", "conditional use", "uses by condition", "condition of use"]
        
        uses_by_conditional_keywords_long = ["conditional use permit", "conditional uses permit", "allowed as conditional use", "permitted as conditional use", "conditional land use and development", "conditional uses", "conditional use"]

        uses_by_prohibited_keywords = ["uses expressly prohibited", "nonpermitted uses", "non-permitted uses", "uses specifically prohibited", "specifically prohibited uses", "specifically prohibited", "uses prohibited.", "prohibited uses and structure", "prohibited uses and activities", "prohibited strutures and uses", "prohibited buildings and uses", "uses and activities prohibited", "prohibited land uses", "prohibited uses", "prohibited use", "use specifically prohibited", "following uses are prohibited", "use prohibited", "prohibited use", "prohibited activities", "prohibited practices", "nonpermitted use", "non-permitted use", "restrictions on uses", "uses not permitted", "are not permitted", "not permitted."]
        
        uses_by_prohibited_keywords_long = ["uses which are not permitted", "uses specifically prohibited", "specifically prohibited", "uses and improvement strictly prohibited", "prohibited uses and structure", "prohibited uses and activities", "uses and activities prohibited", "following uses are prohibited", "not permitted."]

        ending_keywords = ["area, height and dimensional requirements", "area, yard and height regulations", "area and bulk regulations", "area regulations", "development regulations", "acreage and density requirements", "density requirements", "area, bulk, height", "general standards", "density standards", "design standards", "special regulations", "additional requirements", "lot area and width", "lot, area and width", "lot, yard and height", "lot yard and height", "specific declaration", "design requirements", "dimensional and development standards", "height, area and bulk", "height area and bulk", "area, width", "existing structures", "requirements for all developments", "nonconforming structures", "design criteria", "lot area, width, building coverage", "lot area, width, depth, height and yard requirements", "lot area and dimensional requirements", "area and dimensional requirements", "dimensional requirements", "open space, impervious surface and area requirements", "area and dimensional standards", "dimensional standards", "area and height regulations", "dimensional criteria", "minimum parcel or lot size", "minimum lot area", "lot area", "minimum lot size", "structure height regulations", "height regulations", "structure location regulations", "area, height, yard", "property development standards", "development standards", "building height", "area requirements", "area and dimensional regulations", "area and bulk requirements", "bulk requirements", "district regulations", "yard regulations", "development options", "minimum occupation", "maximum density", "administrative waivers", "performance standards", "site development plan approval", "site development", "special requirements"]

        input_text = str(input_text)
        input_text_copy = input_text
        input_text = input_text.lower()


        # # Remove multiple keywords in a single sentence and replace them with one word. If there are multiple keywords, replace whole sentence with "USES BY RIGHT"

        # different_class_use_keyword_count = 0
        # if "right" in input_text:
        #         different_class_use_keyword_count += 1

        # if "special" in input_text or "exception" in input_text:
        #         different_class_use_keyword_count += 1

        # if "condition" in input_text:
        #         different_class_use_keyword_count += 1

        # if "accessory" in input_text:
        #         different_class_use_keyword_count += 1

        # if different_class_use_keyword_count > 2:
        #         return input_text_copy
        

        keyword_not_found_flag = 0

        if len(str(input_text)) < 60:
                
                for keyword in uses_by_exception_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 14 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "USES BY SPECIAL EXCEPTION")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_accessory_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 14 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "ACCESSORY USES")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_conditional_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 14 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "CONDITIONAL USES")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_prohibited_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 14 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "PROHIBITED USES")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_right_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 14 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "USES BY RIGHT")
                                keyword_not_found_flag = 1
                                break

                for keyword in ending_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 14 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                rep_text = keyword + "\n" + "ENDING KEYWORD"
                                input_text = input_text.replace(keyword, rep_text)
                                keyword_not_found_flag = 1
                                break

                if keyword_not_found_flag == 1:
                        return input_text
                elif keyword_not_found_flag == 0:
                        return input_text_copy

        elif len(str(input_text)) < 200:
                
                for keyword in uses_by_exception_keywords_long:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "USES BY SPECIAL EXCEPTION")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_accessory_keywords_long:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "ACCESSORY USES")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_conditional_keywords_long:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "CONDITIONAL USES")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_prohibited_keywords_long:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "PROHIBITED USES")
                                keyword_not_found_flag = 1
                                break

                for keyword in uses_by_right_keywords_long:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_not_found_flag == 0:
                                input_text = input_text.lower()
                                input_text = input_text.replace(keyword, "USES BY RIGHT")
                                keyword_not_found_flag = 1
                                break

                if keyword_not_found_flag == 1:
                        return input_text
                elif keyword_not_found_flag == 0:
                        return input_text_copy

        else:
                return input_text_copy

def transform_control_keywords(input_text):

        controls_keywords = ["area and bulk regulations", "area and bulk standards", "area and bulk requirements", "area and height regulations", "area and yard regulations", "area and development regulations", "area and dimensional regulations", "area and dimensional requirements", "lot and bulk requirements", "lot and bulk regulations", "lot area, width, depth", "area, height and special design regulations", "area and density regulations", "area, height and special regulations", "density and dimensional standards", "lot area, width, building coverage", "lot and setback regulations", "density and dimensional regulations", "development regulations", "dimensional criteria", "lot requirements", "lot and building requirements", "building requirements", "dimensions for development", "development requirements", "dimensional regulations", "design standards", "design requirements", "additional use requirements", "height regulations", "area, height and dimensional requirements", "area, yard and height regulations", "area, yard, and height regulations", "area, yard, height", "acreage and density requirements", "density requirements", "dimensional requirements", "lot, yard and height requirements", "general regulations", "area, density, yards and parking regulations", "site development standards", "site development", "construction standards", "general property development standards", "lot limitations", "lot size", "front yard regulations", "rear yard regulations", "side yard regulations", "density, open space and dimensional standards", "dimensional standards", "intensity of lot use", "subdivision standards", "density/intensity", "required lot area and dimension", "required bulk standards", "performance standards", "performance regulations",  "height, bulk and space requirements", "property development standard", "special development standard", "other general development standard", "area, lot width and yard requirement", "other regulation", "yard requirement", "setback and yards", "area, density, lot width and yard requirement", "development criteria", "area, height, lot width and yard requirement", "minimum lot dimension", "minimum lot coverage", "lot coverage", "lot size and coverage", "minimum front and rear yard", "minimum side yard", "building height", "yards and setbacks", "setback requirements",  "minimum lot area", "maximum dwelling density", "land use regulations", "minimum lot size", "independent living unit regulations", "special regulations", "area, width", "district wide development standards", "lot and structure requirements", "lots and yards requirements", "lot area, building height", "height of building", "lot area, lot width and coverage requirements", "dimensional, open space and coverage regulations", "area, yard and height requirements", "yard and lot requirements",  "area, yard and height restrictions", "lot area, lot width, and coverage requirements", "capacity, area and bulk regulations", "lot, yard and height standards", "yards; lot area", "lot area and width", "lot area regulations", "height, lot width", "required lot size", "required open space", "lot area, building height and yard requirements", "lot, yard and building height requirements", "lot requirements", "bulk and area regulations", "bulk and lot regulations", "bulk and area requirements", "area restrictions and regulations", "height restrictions and regulations", "lot area, lot width", "lot area", "height and story regulations", "height limit", "height limitation", "maximum building and structure height", "maximum height", "maximum density", "specific standards governing all mixed use development", "maximum building coverage", "lot, yard and building requirements", "density, lot width", "lot width", "lot area and yard requirements", "lot area, dimensional and design standards", "lot area.", "lot area and density", "open space, impervious surface and area requirements", "standards of development", "general standards", "development standards", "bulk requirements", "bulk regulations", "bulk and use table", "area regulations", "area requirements", "density and area", "space and bulk standards", "space and bulk requirements", "yard regulations", "yard requirements", "bulk standards", "parking regulations", "special requirements", "height requirements", "height area and bulk", "height area and lot", "height, area and lot", "district regulations", "open space requirements", "minimum open space", "minimum floor area", "rear yard", "side yard", "front yard", "yard dimensions", "yard required", "lot, bulk and intensity", "lot, bulk", "area, yard", "lot size", "height, yard", "setbacks"]

        input_text = str(input_text)
        input_text_copy = input_text
        input_text = input_text.lower()

        keyword_not_found_flag = 0

        if len(str(input_text)) < 150:
                for keyword in controls_keywords:
                        keyword_found_flag = input_text.find(keyword)
                        if keyword_found_flag != -1 and keyword_found_flag < 20:
                                rep_text = "ZONE CONTROLS" + "\n" + keyword
                                input_text = input_text.replace(keyword, rep_text)
                                keyword_not_found_flag = 1
                                break

                if keyword_not_found_flag == 1:
                        return input_text
                elif keyword_not_found_flag == 0:
                        return input_text_copy
        
        else:
                return input_text_copy
