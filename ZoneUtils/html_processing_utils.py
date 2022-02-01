import string
import numpy
from difflib import SequenceMatcher


def remove_punctuation(input_text):
        punctuations = '''!{};:'"\<>?@#$^&*_~'''
        no_punct = ""
        for char in input_text:
                if char not in punctuations:
                        no_punct = no_punct + char
        return no_punct

def punctuation_remover(input_text):
        punctuations = '''!#$%&'()—*+,-./:;?@[\]^_`{|}~–'''
        no_punct = ""
        for char in input_text:
                if char not in punctuations:
                        no_punct = no_punct + char
                else:
                        no_punct = no_punct + " "
        no_punct = no_punct.replace("\xa0"," ")
        no_punct = no_punct.replace("   ", " ")
        no_punct = no_punct.replace("  ", " ")
        return no_punct.strip()

def similarity_index(a, b):
    return SequenceMatcher(None, a, b).ratio()


def transform_control_keywords(raw_text):

        controls_keywords = ["area and bulk regulations", "area and bulk standards", "area and bulk requirements", "area and height regulations", "area and yard regulations", "area and development regulations", "area and dimensional regulations", "area and dimensional requirements", "lot and bulk requirements", "lot and bulk regulations", "lot area, width, depth", "area, height and special design regulations", "area and density regulations", "area, height and special regulations", "density and dimensional standards", "lot area, width, building coverage", "lot and setback regulations", "density and dimensional regulations", "development regulations", "dimensional criteria", "lot requirements", "lot and building requirements", "building requirements", "dimensions for development", "development requirements", "dimensional regulations", "design standards", "design requirements", "additional use requirements", "height regulations", "area, height and dimensional requirements", "area, yard and height regulations", "area, yard, and height regulations", "area, yard, height", "acreage and density requirements", "density requirements", "dimensional requirements", "lot, yard and height requirements", "general regulations", "area, density, yards and parking regulations", "site development standards", "site development", "construction standards", "general property development standards", "lot limitations", "lot size", "front yard regulations", "rear yard regulations", "side yard regulations", "density, open space and dimensional standards", "dimensional standards", "intensity of lot use", "subdivision standards", "density/intensity", "required lot area and dimension", "required bulk standards", "performance standards", "performance regulations",  "height, bulk and space requirements", "property development standard", "special development standard", "other general development standard", "area, lot width and yard requirement", "other regulation", "yard requirement", "setback and yards", "area, density, lot width and yard requirement", "development criteria", "area, height, lot width and yard requirement", "minimum lot dimension", "minimum lot coverage", "lot coverage", "lot size and coverage", "minimum front and rear yard", "minimum side yard", "building height", "yards and setbacks", "setback requirements",  "minimum lot area", "maximum dwelling density", "land use regulations", "minimum lot size", "independent living unit regulations", "special regulations", "area, width", "district wide development standards", "lot and structure requirements", "lots and yards requirements", "lot area, building height", "height of building", "lot area, lot width and coverage requirements", "dimensional, open space and coverage regulations", "area, yard and height requirements", "yard and lot requirements",  "area, yard and height restrictions", "lot area, lot width, and coverage requirements", "capacity, area and bulk regulations", "lot, yard and height standards", "yards; lot area", "lot area and width", "lot area regulations", "height, lot width", "required lot size", "required open space", "lot area, building height and yard requirements", "lot, yard and building height requirements", "lot requirements", "bulk and area regulations", "bulk and lot regulations", "bulk and area requirements", "area restrictions and regulations", "height restrictions and regulations", "lot area, lot width", "lot area", "height and story regulations", "height limit", "height limitation", "maximum building and structure height", "maximum height", "maximum density", "specific standards governing all mixed use development", "maximum building coverage", "lot, yard and building requirements", "density, lot width", "lot width", "lot area and yard requirements", "lot area, dimensional and design standards", "lot area.", "lot area and density", "open space, impervious surface and area requirements", "standards of development", "general standards", "development standards", "bulk requirements", "bulk regulations", "bulk and use table", "area regulations", "area requirements", "density and area", "space and bulk standards", "space and bulk requirements", "yard regulations", "yard requirements", "bulk standards", "parking regulations", "special requirements", "height requirements", "height area and bulk", "height area and lot", "height, area and lot", "district regulations", "open space requirements", "minimum open space", "minimum floor area", "rear yard", "side yard", "front yard", "yard dimensions", "yard required", "lot, bulk and intensity", "lot, bulk", "area, yard", "lot size", "height, yard", "setbacks"]

        for iteration, input_text in enumerate(raw_text):

                input_text = str(raw_text[iteration])
                input_text_copy = input_text
                input_text = input_text.lower()

                previous_sentence = raw_text[iteration - 1].lower()
                second_previous_sentence = raw_text[iteration - 2].lower()
                third_previous_sentence = raw_text[iteration - 3].lower()
                fourth_previous_sentence = raw_text[iteration - 4].lower()
                fifth_previous_sentence = raw_text[iteration - 5].lower()
                sixth_previous_sentence = raw_text[iteration - 6].lower()

                keyword_not_found_flag = 0

                for keyword in controls_keywords:
                        keyword_found_flag = input_text.find(keyword)

                        if keyword_found_flag != -1:
                                
                                # For structure with zone names within one heading
                                find_previous_target_flag = previous_sentence.find('<span class="titletitle">')
                                find_second_previous_target_flag = second_previous_sentence.find('span')
                                find_fourth_previous_target_flag = fourth_previous_sentence.find('<span class="titlenumber">')
                                find_fifth_previous_target_flag = fifth_previous_sentence.find('<a href="')
                                find_sixth_previous_target_flag = sixth_previous_sentence.find('<label class="selectionlabel" id="')

                                if find_previous_target_flag != -1 and find_second_previous_target_flag != -1 and find_fourth_previous_target_flag != -1 and find_fifth_previous_target_flag != -1 and find_sixth_previous_target_flag != -1:

                                        rep_text = "ZONE CONTROLS" + ":" + keyword
                                        raw_text[iteration] = input_text.replace(keyword, rep_text)
                                        break
                                
                                # For structure with zone names within a single heading
                                find_target_flag = input_text.find('</a><div class="litem_content content"><div class="para">')
                                find_target2_flag = input_text.find('class="litem_number" href="')
                                find_target3_flag = input_text.find('class="para">')
                                # find_previous_target_flag = previous_sentence.find('<div class="footnotes"></div></div></div>')
                                # find_second_previous_target_flag = second_previous_sentence.find('</div>')
                                # find_third_previous_target_flag = third_previous_sentence.find('<div class="footnotes"></div></div></div>')
                                # find_fourth_previous_target_flag = fourth_previous_sentence.find('</div>')
                                # find_fifth_previous_target_flag = fifth_previous_sentence.find('<div class="footnotes"></div></div></div>')

                                # if find_target_flag != -1 and find_target2_flag != -1 and find_previous_target_flag != -1 and find_second_previous_target_flag == 0 and find_third_previous_target_flag != -1 and find_fourth_previous_target_flag == 0:
                                flags_distance = keyword_found_flag - find_target3_flag
                                if find_target_flag != -1 and find_target2_flag != -1 and flags_distance < 15:

                                        rep_text = "ZONE CONTROLS" + ":" + keyword
                                        raw_text[iteration] = input_text.replace(keyword, rep_text)
                                        break

                
        return raw_text
                

