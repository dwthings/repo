import xbmc, xbmcgui
from urllib.parse import unquote_plus

class Player:
	def __init__(self, title, link, icon):
		self.title = title
		self.link = link
		self.icon = icon
	
	def play_link(self):
		link = unquote_plus(self.link)
		liz = xbmcgui.ListItem(self.title)
		liz.setInfo('video', {'Title': self.title})
		liz.setArt({'thumb': self.icon, 'icon': self.icon})
		liz.setProperty('IsPlayable', 'true')
		xbmc.Player().play(link,liz)