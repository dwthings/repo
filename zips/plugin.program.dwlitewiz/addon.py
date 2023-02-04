import xbmc, xbmcplugin
import sys
import addonvar
from resources.lib.modules.params import p

xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)

name = p.get_name()
name2 = p.get_name2()
version = p.get_version()
url = p.get_url()
mode = p.get_mode()
iconimage = p.get_iconimage()
fanart = p.get_fanart()
description = p.get_description()

xbmc.executebuiltin('Dialog.Close(busydialog)')

if mode==None:
	from resources.lib.modules.menus import main_menu
	main_menu()
	
elif mode==1:
	from resources.lib.modules.menus import build_menu
	build_menu()

elif mode==3:
	from resources.lib.modules.buildinstall import main
	main(name, name2, version, url, iconimage, fanart, description)

elif mode==4:
	from resources.lib.modules.maintenance import fresh_start
	fresh_start()

elif mode==5:
	from resources.lib.modules.menus import submenu_maintenance
	submenu_maintenance()
	
elif mode==6:
	from resources.lib.modules.maintenance import clear_packages
	clear_packages()
	
elif mode==7:
	from resources.lib.modules.maintenance import clear_thumbnails
	clear_thumbnails()

elif mode==8:
	from resources.lib.modules.maintenance import advanced_settings
	advanced_settings()
	
elif mode==9:
	from xbmcaddon import Addon
	Addon(addonvar.addon_id).openSettings()

elif mode==10:
	from resources.lib.modules.player import Player
	pl = Player(name,url,iconimage)
	pl.play_link()

elif mode==100:
	from resources.lib.GUIcontrol import notify
	d=notify.notify()
	d.doModal()
	del d

xbmcplugin.endOfDirectory(int(sys.argv[1]))