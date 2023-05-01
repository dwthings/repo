import sys
from urllib.parse import unquote_plus

class Params:
	
	def get_params(self):
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
				params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
				splitparams={}
				splitparams=pairsofparams[i].split('=')
				if (len(splitparams))==2:
					param[splitparams[0]]=splitparams[1]
		return param
	
	def get_name(self):
		params=self.get_params()
		name = None
		try:
			name = unquote_plus(params["name"])
		except:
			pass
		return name
	
	def get_name2(self):
		params=self.get_params()
		name2 = None
		try:
			name2 = unquote_plus(params["name2"])
		except:
			pass
		return name2
	
	def get_version(self):
		params=self.get_params()
		version = None
		try:
			version = unquote_plus(params["version"])
		except:
			pass
		return version
	
	def get_url(self):
		params=self.get_params()
		url = None
		try:
			url = unquote_plus(params["url"])
		except:
			pass
		return url
	
	def get_mode(self):
		params=self.get_params()
		mode = None
		try:        
			mode=int(params["mode"])
		except:
			pass
		return mode
	
	def get_iconimage(self):
		params=self.get_params()
		iconimage = None
		try:
			iconimage = unquote_plus(params["iconimage"])
		except:
			pass
		return iconimage
	
	def get_fanart(self):
		params=self.get_params()
		fanart = None
		try:
			fanart = unquote_plus(params["fanart"])
		except:
			pass
		return fanart
	
	def get_description(self):
		params=self.get_params()
		description = None
		try:
			description = unquote_plus(params["description"])
		except:
			pass
		return description
p = Params()