# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json

class _xml:
	def __init__(self, url):
		self.url = url
	
	def get_list(self):
		try:
			xml = ET.fromstring(self.get_page())
		except ET.ParseError:
			xml = ET.fromstringlist(["<root>", self.get_page(), "</root>"])
		item_list = []
		for item in xml:
			item_list.append(self.get_items(item))
		return item_list

	def get_page(self):
		if self.url.startswith('http'):
			from .downloader import Downloader
			d = Downloader(self.url)
			return d.get_urllib()
		else:
			return open(self.url).read()
   
	def get_items(self, item):
		items = {child.tag: child.text for child in item}
		return items
	
	def process_builds(self):
		item_list = self.get_list()
		build_list = []
		for item in item_list:
			name = item.get('name', '')
			version = item.get('version', '')
			url = item.get('url', '')
			icon = item.get('icon', '')
			fanart = item.get('fanart', '')
			description = item.get('description', '')
			build_list.append({'name': name, 'version': version, 'url': url, 'icon': icon, 'fanart': fanart, 'description': description})
		build_list = {'builds': build_list}
		return json.dumps(build_list)