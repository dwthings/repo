import xbmc, xbmcgui, xbmcplugin
import sys
from urllib.parse import quote_plus

def addDir(name,url,mode,iconimage,fanart,description, name2='', version='', addcontext=False,isFolder=True):
	u=sys.argv[0]+"?url="+quote_plus(url)+"&mode="+str(mode)+"&name="+quote_plus(name)+"&icon="+quote_plus(iconimage) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)+"&name2="+quote_plus(name2)+"&version="+quote_plus(version)
	liz=xbmcgui.ListItem(name)
	liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':iconimage})
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "plotoutline": description})
	if addcontext:
		contextMenu = []
		liz.addContextMenuItems(contextMenu)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)