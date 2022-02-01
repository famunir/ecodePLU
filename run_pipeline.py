# execute the complete pipeline

import os
import sys
from flask import Flask
from flask_restful import Api, Resource, request
import urllib.parse
from flask_cors import CORS

sys.path.append(".")

from main.extract_relevant_text import extract_all_text
from main.extract_html import extract_control_html

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class AllZonePlus(Resource):
	# def get(self, link, zonenames):

	# 	link = urllib.parse.unquote(link)
	# 	zonenames = urllib.parse.unquote(zonenames)

	# 	file_name = link.replace("https://ecode360.com/", "")
	# 	file_name = f"{file_name}.txt"

	# 	all_zone_names = zonenames.split("'''")

	# 	os.system("rm -rf scrapy-result/*.txt")
	# 	os.system(f"python3 main/scrape-ecode.py {link}")

	# 	all_plus = extract_all_text(file_name, all_zone_names)
	# 	return {"all_plus" : all_plus}

	def post(self):

		#link = urllib.parse.unquote(request.form["link"])
		#zonenames = urllib.parse.unquote(request.form["zonenames"])

		link = request.form["link"]
		zonenames = request.form["zonenames"]

		file_name = link.replace("https://ecode360.com/", "")

		all_zone_names = zonenames.split("'''")

		os.system("rm -rf scrapy-result/*.txt")
		os.system("rm -rf scrapy-result/*.html")
		
		os.system(f"python3 main/scrape-ecode.py {link}")

		all_plus = extract_all_text(file_name, all_zone_names)
		return {"all_plus" : all_plus}

api.add_resource(AllZonePlus, "/getallplus")

class ZoneControls(Resource):

	def post(self):

		link = request.form["link"]
		zonenames = request.form["zonenames"]

		file_name = link.replace("https://ecode360.com/", "")

		all_zone_names = zonenames.split("'''")

		os.system(f"python3 main/scrape-ecode-for-html.py {link}")

		zone_controls = extract_control_html(file_name, all_zone_names)
		return {"zone_controls" : zone_controls}

api.add_resource(ZoneControls, "/getzonecontrols")

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

