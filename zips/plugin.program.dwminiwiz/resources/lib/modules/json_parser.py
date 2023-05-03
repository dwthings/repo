# -*- coding: utf-8 -*-
import json

class _json:
	def __init__(self, url):
		self.url = url
	
	def get_list(self):
		_list = self.get_page()
		return json.dumps(_list)
	
	def get_page(self):
		if self.url.startswith('http'):
			from .downloader import Downloader
			d = Downloader(self.url)
			return json.loads(d.get_urllib())
		else:
			return json.loads(open(self.url).read())